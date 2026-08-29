# Hugging Face Layout

Suggested model repository:

```text
README.md
LICENSE.model
model.safetensors
training-config.toml
artifact-manifest.json
evaluation/
  metrics.json
```

Suggested dataset repository, only when redistribution is authorized:

```text
README.md
LICENSE.dataset
data/
  train-00000-of-00001.parquet
dataset-manifest.json
provenance.json
```

Hugging Face card YAML must use real metadata before publication. Keep code,
model, and dataset licenses distinct. Pin base models by revision rather than a
mutable branch and include hashes for files obtained outside the Hub.
