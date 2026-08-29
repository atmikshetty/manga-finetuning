"""Build and validate a camera-captioned Kohya character dataset."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

AZIMUTH_TAGS = {
    "front view": "facing viewer",
    "front-right quarter view": "three-quarter view",
    "right side view": "from side, profile",
    "back-right quarter view": "from behind",
    "back view": "from behind",
    "back-left quarter view": "from behind",
    "left side view": "from side, profile",
    "front-left quarter view": "three-quarter view",
}
ELEVATION_TAGS = {
    "low-angle shot": "from below",
    "eye-level shot": "",
    "elevated shot": "from above",
    "high-angle shot": "from above",
}
DISTANCE_TAGS = {
    "close-up": "portrait, close-up",
    "medium shot": "upper body",
    "wide shot": "full body",
}
IMAGE_EXTENSIONS = {".jpeg", ".jpg", ".png", ".webp"}


def camera_caption(view: dict[str, Any], trigger: str, extra: str = "") -> str:
    """Caption variable camera attributes while leaving identity bound to trigger."""
    required = {"azimuth", "elevation", "distance"}
    missing = required - view.keys()
    if missing:
        raise ValueError(f"view missing fields: {', '.join(sorted(missing))}")
    parts = [
        trigger,
        AZIMUTH_TAGS.get(view["azimuth"], ""),
        ELEVATION_TAGS.get(view["elevation"], ""),
        DISTANCE_TAGS.get(view["distance"], ""),
        extra.strip(),
    ]
    return ", ".join(part for part in parts if part)


def load_views(manifest: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    views = payload.get("views")
    if not isinstance(views, list):
        raise ValueError("manifest must contain a views list")
    indexed = {}
    for view in views:
        if not isinstance(view, dict) or not isinstance(view.get("file"), str):
            raise ValueError("every view must contain a string file field")
        if Path(view["file"]).name != view["file"]:
            raise ValueError("view filenames must not contain paths")
        if view["file"] in indexed:
            raise ValueError(f"duplicate manifest view: {view['file']}")
        indexed[view["file"]] = view
    return indexed


def prepare_character_dataset(
    images: Path, manifest: Path, output: Path, trigger: str, *, repeats: int = 10, extra: str = ""
) -> Path:
    if repeats < 1 or not trigger.strip() or any(char in trigger for char in ",\n/"):
        raise ValueError("repeats must be positive and trigger must be one safe tag")
    files = sorted(
        path
        for path in images.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not files:
        raise ValueError(f"no supported images in {images}")
    views = load_views(manifest)
    missing = [path.name for path in files if path.name not in views]
    if missing:
        raise ValueError(f"images missing manifest views: {', '.join(missing)}")
    destination = output / f"{repeats}_{trigger}"
    destination.mkdir(parents=True, exist_ok=True)
    for image in files:
        shutil.copy2(image, destination / image.name)
        caption = camera_caption(views[image.name], trigger, extra)
        (destination / f"{image.stem}.txt").write_text(caption + "\n", encoding="utf-8")
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--extra", default="")
    args = parser.parse_args(argv)
    destination = prepare_character_dataset(
        args.images,
        args.manifest,
        args.output,
        args.trigger,
        repeats=args.repeats,
        extra=args.extra,
    )
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
