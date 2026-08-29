# Model Publishing

Publish weights only when base-model terms, dataset rights, consent, and local
law permit it. Complete the model-card template and disclose base model ID,
immutable revision, local hash, dataset version, trigger, training config,
limitations, evaluation, and memorization checks.

Use `safetensors`, calculate SHA-256, scan metadata for personal paths, and test
the downloaded artifact in a clean environment. Do not bundle source images,
samples without publication rights, secrets, or logs. Apply a model license
separately: Apache-2.0 on this code does not transfer to weights.

Consider gated access, an acceptable-use policy, and a documented takedown
process. Preserve prior hashes and release notes when replacing artifacts.
