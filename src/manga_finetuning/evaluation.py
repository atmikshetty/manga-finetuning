"""Plan and render human-reviewed LoRA checkpoint evaluation grids."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .checkpoints import checkpoint_is_vpred, discover_checkpoints

QUALITY = "masterpiece, best quality, very aesthetic, absurdres"
MONOCHROME = "monochrome, greyscale, traditional media"
NEGATIVE = (
    "worst quality, low quality, lowres, jpeg artifacts, blurry, bad anatomy, bad hands, "
    "watermark, signature, comic, 4koma, multiple views, speech bubble, text"
)
PROMPTS = (
    ("portrait", "solo, portrait, close-up, looking at viewer"),
    ("full-body", "solo, full body, standing, wide shot"),
    ("interaction", "two people, upper body, facing each other, talking"),
    ("action", "solo, dynamic pose, from below, foreshortening"),
    ("scenery", "no humans, scenery, cityscape, wide shot"),
    ("off-style", "solo, chibi, pastel colors, flower field, smiling"),
)


def build_prompt(trigger: str, body: str, *, monochrome: bool = True) -> str:
    return ", ".join(
        part for part in (QUALITY, trigger, MONOCHROME if monochrome else "", body) if part
    )


def load_pipeline(base: Path, device: str):
    import torch
    from diffusers import EulerDiscreteScheduler, StableDiffusionXLPipeline

    pipeline = StableDiffusionXLPipeline.from_single_file(
        base, torch_dtype=torch.float16, add_watermarker=False
    )
    is_vpred = checkpoint_is_vpred(base)
    config = dict(pipeline.scheduler.config)
    if is_vpred:
        config["prediction_type"] = "v_prediction"
        config["rescale_betas_zero_snr"] = True
    pipeline.scheduler = EulerDiscreteScheduler.from_config(config)
    pipeline.to(device)
    return pipeline, is_vpred


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--lora-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--checkpoints", default="")
    parser.add_argument("--scales", default="0.6,0.75,0.9")
    parser.add_argument("--color", action="store_true")
    parser.add_argument("--steps", type=int, default=28)
    parser.add_argument("--guidance", type=float, default=5.0)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--width", type=int, default=832)
    parser.add_argument("--height", type=int, default=1216)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    wanted = {int(value) for value in args.checkpoints.split(",") if value.strip()} or None
    checkpoints = discover_checkpoints(args.lora_dir, wanted)
    scales = [float(value) for value in args.scales.split(",") if value.strip()]
    plan = [
        {"step": step, "checkpoint": str(path), "scale": scale, "prompt": name}
        for step, path in checkpoints
        for scale in scales
        for name, _ in PROMPTS
    ]
    print(json.dumps(plan, indent=2))
    if args.dry_run:
        return 0
    if not checkpoints:
        raise SystemExit("no matching checkpoints found")
    import torch

    pipeline, is_vpred = load_pipeline(args.base, args.device)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata = []
    for step, checkpoint in checkpoints:
        for scale in scales:
            try:
                pipeline.unload_lora_weights()
            except AttributeError:
                pass
            pipeline.load_lora_weights(checkpoint)
            pipeline.set_adapters(pipeline.get_active_adapters(), adapter_weights=[scale])
            for name, body in PROMPTS:
                generator = torch.Generator(args.device).manual_seed(args.seed)
                kwargs = {
                    "prompt": build_prompt(args.trigger, body, monochrome=not args.color),
                    "negative_prompt": NEGATIVE,
                    "num_inference_steps": args.steps,
                    "guidance_scale": args.guidance,
                    "width": args.width,
                    "height": args.height,
                    "generator": generator,
                    "negative_original_size": (512, 512),
                    "negative_target_size": (1024, 1024),
                }
                if is_vpred:
                    kwargs["guidance_rescale"] = 0.7
                image = pipeline(**kwargs).images[0]
                filename = f"step{step:06d}_scale{scale:g}_{name}.png"
                image.save(args.output_dir / filename)
                metadata.append(
                    {
                        "file": filename,
                        "step": step,
                        "scale": scale,
                        "prompt": name,
                        "seed": args.seed,
                    }
                )
    (args.output_dir / "evaluation.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "Review prompt adherence, memorization, trigger separation, style, and anatomy by eye; "
        "do not select using a single scalar metric."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
