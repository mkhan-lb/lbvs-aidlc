#!/bin/sh
# UserPromptExpansion hook (matcher lbvs-aidlc): AIDLC skills take at most one bare change ID.
# /lbvs-aidlc-ticket keeps its ticket reference and /lbvs-aidlc-report its kind and summary;
# /lbvs-aidlc-init and /lbvs-aidlc-onboard take nothing. Any other argument shape blocks the expansion so the ID is not misread as context.
# Exits 0 silently on anything it cannot parse.
AIDLC_HOOK_INPUT=$(cat 2>/dev/null || true)
export AIDLC_HOOK_INPUT
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then AIDLC_HELPER="${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py"; else AIDLC_HELPER="${CLAUDE_PROJECT_DIR:-$PWD}/scripts/aidlc.py"; fi
export AIDLC_HELPER
exec python3 - <<'PY'
import json, os, re, sys

CHANGE_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NO_ARGUMENTS = {"lbvs-aidlc-init", "lbvs-aidlc-onboard"}
EXEMPT = {"lbvs-aidlc-ticket", "lbvs-aidlc-report"}

def rejected(name, arguments):
    if name in EXEMPT:
        return False
    tokens = arguments.split()
    if name in NO_ARGUMENTS:
        return bool(tokens)
    return len(tokens) > 1 or (len(tokens) == 1 and not CHANGE_ID.match(tokens[0]))

def main():
    try:
        payload = json.loads(os.environ.get("AIDLC_HOOK_INPUT", ""))
    except Exception:
        return
    if not isinstance(payload, dict):
        return
    name = payload.get("command_name")
    if not isinstance(name, str):
        return
    name = name.lstrip("/").rsplit(":", 1)[-1]
    if not name.startswith("lbvs-aidlc"):
        return
    arguments = payload.get("command_args")
    if not isinstance(arguments, str):
        arguments = ""
    if not rejected(name, arguments):
        return
    json.dump({"decision": "block",
               "reason": "AIDLC: pass one bare change ID (or none); put context in the next message."}, sys.stdout)
    sys.stdout.write("\n")

try:
    main()
except Exception:
    # A crash here is a workflow defect: report it (traceback and session facts only, never the payload) and stay silent.
    import os, subprocess, sys, traceback
    try:
        reporter = subprocess.Popen([sys.executable, os.environ["AIDLC_HELPER"], "--root", os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd(), "report-bug", "--component", "hooks/argument-guard.sh"],
                                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        reporter.stdin.write(traceback.format_exc().encode("utf-8"))
        reporter.stdin.close()
    except Exception:
        pass
PY
