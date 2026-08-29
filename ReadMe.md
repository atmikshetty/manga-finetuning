# Manga Finetuning

Portable, auditable tools for preparing lawfully sourced panel datasets,
training style and character SDXL LoRAs with Kohya, and reviewing checkpoints.

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
