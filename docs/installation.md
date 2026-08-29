# Installation

## Core

Python 3.11 or newer is required.

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

Install `.[panel]` only on the machine running detection, `.[eval]` on the GPU
evaluation machine, and `.[dev]` for contributors. GPU packages are not core
dependencies and no lockfile pretends to cover platform-specific CUDA wheels.

Kohya `sd-scripts` is external. Clone it separately, check out a reviewed
revision, create its environment according to that revision, then set
`SD_SCRIPTS_DIR` and `VENV_DIR`.
