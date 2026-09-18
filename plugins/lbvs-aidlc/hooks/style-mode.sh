#!/bin/sh
# SessionStart hook: apply the caveman reply style to chat replies. Level from AIDLC_STYLE,
# else <project>/.aidlc/style (lite | full | ultra | off), else lite. Prints nothing when off.
# Oh My Pi's guard extension runs this same script so both hosts inject identical text.
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
LEVEL="${AIDLC_STYLE:-}"
[ -z "$LEVEL" ] && [ -f "$ROOT/.aidlc/style" ] && LEVEL=$(tr -d '[:space:]' < "$ROOT/.aidlc/style")
[ -z "$LEVEL" ] && LEVEL=lite
case "$LEVEL" in
  off) exit 0 ;;
  lite|full|ultra) ;;
  *) LEVEL=lite ;;
esac
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then SKILL="${CLAUDE_PLUGIN_ROOT}/skills/caveman/SKILL.md"; else SKILL="$ROOT/.claude/skills/caveman/SKILL.md"; fi
cat <<EOF
[aidlc-reply-style]
Reply style: caveman $LEVEL (rules: $SKILL). Chat replies only; code, commits, PR bodies, changes/ artifacts, lessons and ADRs keep normal prose. Drop filler, pleasantries and hedging; keep every technical term, number, path, command and error string exact; never drop not/never/no/only. Level lite keeps articles and full sentences. Auto-clarity: switch to full sentences for security warnings, irreversible actions, ordered multi-step instructions and anything compression would make ambiguous. Say "normal mode" to stop for this session; set .aidlc/style to change the default.
EOF
