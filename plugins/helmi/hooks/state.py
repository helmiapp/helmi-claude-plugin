import json, os, re, sys, tempfile


def read_input():
    return json.load(sys.stdin)


def state_path(session_id, kind):
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(tempfile.gettempdir(), "helmi-plugin")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "%s-%s" % (re.sub(r"[^A-Za-z0-9_-]", "", session_id or "nosession"), kind))
