#!/usr/bin/env bash
# Server only. Uses the already activated environment; no automatic installation.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
source "$ROOT/scripts/server_env.sh"
export PYTHONUNBUFFERED=1
echo "Python: $(command -v python)"
echo "Project: $ROOT"
python scripts/prepare_embeddings.py --kind unimol || {
    echo 'Structural cache preparation failed. Check the active Uni-Mol environment.'
    exit 1
}
status=0
python run.py --experiments all --jobs 1 --save-models || status=$?
python scripts/export_templates.py || status=1
python scripts/make_report.py || status=1
echo 'Numerical tables and summary: results/RESULTS_TO_SEND.md'
echo 'If something failed, also send the last lines of the server log.'
exit "$status"
