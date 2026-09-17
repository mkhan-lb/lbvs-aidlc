#!/bin/sh
# PreToolUse hook: deny Edit/Write/MultiEdit/NotebookEdit on paths listed as
# "protected" in any .aidlc/fix/*.json marker (written by /lbvs-aidlc-fix while a
# reproduction test must stay untouched). Markers are looked up from the hook's
# `cwd` (which follows Claude into a worktree) and from CLAUDE_PROJECT_DIR (which
# stays at the main checkout). Exits 0 silently on anything it cannot interpret so
# unrelated edits are never blocked.
AIDLC_HOOK_INPUT=$(cat 2>/dev/null || true)
export AIDLC_HOOK_INPUT
exec python3 - "${CLAUDE_PROJECT_DIR:-$PWD}" <<'PY'
import fnmatch, glob, json, os, subprocess, sys

def git_toplevel(path):
    try:
        result = subprocess.run(["git", "-C", path, "rev-parse", "--show-toplevel"],
                                capture_output=True, text=True, timeout=5, check=False)
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None

def roots(payload):
    candidates = []
    cwd = payload.get("cwd")
    if isinstance(cwd, str) and cwd:
        candidates += [git_toplevel(cwd), cwd]
    candidates.append(sys.argv[1])
    seen = []
    for candidate in candidates:
        if candidate and os.path.isdir(candidate):
            real = os.path.realpath(candidate)
            if real not in seen:
                seen.append(real)
    return seen

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
    if not isinstance(target, str) or not target:
        return
    for root in roots(payload):
        markers = sorted(glob.glob(os.path.join(root, ".aidlc", "fix", "*.json")))
        if not markers:
            continue
        absolute = os.path.realpath(target if os.path.isabs(target) else os.path.join(root, target))
        relative = os.path.relpath(absolute, root)
        candidates = (absolute, relative, relative.replace(os.sep, "/"))
        for marker in markers:
            try:
                with open(marker, encoding="utf-8") as handle:
                    data = json.load(handle)
            except Exception:
                continue
            if not isinstance(data, dict):
                continue
            change_id = data.get("change_id") or os.path.splitext(os.path.basename(marker))[0]
            for pattern in data.get("protected") or []:
                if not isinstance(pattern, str) or not pattern:
                    continue
                normalized = pattern.rstrip("/")
                expanded = normalized if os.path.isabs(normalized) else os.path.join(root, normalized)
                forms = {normalized, expanded, os.path.realpath(expanded)}
                if any(c == f or fnmatch.fnmatchcase(c, f) for c in candidates for f in forms):
                    deny(
                        "lbvs-aidlc-fix protects {} while change '{}' is in progress "
                        "(marker {}). Keep the failing reproduction test unchanged; "
                        "if the test itself is wrong, ask the user to lift protection by deleting the marker."
                        .format(relative, change_id, os.path.relpath(marker, root)))
                    return

try:
    main()
except Exception:
    pass
PY
