# 01 Setup

## Goal

Log into the Open Science Pool access point, clone this repo, confirm the files are present.

## Prerequisites

- OSPool account (request at <https://portal.osg-htc.org/application>)
- Terminal on your laptop
- Git on your laptop

## Steps

1. SSH to the access point:
   ```bash
   ssh <your-osg-username>@ap40.uw.osg-htc.org
   ```

2. Clone the repo:
   ```bash
   git clone https://github.com/Samah989/osg-workshop-ipeds.git ~/workshop
   cd ~/workshop
   ```

3. List the contents:
   ```bash
   ls
   ```

4. Count the parquet files:
   ```bash
   ls data/ | wc -l
   ```

5. Confirm HTCondor is available:
   ```bash
   condor_q
   ```

## Expected output

Step 3:
```
ANSWER_KEY  LICENSE  README.md  data  notebooks  requirements-osg.txt  run_regression.py  src  tutorials
```

Step 4:
```
75
```

Step 5: an empty queue header (no error).

## Files in the repo

| Path | Purpose |
|---|---|
| `run_regression.py` | Analysis script |
| `src/regression.py` | Panel OLS and CPI deflator |
| `requirements-osg.txt` | pip packages |
| `data/` | 75 IPEDS parquet files, 2003-2023 |
| `ANSWER_KEY/` | Finished `run_regression.sh` and `run_regression.submit` |
| `notebooks/` | Copy-paste guide |
| `tutorials/` | These lessons |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ssh: Could not resolve hostname` | Check username spelling; try `ap40.uw.osg-htc.org` (no `www`) |
| `condor_q: command not found` | Account not fully provisioned; email `support@osg-htc.org` |
| Fewer than 75 parquet files | Repo clone was interrupted; delete `~/workshop` and clone again |
