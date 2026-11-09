#!/usr/bin/env bash
# Source from any working directory. Does not modify shell startup files.
HRL_PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export HRL_PROJECT_ROOT
export CONDA_PKGS_DIRS="$HRL_PROJECT_ROOT/.cache/conda-pkgs"
export CONDA_ENVS_PATH="$HRL_PROJECT_ROOT/envs"
export PIP_CACHE_DIR="$HRL_PROJECT_ROOT/.cache/pip"
export XDG_CACHE_HOME="$HRL_PROJECT_ROOT/.cache"
export HF_HOME="$HRL_PROJECT_ROOT/.cache/huggingface"
export TORCH_HOME="$HRL_PROJECT_ROOT/.cache/torch"
export CUDA_CACHE_PATH="$HRL_PROJECT_ROOT/.cache/cuda"
export PYTHONPYCACHEPREFIX="$HRL_PROJECT_ROOT/.cache/pycache"
export PYTHONNOUSERSITE=1
export TMPDIR="$HRL_PROJECT_ROOT/.cache/tmp"
mkdir -p "$TMPDIR" "$HRL_PROJECT_ROOT/logs"
