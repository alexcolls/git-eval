#!/usr/bin/env bash
set -euo pipefail
# Helper to run the combine script (multi-repo analysis) without Poetry
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PYTHONPATH="$SCRIPT_DIR/src" python3 -m giteval.combine "$@"


