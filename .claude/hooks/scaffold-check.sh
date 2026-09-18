#!/bin/sh
# SessionStart hook: when the repository's .aidlc/manifest.json records a plugin_version
# other than the running plugin's, print one line pointing at `aidlc update`. The plugin
# version comes from CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json when set, else from
# plugins/lbvs-aidlc/.claude-plugin/plugin.json under the project. Prints nothing otherwise.
exec python3 - "${CLAUDE_PROJECT_DIR:-$PWD}" "${CLAUDE_PLUGIN_ROOT:-}" <<'PY'
import json, os, sys

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
    if not installed:
        return
    plugin_json = os.path.join(plugin_root or os.path.join(project, "plugins", "lbvs-aidlc"), ".claude-plugin", "plugin.json")
    running = version(plugin_json, "version")
    if running and running != installed:
        print("AIDLC scaffold: installed with plugin {}, running {} — run `aidlc update` to refresh repository seeds.".format(installed, running))

try:
    main()
except Exception:
    pass
PY
