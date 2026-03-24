#!/bin/sh
set -eu

DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
"$DIR/scripts/check-env.sh"
mkdir -p "$DIR/.clawpilot/logs" "$DIR/.clawpilot/tmp"
printf '%s\n' 'Next steps:' '  - fill .env' '  - start postgres' '  - start temporal' '  - validate ClawLoop/OpenClaw paths'
