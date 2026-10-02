#!/usr/bin/env bash
# Pipes sample hook input into each hook script and asserts fire / skip.
set -u
H="$(cd "$(dirname "$0")" && pwd)/plugins/helmi/hooks"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
export CLAUDE_PLUGIN_DATA="$T/state"
fail=0
check() { # name, expected (fire|skip), output
  if { [ "$2" = fire ] && [ -n "$3" ]; } || { [ "$2" = skip ] && [ -z "$3" ]; }; then echo "ok   $1"; else echo "FAIL $1 (got: ${3:-<empty>})"; fail=1; fi
}

# Stop hook
echo '{"message":{"content":[{"type":"tool_use","name":"Read"}]}}' > "$T/qa.jsonl"
echo '{"message":{"content":[{"type":"tool_use","name":"Write"}]}}' > "$T/work.jsonl"
stop() { echo "{\"session_id\":\"$1\",\"transcript_path\":\"$2\",\"stop_hook_active\":$3}" | python3 "$H/stop_nudge.py"; }
check "stop: Q&A-only session is silent"   skip "$(stop s1 "$T/qa.jsonl" false)"
check "stop: session with a Write nudges"  fire "$(stop s2 "$T/work.jsonl" false)"
check "stop: second stop is silent"        skip "$(stop s2 "$T/work.jsonl" false)"
check "stop: stop_hook_active is silent"   skip "$(stop s3 "$T/work.jsonl" true)"

# Document hook
mkdir -p "$T/docs" "$T/repo/src"
big() { head -c 2000 /dev/zero | tr '\0' a > "$1"; }
big "$T/docs/report.md"; big "$T/docs/b.md"; big "$T/docs/c.md"; big "$T/repo/src/notes.md"; big "$T/docs/README.md"; big "$T/docs/x.py"
echo small > "$T/docs/small.md"
doc() { echo "{\"session_id\":\"$1\",\"tool_input\":{\"file_path\":\"$2\"},\"tool_response\":{\"type\":\"${3:-create}\"}}" | python3 "$H/doc_written.py"; }
check "doc: new report.md fires"          fire "$(doc d1 "$T/docs/report.md")"
check "doc: same path again is silent"    skip "$(doc d1 "$T/docs/report.md")"
check "doc: small file is silent"         skip "$(doc d2 "$T/docs/small.md")"
check "doc: code dir is silent"           skip "$(doc d2 "$T/repo/src/notes.md")"
check "doc: README is silent"             skip "$(doc d2 "$T/docs/README.md")"
check "doc: non-doc extension is silent"  skip "$(doc d2 "$T/docs/x.py")"
check "doc: overwrite is silent"          skip "$(doc d2 "$T/docs/b.md" update)"
check "doc: second doc fires"             fire "$(doc d1 "$T/docs/b.md")"
check "doc: third doc hits session cap"   skip "$(doc d1 "$T/docs/c.md")"

exit $fail
