#!/usr/bin/env bash
set -euo pipefail

if command -v black >/dev/null 2>&1; then
  black --check .
else
  echo "black not installed, skip" >&2
fi

