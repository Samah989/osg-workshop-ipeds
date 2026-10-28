# Research Computing on the Open Science Pool. Hands-on workshop

**Instructor:** Samah Alshrief, Ph.D

In this workshop you'll take a research pipeline (IPEDS higher-education panel regression) from a laptop to a distributed job running on the Open Science Pool (OSPool) via HTCondor. No prior HTCondor experience assumed.

## Outcomes

After the workshop you will have:

- A working HTCondor **submit file** that requests CPU/memory/disk and ships input data
- A **shell wrapper** that installs Python dependencies inside the OSPool container and runs your analysis
- A completed job that produced regression coefficients as a CSV in your OSG home directory
- The vocabulary to read `.log`, `.out`, `.err` files and diagnose failures

## Prerequisites (before the workshop)

- An OSPool account (email me your name a few days in advance so I can request access)


## Repo layout

```
osg-workshop-ipeds/
├── README.md                        (this file)
├── requirements-osg.txt             pip-pinned deps for the OSPool container
├── src/
│   ├── __init__.py
│   └── regression.py                helper: fixed_effects_panel, real-dollar deflator
├── run_regression.py                the analysis script  -  pandas → coefficients CSV
├── data/                            small parquet sample so the demo runs quickly
│   └── (5 files, ~15 MB total  -  one year of each IPEDS dataset)
├── notebooks/
│   └── copy_paste_guide.ipynb       step-by-step workshop guide with snippets
└── ANSWER_KEY/                      final .sh + .submit files, for after-workshop reference
    ├── run_regression.sh
    └── run_regression.submit
```

## Workshop flow

1. **Clone this repo onto the OSPool access point** (`ap40.uw.osg-htc.org`)
2. Peek at the data and the Python script
3. Together, write the shell wrapper with `nano` (you'll paste from the notebook)
4. Together, write the HTCondor submit file with `nano` (you'll paste from the notebook)
5. `condor_submit run_regression.submit`
6. Watch it with `condor_q -nobatch`, read the logs, pull the result CSV back

Full step-by-step is in [`notebooks/copy_paste_guide.ipynb`](notebooks/copy_paste_guide.ipynb).

## After the workshop

The `ANSWER_KEY/` folder has the final versions of `run_regression.sh` and `run_regression.submit` for reference. Try modifying them: change the RQ, change resource requests, add a second RQ as a queued sub-job.

## Related public resources

- OSPool docs: <https://portal.osg-htc.org/documentation/>
- HTCondor manual: <https://htcondor.readthedocs.io>
- IPEDS via Urban Institute Education Data Portal: <https://educationdata.urban.org/documentation/>

## License

MIT  -  see [LICENSE](./LICENSE).
