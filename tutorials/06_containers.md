# 06 Containers

## Goal

Use a CVMFS-hosted container image, understand when to build a custom one.

## Prerequisites

- Tutorials 01-05 complete

## Container paths on OSPool

Pre-built images live under CVMFS at:
```
/cvmfs/singularity.opensciencegrid.org/opensciencegrid/
```

Common tags:

| Path | Base OS |
|---|---|
| `.../opensciencegrid/osgvo-ubuntu-20.04:latest` | Ubuntu 20.04 |
| `.../opensciencegrid/osgvo-el7:latest` | CentOS 7 |
| `.../opensciencegrid/osgvo-el9:latest` | Rocky 9 |

The full browsable catalog: <https://portal.osg-htc.org/documentation/htc_workloads/using_software/available-containers-list/>

Reference the image in your submit file:
```
container_image = /cvmfs/singularity.opensciencegrid.org/opensciencegrid/osgvo-ubuntu-20.04:latest
```

## When to install dependencies in the wrapper vs. bake them into a container

| Install in wrapper (`pip install --target=deps`) | Bake into container |
|---|---|
| Few jobs | Many jobs |
| Dependencies change often | Dependencies stable |
| Python-only packages | Compiled packages (GDAL, R, Fortran) |
| Workshop or one-off analysis | Repeated production runs |

Wrapper-install cost per job: 30-60 seconds. Container cost: zero. Build cost: 10-30 minutes once, then push to Docker Hub.

## Building a custom container

### 1. Write `Dockerfile`

```dockerfile
FROM opensciencegrid/osgvo-ubuntu-20.04:latest
RUN pip install --no-cache-dir \
    pandas>=1.5,<2.1 \
    pyarrow \
    numpy>=1.22,<1.25 \
    statsmodels \
    linearmodels \
    scipy>=1.9,<1.11 \
    tabulate \
    requests \
    tqdm
```

### 2. Build and push

Needs Docker on your laptop and a free Docker Hub account.

```bash
docker build -t <dockerhub-user>/ipeds-regression:v1 .
docker push <dockerhub-user>/ipeds-regression:v1
```

### 3. Reference in submit

```
container_image = docker://<dockerhub-user>/ipeds-regression:v1
```

OSPool converts the Docker image to Apptainer SIF on first pull and caches it per compute node.

### 4. Shorter wrapper

With dependencies baked in, the wrapper collapses to:
```bash
#!/bin/bash
set -eo pipefail
mkdir -p results
python3 run_regression.py --out results/
```

## Vocabulary

| Term | Definition |
|---|---|
| Docker | Container tool for building images on a laptop; requires root |
| Apptainer | Container runtime that runs as a regular user; used on OSPool |
| SIF | Single-file container format Apptainer reads directly |
| CVMFS | Read-only global filesystem that delivers pre-built images to compute nodes |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Cannot download singularity image` | Container path typo; check the OSG catalog page for a currently-live tag |
| Job runs but packages missing | Container is bare; add `pip install --target=deps -r requirements-osg.txt` in the wrapper |
| Docker push rejected | Repository name must include your Docker Hub username as a prefix |
| Container works locally but not on OSPool | Image uses features unavailable in Apptainer; rebuild from the `opensciencegrid/osgvo-*` base |
