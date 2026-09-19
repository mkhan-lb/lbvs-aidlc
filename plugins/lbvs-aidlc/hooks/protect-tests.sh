#!/bin/sh
# PreToolUse hook: deny Edit/Write/MultiEdit/NotebookEdit on paths listed as
# "protected" in any .aidlc/fix/*.json marker (written by /lbvs-aidlc-fix while a
# reproduction test must stay untouched). Markers are looked up from the repository
# that holds the target file (its git top level or nearest `.aidlc/fix` ancestor, which
# may be a worktree the session did not start in), then from the hook's `cwd` and from
# CLAUDE_PROJECT_DIR (the main checkout). Exits 0 silently on anything it cannot
# interpret so unrelated edits are never blocked.
AIDLC_HOOK_INPUT=$(cat 2>/dev/null || true)
export AIDLC_HOOK_INPUT
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then AIDLC_HELPER="${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py"; else AIDLC_HELPER="${CLAUDE_PROJECT_DIR:-$PWD}/scripts/aidlc.py"; fi
export AIDLC_HELPER
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

def fix_root(path):
    path = os.path.realpath(path)
    while True:
        if os.path.isdir(os.path.join(path, ".aidlc", "fix")):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            return None
        path = parent

def roots(payload, target):
    cwd = payload.get("cwd")
    if not (isinstance(cwd, str) and cwd):
        cwd = None
    target_dir = os.path.dirname(target if os.path.isabs(target) else os.path.join(cwd or sys.argv[1], target))
    candidates = [fix_root(target_dir), git_toplevel(target_dir)]
    if cwd:
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
    for root in roots(payload, target):
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
    # A crash here is a workflow defect: report it (traceback and session facts only, never the payload) and stay silent.
    import os, subprocess, sys, traceback
    try:
        reporter = subprocess.Popen([sys.executable, os.environ["AIDLC_HELPER"], "--root", os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd(), "report-bug", "--component", "hooks/protect-tests.sh"],
                                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        reporter.stdin.write(traceback.format_exc().encode("utf-8"))
        reporter.stdin.close()
    except Exception:
        pass
PY
