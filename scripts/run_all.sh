#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/scripts/server_env.sh"
python "$ROOT/run.py" --validate
python "$ROOT/scripts/export_templates.py"
# Requires a generated Uni-Mol structural CSV and the optional GNN dependencies.
status=0
python "$ROOT/run.py" --experiments all --jobs 1 --save-models "$@" || status=$?
python "$ROOT/scripts/make_report.py" || status=1
exit "$status"
