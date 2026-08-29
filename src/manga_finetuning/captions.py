"""Normalize tag captions and pin a trigger token at the front."""

from __future__ import annotations

import argparse
from pathlib import Path

DROP_ALWAYS = frozenset(
    {"comic", "english text", "photo background", "speech bubble", "traditional media"}
)
MONOCHROME_TAGS = frozenset({"greyscale", "monochrome"})


def parse_tags(text: str) -> list[str]:
    return [tag.strip() for tag in text.replace("\n", ",").split(",") if tag.strip()]


def process_caption(text: str, trigger: str, *, color: bool = False) -> str:
    """Return a deterministic caption; repeated application is idempotent."""
    trigger = trigger.strip()
    if not trigger or "," in trigger or "\n" in trigger:
        raise ValueError("trigger must be one non-empty tag")
    anchors = [] if color else ["monochrome", "greyscale"]
    dropped = DROP_ALWAYS if color else DROP_ALWAYS | MONOCHROME_TAGS
    prefix = {trigger.casefold(), *(anchor.casefold() for anchor in anchors)}
    seen: set[str] = set()
    tail: list[str] = []
    for tag in parse_tags(text):
        key = tag.casefold()
        if key in dropped or key in prefix or key in seen:
            continue
        seen.add(key)
        tail.append(tag)
    return ", ".join([trigger, *anchors, *tail])


def process_directory(directory: Path, trigger: str, *, color: bool = False) -> int:
    count = 0
    for path in sorted(directory.glob("*.txt")):
        updated = process_caption(path.read_text(encoding="utf-8"), trigger, color=color)
        path.write_text(updated + "\n", encoding="utf-8")
        count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--color", action="store_true")
    args = parser.parse_args(argv)
    if not args.directory.is_dir():
        parser.error(f"caption directory does not exist: {args.directory}")
    count = process_directory(args.directory, args.trigger, color=args.color)
    print(f"processed {count} captions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
