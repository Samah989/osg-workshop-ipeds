#!/bin/bash
set -eo pipefail

# Create the output directory first so HTCondor always has something to return.
mkdir -p results deps

echo "Host: $(hostname)"
echo "Python: $(python3 --version)"

# The container has Python but not pandas. Install into ./deps (no virtualenv needed).
python3 -m ensurepip --user 2>/dev/null || true
python3 -m pip install --quiet --target=deps pandas pyarrow

export PYTHONPATH="$PWD/deps:${PYTHONPATH:-}"
python3 summarize.py directory_2015.parquet results/

echo "Output files:"
ls -l results
