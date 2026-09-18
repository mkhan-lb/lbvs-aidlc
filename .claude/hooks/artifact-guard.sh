#!/bin/sh
# PreToolUse hook (Edit/Write/MultiEdit/NotebookEdit): the text about to land in a change
# artifact (changes/**/*.md) or lesson (docs/solutions/**/*.md) is piped through
# `aidlc.py lint-artifacts --stdin <repo-relative path>`; any hit denies the edit with the
# offending lines. The helper is the plugin's copy when CLAUDE_PLUGIN_ROOT is set, else the
# project's scripts/aidlc.py. Exits 0 silently on anything it cannot interpret or lint.
AIDLC_HOOK_INPUT=$(cat 2>/dev/null || true)
export AIDLC_HOOK_INPUT
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  AIDLC_HELPER="${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py"
else
  AIDLC_HELPER="${CLAUDE_PROJECT_DIR:-$PWD}/scripts/aidlc.py"
fi
exec python3 - "${CLAUDE_PROJECT_DIR:-$PWD}" "$AIDLC_HELPER" <<'PY'
import json, os, subprocess, sys

GUARDED = ("changes/", "docs/solutions/")

def git_toplevel(path):
    try:
        result = subprocess.run(["git", "-C", path, "rev-parse", "--show-toplevel"],
                                capture_output=True, text=True, timeout=5, check=False)
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None

def relative_target(payload, target):
    cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else None
    absolute = os.path.realpath(target if os.path.isabs(target) else os.path.join(cwd or sys.argv[1], target))
    for root in (git_toplevel(os.path.dirname(absolute)), cwd, sys.argv[1]):
        if not root or not os.path.isdir(root):
            continue
        relative = os.path.relpath(absolute, os.path.realpath(root)).replace(os.sep, "/")
        if not relative.startswith(".."):
            return root, relative
    return None, None

def new_text(tool_input):
    if isinstance(tool_input.get("edits"), list):
        return "\n".join(e.get("new_string", "") for e in tool_input["edits"] if isinstance(e, dict))
    for key in ("content", "new_string", "new_source"):
        if isinstance(tool_input.get(key), str):
            return tool_input[key]
    return None

def deny(reason):
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}, sys.stdout)
    sys.stdout.write("\n")

def main():
    try:
        payload = json.loads(os.environ.get("AIDLC_HOOK_INPUT", ""))
    except Exception:
        return
    if not isinstance(payload, dict):
        return
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not isinstance(target, str) or not target.endswith(".md"):
        return
    root, relative = relative_target(payload, target)
    if not relative or not relative.startswith(GUARDED):
        return
    text = new_text(tool_input)
    if text is None or not os.path.isfile(sys.argv[2]):
        return
    result = subprocess.run([sys.executable, sys.argv[2], "lint-artifacts", "--stdin", relative],
                            input=text, capture_output=True, text=True, timeout=20, check=False, cwd=root)
    if result.returncode != 1:
        return
    hits = [line for line in result.stdout.splitlines() if line.strip()][:5]
    deny("AIDLC: {} would carry session or machine-local references:\n{}\n"
         "Content boundary: docs/ARTIFACTS.md#content-boundary".format(relative, "\n".join(hits)))

try:
    main()
except Exception:
    pass
PY
