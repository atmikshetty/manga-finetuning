# Pipeline

1. Establish rights and freeze a source inventory outside Git.
2. Extract panels and optionally normalized layout JSONL with a pinned detector.
3. White out detected text and inspect misses manually.
4. Filter dimensions, normalize RGB/PNG, and deduplicate by dHash.
5. Produce sidecar captions and apply a unique trigger idempotently.
6. Validate image/caption pairs and create artifact/run manifests.
7. Train with the matching epsilon or v-prediction wrapper settings.
8. Render fixed prompts across intermediate checkpoints and LoRA scales.
9. Review prompt adherence, memorization, trigger behavior, anatomy, and style.
10. Publish only when every artifact has its own provenance and license.

Each stage writes to a separate directory. Never mutate source data. Preserve
manifests and configs with experiment records, but keep copyrighted artifacts
and machine paths out of Git.
