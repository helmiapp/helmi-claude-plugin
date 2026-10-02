"""Stop hook: once per session, after real file work, ask Claude to offer saving to Helmi."""
import json, os
from state import read_input, state_path

WORK_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
REASON = (
    "Before finishing: if this session produced decisions, documents or follow-ups worth keeping in Helmi, "
    "list them in one numbered list (Helmi MCP tools: add-project-note for decisions, upload-vault-file for files, "
    "manage-task for follow-ups) and ask the user which to save. Write nothing until they answer. "
    "If nothing is worth saving, just finish without mentioning Helmi."
)


def did_file_work(transcript_path):
    try:
        with open(transcript_path) as f:
            for line in f:
                if '"tool_use"' not in line:
                    continue
                msg = json.loads(line).get("message", {})
                for block in msg.get("content") or []:
                    if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") in WORK_TOOLS:
                        return True
    except (OSError, ValueError):
        return False
    return False


def main():
    data = read_input()
    if data.get("stop_hook_active"):
        return
    marker = state_path(data.get("session_id"), "stop")
    if os.path.exists(marker) or not did_file_work(data.get("transcript_path", "")):
        return
    open(marker, "w").close()
    print(json.dumps({"decision": "block", "reason": REASON}))


if __name__ == "__main__":
    main()
