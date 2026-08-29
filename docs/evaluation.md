# Evaluation

Use fixed prompts, negative prompt, dimensions, seed, steps, scheduler, and base
model while sweeping checkpoint and scale. Include portraits, full bodies,
interactions, action, scenery, and an intentionally off-distribution prompt.

```bash
manga-eval-checkpoints --base "$MODEL_ROOT/base-vpred.safetensors" \
  --lora-dir "$OUTPUT_ROOT" --output-dir "$OUTPUT_ROOT/evaluation" \
  --trigger style_token --checkpoints 600,900,1200 --scales 0.6,0.75,0.9
```

For v-prediction checkpoints the evaluator forces `prediction_type` to
`v_prediction`, enables zero-terminal-SNR rescaling, uses plain Euler, and sets
guidance rescale. Select by human review: prompt adherence, memorization,
trigger separation, style, then anatomy. Image statistics are descriptive and
must not become a single pass/fail score.
