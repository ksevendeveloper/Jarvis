#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <command>"
  exit 2
fi

cmd="$*"
echo "[jarvis/scripts] Executing: $cmd"
bash -lc "$cmd"
