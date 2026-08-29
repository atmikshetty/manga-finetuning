# Training

Copy `.env.example` values into your shell or private environment manager. The
wrappers require `SD_SCRIPTS_DIR`, `VENV_DIR`, `MODEL_ROOT`, `DATA_ROOT`, and
`OUTPUT_ROOT`; `CACHE_ROOT` is optional.

```bash
PREDICTION_TYPE=epsilon OUT_NAME=style-v1 scripts/train_style.sh
PREDICTION_TYPE=v_prediction BASE_MODEL="$MODEL_ROOT/base-vpred.safetensors" \
  OUT_NAME=style-vpred-v1 scripts/train_style.sh
TRIGGER=person_token scripts/train_character.sh
```

V-prediction runs retain `--v_parameterization`, `--zero_terminal_snr`, and
`--scale_v_pred_loss_like_noise_pred`, omit epsilon noise offset, and use Euler
for samples. Do not simplify these away: incorrect scheduler semantics can make
a healthy checkpoint appear as noise or flat gray output.

Intermediate checkpoints matter. The final checkpoint often overfits before
training ends, especially for small character sets.
