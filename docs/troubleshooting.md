# Troubleshooting

## Gray or noisy v-prediction samples

Confirm the base header, `PREDICTION_TYPE=v_prediction`, all three Kohya v-pred
flags, plain Euler sampling, zero-terminal-SNR, and evaluation guidance rescale.

## Duplicate panels remain

dHash detects visually similar structure, not semantic duplication. Lower the
threshold for fewer false positives or add an audited scalable index. Always
review removals before deleting source records.

## Missing or excessive whiteout

Inspect detector boxes and adjust text padding. A box that intersects a panel
is translated into crop-local coordinates; excessive text coverage rejects the
crop. Keep originals immutable and review outputs manually.

## Resume skipped unexpected pages

Crop mode uses per-page `.panels.done` markers. Layout-only mode uses page names
already present in JSONL. Remove only the specific derived marker after
verifying outputs; never alter source pages.
