# Manga Finetuning

Portable, auditable tools for preparing lawfully sourced panel datasets,
training style and character SDXL LoRAs with Kohya, and reviewing checkpoints.

## Showcase

Generated examples from the
[Manga Finetuning LoRA Collection](https://huggingface.co/collections/sleephashira/manga-finetuning-lora-collection-6a934c160ee93453d004b9c0).

**Kimetsu color style** — trigger `dsmanga`, Illustrious XL — [model](https://huggingface.co/sleephashira/kimetsu-color-illustrious-xl-lora)

<img src="https://huggingface.co/sleephashira/kimetsu-color-illustrious-xl-lora/resolve/main/examples/showcase.png" alt="Color manga panel of a water dragon technique rendered by the Kimetsu color LoRA" width="760">

**OPM Murata monochrome style** — trigger `mrtmanga`, Illustrious XL — [model](https://huggingface.co/sleephashira/opm-murata-illustrious-xl-lora)

<img src="https://huggingface.co/sleephashira/opm-murata-illustrious-xl-lora/resolve/main/examples/showcase.png" alt="Monochrome manga impact panel with dense speed lines rendered by the OPM Murata LoRA" width="760">

**Bleach and JoJo multistyle** — triggers `blcmanga`, `blccolor`, `jjbamanga`, NoobAI XL V-Pred — [model](https://huggingface.co/sleephashira/bleach-jojo-multistyle-noobai-xl-vpred-lora)

<img src="https://huggingface.co/sleephashira/bleach-jojo-multistyle-noobai-xl-vpred-lora/resolve/main/examples/showcase.png" alt="Composed color manga page mixing the three multistyle registers" width="560">

**Rei character** — trigger `reichar`, NoobAI XL V-Pred — [model](https://huggingface.co/sleephashira/rei-character-noobai-xl-vpred-lora)

<img src="https://huggingface.co/sleephashira/rei-character-noobai-xl-vpred-lora/resolve/main/examples/showcase.png" alt="Monochrome character portrait of Rei rendered by the character LoRA" width="560">

> [!IMPORTANT]
> Apache-2.0 covers code and documentation only. It does **not** license any
> dataset, model weight, manga page, illustration, or generated artwork. This
> repository ships none of those artifacts. You must document separate rights
> and provenance for every input and output.

## Status

The curated pipeline is alpha quality: core transforms are tested, but GPU
model compatibility must be verified for each pinned upstream revision.

## Scope

Included: panel extraction and text whiteout, dHash dataset preparation,
trigger captions, character camera captions, style/character Kohya wrappers,
artifact manifests, and checkpoint evaluation.

Excluded: image acquisition, raw scans, scraping, dialogue, page composition,
generation applications, galleries, archives, logs, datasets, and weights.

## Quickstart

```bash
python3.11 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest

manga-prepare-dataset --input-dir /data/panels --output-dir /data/kohya/10_style
manga-apply-trigger /data/kohya/10_style --trigger style_token
manga-eval-checkpoints --base /models/base.safetensors \
  --lora-dir /outputs --output-dir /outputs/eval --trigger style_token --dry-run
```

Panel extraction requires `.[panel]`; GPU evaluation requires `.[eval]`.
Training itself uses a separately installed, revision-pinned Kohya
`sd-scripts` checkout.

## Architecture

The package follows a functional-core/imperative-shell design. Geometry,
caption, hash, checkpoint, and manifest logic lives under
`src/manga_finetuning`; CLI entry points perform filesystem or optional GPU
work. Shell wrappers discover the repository root and take all machine paths
from environment variables.

See [installation](docs/installation.md), [pipeline](docs/pipeline.md),
[training](docs/training.md), and [migration scope](docs/migration-scope.md).
