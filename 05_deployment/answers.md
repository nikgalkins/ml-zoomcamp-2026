# Homework 5: Deploying Machine Learning Models (2026)

Verified on October 26, 2026. Source: [official 2026 homework](https://github.com/DataTalksClub/machine-learning-zoomcamp/blob/a395ca7ca995df92d8321daa017f3a1b4425a4a0/cohorts/2026/homework/05-deployment/homework.md).
Release revision: `a395ca7ca995df92d8321daa017f3a1b4425a4a0`.

| Question | Answer | Verification |
|---|---|---|
| Q1 — Run `uv --version` | `uv 0.13.5 (46776a95d 2026-10-21 x86_64-pc-windows-msvc)` | Actual execution; setup check, not graded |
| Q2 — Exact locked scikit-learn version? | **1.7.2** | Official `pyproject.toml` and `uv.lock`; also confirmed by importing the installed package |
| Q3 — Conversion probability for the specified lead? | **0.533** | Actual `pickle.load` and `predict_proba`: `0.5329944186432507` |
| Q4 — Conversion probability from the local API? | **0.770** | Actual HTTP response: `{"conversion_probability":0.769799,"conversion":true}` |
| Q5 — Python base-image tag? | **python:3.11.15-slim-bookworm** | Verified from the unchanged official Dockerfile |
| Q6 — Conversion probability from the Docker container? | **Not verified**; expected **0.770** from the assignment's required parity with Q4 | Docker build/run could not execute; the official client passed against the local API only |

## Release integrity and environment

All 15 files in the official deployment directory were downloaded as raw bytes at the revision above, including every requested file, plus the official README, homework, grading configuration, and training script. The training script was not executed. Each file's `git hash-object --no-filters` matched its official GitHub blob SHA. Original files were not edited; `uv.lock` was not regenerated.

Model SHA-256, calculated with `Get-FileHash pipeline.bin -Algorithm SHA256`:

```text
1646bbdcd38d4f044da6b630c5b332c93a314245a8c21929011c42de51f629f1
```

`uv` was initially absent. Astral's [official PowerShell installer](https://docs.astral.sh/uv/getting-started/installation/) installed it into the repository's ignored `.runtime/hw5/uv` directory using `UV_UNMANAGED_INSTALL`. Python, its executable links, and the uv cache are also isolated under `.runtime/hw5`. Dependencies are installed only in `05_deployment/.venv`. The root `.venv` was not used or modified.

`uv sync --locked` succeeded, installing 18 packages. Execution confirmed Python **3.11.15**, scikit-learn **1.7.2**, and interpreter path `05_deployment/.venv/Scripts/python.exe`.

## Q3: exact input and execution

The added [q3_predict.py](q3_predict.py) loads the unchanged binary using pickle and calls `pipeline.predict_proba([lead])[0, 1]` for:

```json
{"lead_source":"paid_ads","industry":"technology","employment_status":"employed","location":"north_america","number_of_courses_viewed":2,"annual_income":79276.0,"interaction_count":4,"lead_score":0.41}
```

Output:

```json
{"conversion_probability":0.5329944186432507,"rounded":"0.533"}
```

## Q4: actual local API evidence

Started the unchanged `predict:app` using uvicorn on port 9696. Exact request body:

```json
{"lead_source":"organic_search","industry":"technology","employment_status":"employed","location":"europe","number_of_courses_viewed":4,"annual_income":80304.0,"interaction_count":7,"lead_score":0.74}
```

`GET http://localhost:9696/health` returned:

```json
{"status":"ok","model_sha256":"1646bbdcd38d4f044da6b630c5b332c93a314245a8c21929011c42de51f629f1","feature_defaults_sha256":"1694f842b908fac9f53c0cc19be6d91f934befc63af23cc32fefafde69acd0cd"}
```

`POST http://localhost:9696/predict` returned:

```json
{"conversion_probability":0.769799,"conversion":true}
```

Both health hashes matched `model_metadata.json`. Probability bounds and the boolean type passed checks. The official `smoke_test.py` passed its deterministic inference assertions, returning `0.769799`. The unchanged `q6_test.py` passed against this local API and returned the same result; this does not establish Docker execution. Captured HTTP evidence is in [local_api_evidence.json](local_api_evidence.json).

## Q5: official container declaration

```dockerfile
FROM python:3.11.15-slim-bookworm@sha256:d29f48a31a8b408ed19272ca1e7b10ebae13b240a27e862d3d4217c528e2e0c3
```

The Dockerfile also pins uv **0.10.11** by digest and runs `uv sync --locked --no-dev`. This is the container's declared uv version; Q1 records the actual local version.

## Commands executed

PowerShell setup from the repository root (the download loop used the pinned revision and verified every blob):

```powershell
git status --short
Get-Command uv,docker -ErrorAction SilentlyContinue
$revision = 'a395ca7ca995df92d8321daa017f3a1b4425a4a0'
$release = Invoke-RestMethod "https://api.github.com/repos/DataTalksClub/machine-learning-zoomcamp/contents/cohorts/2026/homework/05-deployment?ref=$revision"
New-Item -ItemType Directory -Path 05_deployment -Force
foreach ($file in $release) {
    $path = Join-Path '05_deployment' $file.name
    Invoke-WebRequest -UseBasicParsing -Uri $file.download_url -OutFile $path
    if ((git hash-object --no-filters $path) -ne $file.sha) { throw 'Blob mismatch' }
}
Get-FileHash 05_deployment/pipeline.bin -Algorithm SHA256
New-Item -ItemType Directory -Path .runtime/hw5 -Force
Invoke-WebRequest -UseBasicParsing https://astral.sh/uv/install.ps1 -OutFile .runtime/hw5/install-uv.ps1
$env:UV_UNMANAGED_INSTALL = Join-Path (Get-Location) '.runtime/hw5/uv'
& .runtime/hw5/install-uv.ps1
```

Environment and inference commands (same settings used during verification):

```powershell
$env:UV_PYTHON_INSTALL_DIR = 'C:\Users\nikit\ml-zoomcamp-2026\.runtime\hw5\python'
$env:UV_CACHE_DIR = 'C:\Users\nikit\ml-zoomcamp-2026\.runtime\hw5\cache'
$env:UV_PYTHON_BIN_DIR = 'C:\Users\nikit\ml-zoomcamp-2026\.runtime\hw5\bin'
$env:UV_PROJECT_ENVIRONMENT = 'C:\Users\nikit\ml-zoomcamp-2026\05_deployment\.venv'
Set-Location C:\Users\nikit\ml-zoomcamp-2026\05_deployment
$env:PATH = "$(Resolve-Path ..\.runtime\hw5\uv);$env:PATH"
# uv was invoked via its full relative path during execution; PATH above is equivalent.
uv --version
uv python install 3.11.15
uv sync --locked
uv run --locked python --version
uv run --locked python -c 'import sys,sklearn; print(sys.executable); print(sklearn.__version__)'
uv run --locked python smoke_test.py
uv run --locked python q3_predict.py
uv run --locked uvicorn predict:app --host 0.0.0.0 --port 9696
```

In another terminal while the server was running:

```powershell
Invoke-RestMethod http://localhost:9696/health
$lead = @{lead_source='organic_search'; industry='technology'; employment_status='employed'; location='europe'; number_of_courses_viewed=4; annual_income=80304.0; interaction_count=7; lead_score=0.74}
Invoke-RestMethod http://localhost:9696/predict -Method Post -ContentType 'application/json' -Body ($lead | ConvertTo-Json -Compress)
& ..\.runtime\hw5\uv\uv.exe run --locked python q6_test.py
```

## Q6: errors and unresolved blocker

Attempted from `05_deployment`:

```powershell
docker build -t zoomcamp-model:2026-hw5 .
docker run --rm -p 9696:9696 zoomcamp-model:2026-hw5
```

Both failed with `CommandNotFoundException`: **The term 'docker' is not recognized**. No image was built and no container ran. Container HTTP responses and local/container parity remain unverified.

Diagnosis used `where.exe docker`, `Get-Command docker`, Windows uninstall records, known system and per-user executable paths, Start Menu checks, `Get-Process *docker*`, `Get-Service *docker*`, Docker named-pipe enumeration, and `wsl --list --verbose`. No Docker executable, installed application record, running process/service, or Docker engine pipe was found. The existing `%LOCALAPPDATA%/Docker` contains residual data; its installer log records a February 2, 2026 attempt reporting `No installation found` and relaunching for UAC. The Start Menu folder contains no usable shortcut. WSL lists only a stopped `Ubuntu-24.04` distribution, with no Docker Desktop distribution. Docker Desktop is therefore unavailable on this machine based on these checks.

Initial sandbox network and WSL-access errors were resolved by rerunning the necessary operations with approved access. Installation emitted a benign warning that the isolated Python links directory is outside PATH; `uv run` selected the correct interpreter successfully.

To finish Q6 once Docker Desktop is installed and running, stop the local server to release port 9696, rerun the build/run commands above, then call `/health` and run `uv run --locked python q6_test.py` against the container. Compare both health hashes and `conversion_probability` with Q4. **0.770 is the expected answer, not a container-verified result.**

## Repository hygiene

No files were staged, committed, pushed, or submitted. The Git index was empty. Existing ignore rules cover `.runtime/`, `.venv/`, and `__pycache__/`. The final review checked the untracked Homework 5 files and staged paths for environment files, caches, credentials, and temporary files. Only the root README and the new Homework 5 directory were intentionally changed; the pre-existing modification to `02_regression_homework.ipynb` was preserved. HW1–HW4, their datasets, and the root virtual environment were not modified by this work.
