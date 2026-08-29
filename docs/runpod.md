# RunPod Setup

Choose an image compatible with the required CUDA/PyTorch versions and use a
persistent volume for models, datasets, caches, and outputs. Clone this project
and a reviewed Kohya revision into separate directories. Never bake credentials
into an image or startup script.

Set the path variables from `.env.example`, install only the relevant optional
extras, and run a tiny generated-data smoke test before uploading authorized
data. Pin the panel detector `--revision` because it executes remote code.

Restrict network exposure, use short-lived provider secrets, and remove shell
history and caches before releasing a volume. Download manifests and configs
before terminating the pod. Provider IDs and personal volume paths belong in
private operational records, not this repository.
