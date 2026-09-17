#!/bin/sh
set -eu
exec python3 "${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}/scripts/aidlc.py" mode
