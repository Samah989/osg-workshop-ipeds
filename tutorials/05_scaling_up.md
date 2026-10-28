# 05 Scaling Up

## Goal

Submit many jobs from one submit file using `queue`.

## Prerequisites

- Tutorials 01-04 complete

## `queue` syntax

| Form | Behavior |
|---|---|
| `queue N` | N copies of the same job; use `$(Process)` to vary output |
| `queue var from file` | One job per line in the file; `$(var)` holds the current line |
| `queue var matching (pattern)` | One job per matching file; `$(var)` holds the filename |
| `queue var in (a, b, c)` | One job per listed value |

## Automatic variables

| Variable | Value |
|---|---|
| `$(Cluster)` | Shared cluster ID assigned at submit |
| `$(Process)` | 0, 1, 2, ... for each copy inside a cluster |
| `$(Item)` or your named variable | Current value from `queue from` or `queue in` |

## Example 1  -  N identical copies

```
executable = run_regression.sh
arguments  = --seed $(Process)

output = logs/regress.$(Cluster).$(Process).out
error  = logs/regress.$(Cluster).$(Process).err
log    = logs/regress.$(Cluster).$(Process).log

queue 50
```

Submits 50 jobs with seed 0 through 49.

## Example 2  -  One job per RQ

Edit `run_regression.sh` to take an argument:
```bash
RQ="$1"
python3 run_regression.py --rq "$RQ" --out results/
```

Submit:
```
executable = run_regression.sh
arguments  = $(rq_number)

transfer_input_files    = run_regression.py, requirements-osg.txt, src, data
transfer_output_files   = results

request_cpus   = 2
request_memory = 4 GB
request_disk   = 4 GB
+JobDurationCategory = "Medium"

log    = logs/regress.$(Cluster).$(Process).log
output = logs/regress.$(Cluster).$(Process).out
error  = logs/regress.$(Cluster).$(Process).err

queue rq_number from (
    1
    2
    3
)
```

Three jobs, one per RQ.

## Example 3  -  One job per parquet

```
transfer_input_files = run_regression.py, requirements-osg.txt, src, $(dataset)
arguments            = --dataset $(dataset) --out results/

queue dataset matching (data/*.parquet)
```

One job per matching file.

## Example 4  -  One job per state

File `states.txt`:
```
NJ
NY
CA
TX
PA
```

Submit:
```
arguments = --state $(state)
output    = logs/regress.$(Cluster).$(state).out
queue state from states.txt
```

## Monitoring a batch

```bash
condor_q                              # grouped
condor_q -nobatch                     # per-job
condor_watch_q                        # live
condor_q -held                        # just the holds
```

## Releasing a batch of held jobs after a fix

```bash
condor_release -constraint 'JobStatus == 5'
```

JobStatus `5` is the HTCondor code for held.

## Guidelines

| Do | Why |
|---|---|
| Keep `request_memory` and `request_disk` low | Smaller requests match slots faster |
| Set `max_retries = 2` on scaled runs | OSPool slots can be preempted |
| Use `$(Process)` or `$(var)` in output paths | Separate output per job |
| Bundle very short jobs into larger ones | Scheduler overhead dominates sub-minute jobs |

## Troubleshooting

| Symptom | Fix |
|---|---|
| All jobs log to the same file | Add `$(Process)` or `$(var)` to the `output`, `error`, `log` paths |
| Only some jobs match | Check `condor_q -better-analyze` on a stuck one; the matching slot pool may be small |
| `queue from file` reads nothing | Confirm the file is in the submit directory and has one value per line |
