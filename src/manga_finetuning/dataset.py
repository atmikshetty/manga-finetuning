"""Prepare deduplicated, aspect-preserving image datasets for Kohya."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .hashing import HashIndex, difference_hash

IMAGE_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".webp"}


@dataclass
class PreparationStats:
    candidates: int = 0
    kept: int = 0
    corrupt: int = 0
    duplicate: int = 0
    too_small: int = 0


def collect_images(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def prepare_dataset(
    input_dir: Path,
    output_dir: Path,
    *,
    min_side: int = 512,
    max_side: int = 1152,
    duplicate_threshold: int = 8,
    max_images: int | None = None,
) -> PreparationStats:
    """Validate, deduplicate, resize, and normalize images as numbered PNG files."""
    if min_side < 1 or max_side < min_side:
        raise ValueError("require 1 <= min_side <= max_side")
    if input_dir.resolve() == output_dir.resolve():
        raise ValueError("input and output directories must differ")
    from PIL import Image, ImageFile

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    files = collect_images(input_dir)
    stats = PreparationStats(candidates=len(files))
    hashes = HashIndex(duplicate_threshold)
    output_dir.mkdir(parents=True, exist_ok=True)
    for path in files:
        if max_images is not None and stats.kept >= max_images:
            break
        try:
            with Image.open(path) as source:
                source.load()
                image = source.convert("RGB")
        except (OSError, ValueError):
            stats.corrupt += 1
            continue
        width, height = image.size
        if min(width, height) < min_side:
            stats.too_small += 1
            continue
        if not hashes.add_if_unique(difference_hash(image)):
            stats.duplicate += 1
            continue
        longest = max(width, height)
        if longest > max_side:
            scale = max_side / longest
            image = image.resize(
                (max(1, int(width * scale)), max(1, int(height * scale))),
                Image.Resampling.LANCZOS,
            )
        image.save(output_dir / f"panel_{stats.kept:05d}.png", format="PNG")
        stats.kept += 1
    return stats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--min-side", type=int, default=512)
    parser.add_argument("--max-side", type=int, default=1152)
    parser.add_argument("--duplicate-threshold", type=int, default=8)
    parser.add_argument("--max-images", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    stats = prepare_dataset(
        args.input_dir,
        args.output_dir,
        min_side=args.min_side,
        max_side=args.max_side,
        duplicate_threshold=args.duplicate_threshold,
        max_images=args.max_images,
    )
    print(json.dumps(asdict(stats), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
