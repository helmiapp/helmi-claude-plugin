"""PostToolUse(Write) hook: when a new document-like file is written, suggest saving it to Helmi."""
import json, os
from state import read_input, state_path

DOC_EXT = {".md", ".pdf", ".docx", ".pptx", ".xlsx", ".csv"}
CODE_DIRS = {"src", "app", "lib", "tests", "test", "node_modules", ".claude", ".git"}
SKIP_NAMES = {"claude.md", "skill.md", "readme.md", "agents.md", "changelog.md"}
MIN_BYTES = 1500
MAX_PER_SESSION = 2


def is_candidate(path, response):
    if isinstance(response, dict) and response.get("type") == "update":
        return False
    if os.path.splitext(path)[1].lower() not in DOC_EXT or os.path.basename(path).lower() in SKIP_NAMES:
        return False
    if CODE_DIRS & set(os.path.normpath(path).split(os.sep)):
        return False
    try:
        return os.path.getsize(path) > MIN_BYTES
    except OSError:
        return False


def main():
    data = read_input()
    path = (data.get("tool_input") or {}).get("file_path", "")
    if not path or not is_candidate(path, data.get("tool_response")):
        return
    log = state_path(data.get("session_id"), "docs")
    seen = open(log).read().splitlines() if os.path.exists(log) else []
    if path in seen or len(seen) >= MAX_PER_SESSION:
        return
    with open(log, "a") as f:
        f.write(path + "\n")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": (
            "You just created %s. If it is something other people will read or need later, call vault-overview "
            "(and browse-vault on the likely folder), then suggest ONE Helmi vault path for it in a single line at "
            "the end of your reply. Do not upload without a yes (the /helmi:save skill has the steps). "
            "If it is scratch work, say nothing about Helmi." % path
        ),
    }}))


if __name__ == "__main__":
    main()
