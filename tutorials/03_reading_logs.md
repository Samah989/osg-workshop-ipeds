# 03 Reading Logs

## Goal

Locate the three log files HTCondor produces per job and interpret their contents.

## Prerequisites

- Tutorial 02 complete
- At least one job submitted (completed or in-progress)

## The three files

For a submit file with:
```
log    = logs/regress.$(Cluster).log
output = logs/regress.$(Cluster).out
error  = logs/regress.$(Cluster).err
```

| File | Contents | Writer |
|---|---|---|
| `.log` | HTCondor event records (submitted, started, held, terminated) | HTCondor |
| `.out` | stdout of your wrapper and Python script | Your code |
| `.err` | stderr: `set -x` trace, Python tracebacks | Your code |

## Event codes in the `.log` file

| Code | Event |
|---|---|
| `000` | Submitted |
| `001` | Executing |
| `004` | Evicted |
| `005` | Terminated (check return value) |
| `006` | Memory usage report |
| `012` | Held |
| `021` | Starter message (usually an error) |
| `040` | Input/output file transfer |

## Steps

1. List all logs for your newest job:
   ```bash
   ls -t logs/*.log | head -1
   ```

2. Extract the key events:
   ```bash
   grep -E '^00[0145]|^012|^021' logs/regress.<cluster>.log
   ```

3. Read the stdout tail:
   ```bash
   tail -n 30 logs/regress.<cluster>.out
   ```

4. Read the stderr tail:
   ```bash
   tail -n 40 logs/regress.<cluster>.err
   ```

5. Confirm exit status:
   ```bash
   condor_history <cluster> -limit 1 -af ExitCode HoldReason JobStatus
   ```

## Expected output for a successful job

Step 2 (sequence of event codes):
```
000  submitted
040  started transferring input files
040  finished transferring input files
001  executing
040  started transferring output files
040  finished transferring output files
005  terminated with return value 0
```

Step 3 (stdout):
```
[regress] host=... start=...
total ...
-rw-r--r-- ... directory__2003__all__...parquet
...
Successfully installed Cython-... linearmodels-... pandas-... statsmodels-...
Panel: 27,867 obs, 2,465 institutions, years 2003-2017
### RQ2  -  grad rate ~ spending mix
- Observations: 24,112
- Entities: 2,308
- Within R²: 0.013
...
rq2_main.csv
```

Step 5:
```
ExitCode  HoldReason  JobStatus
0         undefined   4
```

(`JobStatus 4` = completed.)

## Streaming logs live

If `stream_output = True` and `stream_error = True` are in the submit file, the `.out` and `.err` files grow as the job runs. Watch:

```bash
tail -f logs/regress.<cluster>.out
tail -f logs/regress.<cluster>.err
```

`Ctrl-C` to stop watching.

## Common patterns in `.err`

| Pattern | Meaning |
|---|---|
| `Traceback (most recent call last):` | Python exception; next lines name the file and line number |
| `ERROR: Could not find a version that satisfies` | `requirements-osg.txt` asks for a package wheel that is not available |
| `syntax error near unexpected token` | Shell error in the wrapper |
| Just a `set -x` trace with no error after | Job was evicted mid-run; HTCondor will retry if `max_retries` is set |
