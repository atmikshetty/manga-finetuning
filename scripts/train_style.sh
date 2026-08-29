#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
: "${SD_SCRIPTS_DIR:?Set SD_SCRIPTS_DIR to a Kohya sd-scripts checkout}"
: "${VENV_DIR:?Set VENV_DIR to the Python virtual environment}"
: "${MODEL_ROOT:?Set MODEL_ROOT}"
: "${DATA_ROOT:?Set DATA_ROOT}"
: "${OUTPUT_ROOT:?Set OUTPUT_ROOT}"
CACHE_ROOT="${CACHE_ROOT:-${REPO_ROOT}/.cache}"
LOG_ROOT="${LOG_ROOT:-${OUTPUT_ROOT}/logs}"
BASE_MODEL="${BASE_MODEL:-${MODEL_ROOT}/base-model.safetensors}"
DATA_DIR="${DATA_DIR:-${DATA_ROOT}/style}"
SAMPLE_PROMPTS="${SAMPLE_PROMPTS:-${REPO_ROOT}/examples/style-prompts.txt}"
ACCELERATE_CONFIG="${ACCELERATE_CONFIG:-${REPO_ROOT}/configs/accelerate.yaml}"
OUT_NAME="${OUT_NAME:-style_lora}"
MAX_STEPS="${MAX_STEPS:-2200}"
BATCH_SIZE="${BATCH_SIZE:-2}"
NETWORK_DIM="${NETWORK_DIM:-32}"
NETWORK_ALPHA="${NETWORK_ALPHA:-16}"
UNET_LR="${UNET_LR:-1e-4}"
TEXT_ENCODER_LR="${TEXT_ENCODER_LR:-5e-5}"
PREDICTION_TYPE="${PREDICTION_TYPE:-epsilon}"
SAMPLE_SAMPLER="${SAMPLE_SAMPLER:-euler_a}"

mkdir -p -- "${OUTPUT_ROOT}" "${LOG_ROOT}" "${CACHE_ROOT}/huggingface" "${CACHE_ROOT}/torch"
export HF_HOME="${CACHE_ROOT}/huggingface"
export HF_HUB_CACHE="${CACHE_ROOT}/huggingface"
export TORCH_HOME="${CACHE_ROOT}/torch"
export PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}"

regularization=(--min_snr_gamma 5 --noise_offset 0.05)
if [[ "${PREDICTION_TYPE}" == "v_prediction" ]]; then
  regularization=(--v_parameterization --zero_terminal_snr --scale_v_pred_loss_like_noise_pred)
  SAMPLE_SAMPLER="${SAMPLE_SAMPLER/euler_a/euler}"
fi

"${VENV_DIR}/bin/accelerate" launch --config_file "${ACCELERATE_CONFIG}" --num_cpu_threads_per_process 8 \
  "${SD_SCRIPTS_DIR}/sdxl_train_network.py" \
  --pretrained_model_name_or_path "${BASE_MODEL}" --train_data_dir "${DATA_DIR}" \
  --output_dir "${OUTPUT_ROOT}" --output_name "${OUT_NAME}" --logging_dir "${LOG_ROOT}" \
  --resolution 1024,1024 --enable_bucket --min_bucket_reso 512 --max_bucket_reso 1536 --bucket_reso_steps 64 \
  --network_module networks.lora --network_dim "${NETWORK_DIM}" --network_alpha "${NETWORK_ALPHA}" \
  --train_batch_size "${BATCH_SIZE}" --max_train_steps "${MAX_STEPS}" --gradient_checkpointing \
  --mixed_precision bf16 --save_precision bf16 --no_half_vae --optimizer_type AdamW8bit \
  --learning_rate "${UNET_LR}" --unet_lr "${UNET_LR}" --text_encoder_lr "${TEXT_ENCODER_LR}" \
  --lr_scheduler cosine --lr_warmup_steps 100 --cache_latents --cache_latents_to_disk \
  --caption_extension .txt --shuffle_caption --keep_tokens 1 "${regularization[@]}" --sdpa \
  --save_every_n_steps 300 --sample_every_n_steps 300 --sample_prompts "${SAMPLE_PROMPTS}" \
  --sample_sampler "${SAMPLE_SAMPLER}" --save_model_as safetensors --max_data_loader_n_workers 8 \
  --persistent_data_loader_workers --seed 42
