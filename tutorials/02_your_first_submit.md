# 02 Your First Submit

## Goal

Create `run_regression.sh` and `run_regression.submit`, submit one job, confirm a result CSV returns.

## Prerequisites

- Tutorial 01 complete
- You are at the shell on `ap40` in `~/workshop`

## Steps

1. Create the wrapper:
   ```bash
   nano run_regression.sh
   ```
   Paste:
   ```bash
   #!/bin/bash
   set -eo pipefail
   export PS4='+ [regress $(date +%H:%M:%S)] '
   set -x

   mkdir -p results deps
   : > results/.placeholder

   echo "[regress] host=$(hostname) start=$(date -Iseconds)"
   ls -la data 2>/dev/null | head -10

   python3 -m ensurepip --user 2>/dev/null || true
   python3 -m pip install --upgrade --target=deps pip 2>/dev/null || python3 -m pip install --user --upgrade pip
   python3 -m pip install --target=deps -r requirements-osg.txt

   export PYTHONPATH="$PWD/deps:${PYTHONPATH:-}"
   python3 run_regression.py --out results/

   ls -lh results
   ```
   Save: `Ctrl-O`, `Enter`, `Ctrl-X`.

2. Make the wrapper executable:
   ```bash
   chmod +x run_regression.sh
   ```

3. Create the submit file:
   ```bash
   nano run_regression.submit
   ```
   Paste:
   ```
   container_image = /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-ubuntu-20.04:latest

   executable = run_regression.sh

   transfer_input_files    = run_regression.py, requirements-osg.txt, src, data
   transfer_output_files   = results
   should_transfer_files   = YES
   when_to_transfer_output = ON_EXIT

   request_cpus   = 2
   request_memory = 4 GB
   request_disk   = 4 GB

   +JobDurationCategory = "Medium"
   max_retries = 2

   log             = logs/regress.$(Cluster).log
   output          = logs/regress.$(Cluster).out
   error           = logs/regress.$(Cluster).err
   stream_output   = True
   stream_error    = True

   queue 1
   ```
   Save.

4. Create the logs directory:
   ```bash
   mkdir -p logs
   ```

5. Submit:
   ```bash
   condor_submit run_regression.submit
   ```

6. Record the cluster number from the output. Watch:
   ```bash
   condor_q -nobatch
   ```

7. When the job no longer appears in `condor_q`, read the result:
   ```bash
   ls -lh results/
   cat results/rq2_main.csv
   ```

## Expected output

Step 5:
```
Submitting job(s).
1 job(s) submitted to cluster NNNNNN.
```

Step 7:
```
rq2_main.csv (~700 bytes)
```
Content: one header row plus five coefficient rows (`log_instr_per_fte`, `log_admin_per_fte`, `log_fte`, `sector_2`, `sector_3`).

## HTCondor status codes

| `ST` | Meaning |
|---|---|
| `I` | Idle, waiting for a slot |
| `R` | Running |
| `H` | Held, see tutorial 04 |
| `C` | Completed |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `condor_submit: command not found` | Not on `ap40`; SSH back in |
| Job stays `I` for 10+ minutes | See tutorial 04, idle section |
| Job goes `H` immediately | See tutorial 04, held section |
| `results/` is empty | See tutorial 04, exited-with-no-output section |
