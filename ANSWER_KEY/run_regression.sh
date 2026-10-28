#!/bin/bash
# ---------------------------------------------------------------------------
# OSG wrapper: run the IPEDS RQ2 regression inside the OSPool container.
# Installs pip deps to ./deps (osgvo-ubuntu-20.04 does not ship python3-venv).
# ---------------------------------------------------------------------------
set -eo pipefail
export PS4='+ [regress $(date +%H:%M:%S)] '
set -x

# 1. Create results/ FIRST so transfer_output_files always finds a dir,
#    even if pip or python later fail.
mkdir -p results deps
: > results/.placeholder

echo "[regress] host=$(hostname)  start=$(date -Iseconds)"
echo "[regress] pwd=$(pwd)  data/ contents:"
ls -la data 2>/dev/null | head -10 || echo "  (no data/ dir yet)"

# 2. Install Python dependencies into ./deps (no venv, no root needed).
python3 -m ensurepip --user 2>/dev/null || true
python3 -m pip install --upgrade --target=deps pip 2>/dev/null || python3 -m pip install --user --upgrade pip
python3 -m pip install --target=deps -r requirements-osg.txt

# 3. Put ./deps on the import path and run the analysis.
export PYTHONPATH="$PWD/deps:${PYTHONPATH:-}"
python3 run_regression.py --out results/

echo "[regress] done=$(date -Iseconds)  outputs:"
ls -lh results
