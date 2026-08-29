#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
: "${SD_SCRIPTS_DIR:?Set SD_SCRIPTS_DIR to a Kohya sd-scripts checkout}"
: "${VENV_DIR:?Set VENV_DIR}"
: "${MODEL_ROOT:?Set MODEL_ROOT}"
: "${DATA_ROOT:?Set DATA_ROOT}"
: "${OUTPUT_ROOT:?Set OUTPUT_ROOT}"
: "${TRIGGER:?Set TRIGGER to the character token}"
CACHE_ROOT="${CACHE_ROOT:-${REPO_ROOT}/.cache}"
DATA_DIR="${DATA_DIR:-${DATA_ROOT}/character}"
SAMPLE_PROMPTS="${SAMPLE_PROMPTS:-${REPO_ROOT}/examples/character-prompts.txt}"

export BASE_MODEL="${BASE_MODEL:-${MODEL_ROOT}/base-vpred-model.safetensors}"
export DATA_DIR SAMPLE_PROMPTS
export OUT_NAME="${OUT_NAME:-${TRIGGER}_character_vpred}"
export MAX_STEPS="${MAX_STEPS:-1800}"
export BATCH_SIZE="${BATCH_SIZE:-2}"
export NETWORK_DIM="${NETWORK_DIM:-64}"
export NETWORK_ALPHA="${NETWORK_ALPHA:-32}"
export UNET_LR="${UNET_LR:-3e-4}"
export TEXT_ENCODER_LR="${TEXT_ENCODER_LR:-3e-5}"
export PREDICTION_TYPE="v_prediction"
export SAMPLE_SAMPLER="euler"

exec "${REPO_ROOT}/scripts/train_style.sh"
