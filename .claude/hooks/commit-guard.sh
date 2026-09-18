#!/bin/sh
# PreToolUse hook (Bash): a `git ... commit` or `git ... push` anywhere in the command
# (chained with && ; || |, after `cd`, behind env assignments or `git -C <dir>`) returns
# permissionDecision "ask" so the engineer confirms before history changes. Exits 0 silently
# on any other command and on anything it cannot parse.
AIDLC_HOOK_INPUT=$(cat 2>/dev/null || true)
export AIDLC_HOOK_INPUT
exec python3 - <<'PY'
import json, os, re, sys

SEPARATORS = re.compile(r"&&|\|\||[;|\n]")
ENV_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
OPTIONS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}

def git_subcommand(segment):
    words = segment.split()
    while words and ENV_ASSIGNMENT.match(words[0]):
        words.pop(0)
    if not words or words[0].lstrip("({") != "git":
        return None
    index = 1
    while index < len(words):
        word = words[index]
        if word in OPTIONS_WITH_VALUE:
            index += 2
        elif word.startswith("-"):
            index += 1
        else:
            return word
    return None

def touches_history(command):
    return any(git_subcommand(segment) in ("commit", "push") for segment in SEPARATORS.split(command))

def main():
    try:
        payload = json.loads(os.environ.get("AIDLC_HOOK_INPUT", ""))
    except Exception:
        return
    if not isinstance(payload, dict):
        return
    tool_input = payload.get("tool_input") or {}
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not touches_history(command):
        return
    json.dump({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "AIDLC: git commit/push runs only on your confirmation; "
                                    "/lbvs-aidlc-ship and /lbvs-aidlc-fix ask before reaching this.",
    }}, sys.stdout)
    sys.stdout.write("\n")

try:
    main()
except Exception:
    pass
PY
