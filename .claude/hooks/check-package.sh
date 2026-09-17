#!/bin/sh
# SessionStart: stdout becomes context, so say nothing when the package is intact and
# put the errors on stdout when it is not, so Claude can act on them.
set -u
helper="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}/scripts/aidlc.py"
if ! output=$(python3 "$helper" check 2>&1); then
  printf 'AIDLC package check failed; fix before relying on the skills:\n%s\n' "$output"
fi
exit 0
