#!/bin/sh
# PreToolUse hook (Bash): `gh pr create|merge|ready|edit|close`, `gh api` against a pulls
# endpoint, or a force-push (`git push --force*`, `+refspec`) anywhere in the command returns
# permissionDecision "ask" so the engineer confirms before a pull request opens, merges or
# history is rewritten. Ordinary git commit/push follow the normal permission flow. Exits 0
# silently on any other command and on anything it cannot parse.
AIDLC_HOOK_INPUT=$(cat 2>/dev/null || true)
export AIDLC_HOOK_INPUT
exec python3 - <<'PY'
import json, os, re, sys

SEPARATORS = re.compile(r"&&|\|\||[;|\n]")
ENV_ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
OPTIONS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}

PR_SUBCOMMANDS = {"create", "merge", "ready", "edit", "close", "reopen"}
FORCE_FLAGS = ("--force", "-f", "--force-with-lease", "--force-if-includes")

def words_of(segment):
    words = segment.split()
    while words and ENV_ASSIGNMENT.match(words[0]):
        words.pop(0)
    if words:
        words[0] = words[0].lstrip("({")
    return words

def positional(words, options_with_value):
    index = 1
    while index < len(words):
        word = words[index]
        if word in options_with_value:
            index += 2
        elif word.startswith("-"):
            index += 1
        else:
            return words[index:]
    return []

def needs_confirmation(segment):
    words = words_of(segment)
    if not words:
        return False
    if words[0] == "gh":
        rest = positional(words, {"-R", "--repo"})
        if rest[:1] == ["pr"] and len(rest) > 1 and rest[1] in PR_SUBCOMMANDS:
            return True
        return rest[:1] == ["api"] and any("/pulls" in word for word in rest) and any(
            word in ("-X", "--method") and index + 1 < len(words) and words[index + 1].upper() != "GET"
            for index, word in enumerate(words))
    if words[0] == "git":
        rest = positional(words, OPTIONS_WITH_VALUE)
        if rest[:1] != ["push"]:
            return False
        return any(word.startswith(FORCE_FLAGS) or word.startswith("+") for word in rest[1:])
    return False

def touches_history(command):
    return any(needs_confirmation(segment) for segment in SEPARATORS.split(command))

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
        "permissionDecisionReason": "AIDLC: opening or merging a pull request and force-pushing run only on "
                                    "your confirmation; /lbvs-aidlc-ship asks its own question first.",
    }}, sys.stdout)
    sys.stdout.write("\n")

try:
    main()
except Exception:
    pass
PY
