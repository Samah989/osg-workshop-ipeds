# 04 Debugging Held Jobs

## Goal

Diagnose a job stuck idle, held with a reason, or exited without producing output.

## Prerequisites

- Tutorials 01-03 complete
- A job that is not completing cleanly

## Three failure modes

| Queue state | Cause |
|---|---|
| `I` for over 10 minutes | No slot matches the resource request |
| `H` (held) | Transfer failure, resource overrun, or starter error |
| Gone from queue, `results/` empty | Script crashed before writing output |

---

## Mode 1  -  Stuck idle

1. Ask HTCondor why nothing matches:
   ```bash
   condor_q <cluster> -better-analyze | head -40
   ```

2. Read the "Request has not succeeded. 0 slot(s) matched" line and the attributes listed above it.

### Fixes

| In your submit | Change to |
|---|---|
| `request_memory = 64 GB` | `request_memory = 4 GB` |
| `+JobDurationCategory = "Short"` | `+JobDurationCategory = "Medium"` or `"Long"` |
| `container_image = .../osgvo-ubuntu-22.04:latest` | `container_image = .../osgvo-ubuntu-20.04:latest` |

### After the fix

```bash
condor_rm <cluster>
condor_submit run_regression.submit
```

---

## Mode 2  -  Held

1. Read the hold reason:
   ```bash
   condor_q -held
   ```

2. Match the hold code against the table below.

### Hold codes

| Code | Reason | Fix |
|---|---|---|
| `12/2` | Transfer output files failure (`results/` missing) | Add `mkdir -p results` at the top of the wrapper |
| `13/2` | Transfer input files failure | A file in `transfer_input_files` does not exist on the access point |
| `34/0` | Memory exceeded | Raise `request_memory` |
| `34/4` | Disk exceeded | Raise `request_disk` |
| `3/0` | PREPARE_JOB failed (container unavailable) | Check the `container_image` path |

### After the fix

```bash
condor_rm <cluster>
condor_submit run_regression.submit
```

---

## Mode 3  -  Exited with no output

1. Check the exit code:
   ```bash
   condor_history <cluster> -limit 1 -af ExitCode HoldReason JobStatus
   ```

2. Match the exit code against the table below.

### Exit codes

| Code | Meaning | Fix |
|---|---|---|
| `0` | Clean exit, but no CSV | Script wrote to a different path than `--out results/` |
| `1` | Python exception | Read `logs/regress.<cluster>.err` |
| `127` | Command not found | Typo in the wrapper |
| `139` | Segfault | Rare; usually native code |

### Common Python errors

| Error in `.err` | Fix |
|---|---|
| `IndentationError: unexpected indent` | Restore from git: `git checkout -- run_regression.py` |
| `KeyError: 'some_column'` | Column name in script does not match the parquet schema |
| `ModuleNotFoundError: No module named 'tabulate'` | Add the package to `requirements-osg.txt` and resubmit |
| `FileNotFoundError: No parquets matched data/...` | `data/` was empty on the execute point; confirm `transfer_input_files` includes `data` |

### After the fix

```bash
condor_submit run_regression.submit
```

---

## Audit workflow

```bash
condor_q -nobatch
condor_q -held
condor_history <cluster> -limit 1 -af ExitCode HoldReason JobStatus
tail -n 40 logs/regress.<cluster>.err
tail -n 30 logs/regress.<cluster>.out
```

## When to escalate

Email `support@osg-htc.org` with the cluster ID, the hold reason, and the `.log` and `.err` files when:

- The error is from HTCondor itself, not your code or wrapper
- A hold reason says `SYSTEM_PERIODIC_HOLD`
- The same job succeeds on one site and fails on another
