#!/bin/sh
# SessionStart hook: when the repository's .aidlc/manifest.json records a plugin_version
# other than the running plugin's, print one line pointing at `aidlc update`; count the automatic
# bug reports parked under .aidlc/reports/ because gh was not authenticated when they were captured. The plugin
# version comes from CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json when set, else from
# plugins/lbvs-aidlc/.claude-plugin/plugin.json under the project. Prints nothing otherwise.
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then AIDLC_HELPER="${CLAUDE_PLUGIN_ROOT}/scripts/aidlc.py"; else AIDLC_HELPER="${CLAUDE_PROJECT_DIR:-$PWD}/scripts/aidlc.py"; fi
export AIDLC_HELPER
exec python3 - "${CLAUDE_PROJECT_DIR:-$PWD}" "${CLAUDE_PLUGIN_ROOT:-}" <<'PY'
import glob, json, os, sys

def version(path, key):
    try:
        with open(path, encoding="utf-8") as handle:
            value = json.load(handle).get(key)
    except Exception:
        return None
    return value if isinstance(value, str) and value else None

def main():
    project, plugin_root = sys.argv[1], sys.argv[2]
    installed = version(os.path.join(project, ".aidlc", "manifest.json"), "plugin_version")
    parked = len(glob.glob(os.path.join(project, ".aidlc", "reports", "*.pending.json")))
    if parked:
        print("AIDLC: {} automatic bug report(s) parked under .aidlc/reports/ (gh was not authenticated); `aidlc report-bug --pending` files them.".format(parked))
    if not installed:
        return
    plugin_json = os.path.join(plugin_root or os.path.join(project, "plugins", "lbvs-aidlc"), ".claude-plugin", "plugin.json")
    running = version(plugin_json, "version")
    if running and running != installed:
        print("AIDLC scaffold: installed with plugin {}, running {} — run `aidlc update` to refresh repository seeds.".format(installed, running))

try:
    main()
except Exception:
    # A crash here is a workflow defect: report it (traceback and session facts only, never the payload) and stay silent.
    import os, subprocess, sys, traceback
    try:
        reporter = subprocess.Popen([sys.executable, os.environ["AIDLC_HELPER"], "--root", os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd(), "report-bug", "--component", "hooks/scaffold-check.sh"],
                                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        reporter.stdin.write(traceback.format_exc().encode("utf-8"))
        reporter.stdin.close()
    except Exception:
        pass
PY
