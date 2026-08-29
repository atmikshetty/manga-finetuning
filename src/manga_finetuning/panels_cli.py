"""Extract text-free panels and optional layout JSONL using a trusted Magi model."""

from __future__ import annotations

import argparse
import json
from contextlib import nullcontext
from datetime import UTC, datetime
from pathlib import Path

from .panels import (
    collect_pages,
    done_marker,
    extract_boxes,
    layout_records,
    load_dumped_pages,
    output_directory,
    process_page,
)

DEFAULT_MODEL = "ragavsachdeva/magi"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--layout-jsonl", type=Path)
    parser.add_argument("--layout-only", action="store_true")
    parser.add_argument("--source", help="lawful source identifier stored in layout records")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--revision", help="pin trusted remote model code to a commit")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--min-panel-size", type=int, default=300)
    parser.add_argument("--text-padding", type=int, default=4)
    parser.add_argument("--max-text-coverage", type=float, default=0.5)
    parser.add_argument("--limit", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.input_dir.is_dir():
        raise SystemExit(f"input directory not found: {args.input_dir}")
    if args.layout_only and not args.layout_jsonl:
        raise SystemExit("--layout-only requires --layout-jsonl")
    if not args.layout_only and not args.output_dir:
        raise SystemExit("--output-dir is required unless --layout-only is used")

    import numpy as np
    import torch
    from PIL import Image, ImageFile
    from transformers import AutoModel

    if args.device.startswith("cuda") and not torch.cuda.is_available():
        raise SystemExit("CUDA requested but unavailable; pass --device cpu for a slow fallback")
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    pages = collect_pages(args.input_dir)
    if args.limit is not None:
        pages = pages[: args.limit]
    dumped = load_dumped_pages(args.layout_jsonl) if args.layout_only else set()
    pages = [
        page
        for page in pages
        if str(page) not in dumped
        and (args.layout_only or not done_marker(page, args.input_dir, args.output_dir).exists())
    ]

    model = (
        AutoModel.from_pretrained(args.model, revision=args.revision, trust_remote_code=True)
        .to(args.device)
        .eval()
    )
    source = args.source or args.input_dir.name
    if args.layout_jsonl:
        args.layout_jsonl.parent.mkdir(parents=True, exist_ok=True)
    layout_handle = (
        args.layout_jsonl.open("a", encoding="utf-8") if args.layout_jsonl else nullcontext(None)
    )
    with layout_handle as layout_file:
        for start in range(0, len(pages), args.batch_size):
            batch = pages[start : start + args.batch_size]
            originals = []
            arrays = []
            for path in batch:
                with Image.open(path) as opened:
                    opened.load()
                    original = opened.convert("RGB")
                originals.append(original)
                arrays.append(np.asarray(original.convert("L").convert("RGB")))
            with (
                torch.no_grad(),
                (
                    torch.autocast("cuda", dtype=torch.float16)
                    if args.fp16 and args.device.startswith("cuda")
                    else nullcontext()
                ),
            ):
                results = model.predict_detections_and_associations(arrays)
            for path, original, result in zip(batch, originals, results, strict=True):
                panels, texts = extract_boxes(result, *original.size)
                if layout_file:
                    for record in layout_records(str(path), source, *original.size, panels, texts):
                        layout_file.write(json.dumps(record, sort_keys=True) + "\n")
                    layout_file.flush()
                if args.layout_only:
                    continue
                output = output_directory(path, args.input_dir, args.output_dir)
                output.mkdir(parents=True, exist_ok=True)
                crops, _ = process_page(
                    original,
                    panels,
                    texts,
                    min_panel_size=args.min_panel_size,
                    text_padding=args.text_padding,
                    max_text_coverage=args.max_text_coverage,
                )
                for index, crop in crops:
                    crop.save(output / f"{path.stem}-panel-{index:02d}.png", "PNG")
                done_marker(path, args.input_dir, args.output_dir).write_text(
                    datetime.now(UTC).isoformat(), encoding="utf-8"
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
