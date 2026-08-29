# Reproducibility

Record the Git revision, Python version, OS/CUDA stack, exact base model
repository and revision, local model SHA-256, detector revision, Kohya revision,
dataset manifest SHA-256, config SHA-256, seed, command, and output checksums.

```bash
manga-artifact-manifest /data/dataset-v1 --output records/dataset-v1.json
manga-run-manifest --config configs/style-vpred.toml --output records/run.json
```

Run manifests intentionally omit environment variables because they commonly
contain secrets and personal paths. Store machine-specific paths in a private
run system. Deterministic seeds improve comparison but do not guarantee
bit-for-bit CUDA reproducibility across hardware and library versions.
