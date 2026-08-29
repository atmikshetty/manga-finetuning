---
license: <MODEL_LICENSE>
base_model: <BASE_MODEL_ID>
base_model_revision: <IMMUTABLE_REVISION>
pipeline_tag: text-to-image
tags:
  - lora
  - sdxl
---

# <Model Name>

## Provenance

- Base model: `<ID>` at `<REVISION>`, SHA-256 `<HASH>`
- Training code revision: `<REVISION>`
- Dataset: `<DATASET_ID_AND_VERSION>` under `<DATASET_LICENSE>`
- Trigger: `<TRIGGER>`
- Config and run manifest: `<LINKS_OR_HASHES>`

## Intended Use

<PERMITTED_AND_OUT_OF_SCOPE_USES>

## Training

<PREDICTION_TYPE, ZTSNR, STEPS, RANK, ALPHA, LR, SEED, HARDWARE>

## Evaluation

<PROMPT_ADHERENCE, TRIGGER_SEPARATION, HUMAN_REVIEW, METRICS>

## Memorization Checks

<NEAREST_NEIGHBOR_METHOD, PROMPTS, REVIEW_RESULT, LIMITATIONS>

## Limitations and Risks

<BIAS, ANATOMY, TEXT, STYLE_IMITATION, MISUSE, DATA_LIMITATIONS>

## License

Weights use `<MODEL_LICENSE>`. Apache-2.0 for the training code does not cover
the weights, dataset, source artwork, or generated images.
