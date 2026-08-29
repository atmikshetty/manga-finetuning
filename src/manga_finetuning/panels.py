"""Pure panel geometry, crop, whiteout, layout, and resume helpers."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

Box = list[int]
PANEL_KEYS = ("panels", "panel", "panel_boxes", "panel_bboxes")
TEXT_KEYS = ("texts", "text", "text_boxes", "text_bboxes", "dialogue", "balloons")
SPREAD_ASPECT = 1.2
SPREAD_KEEP_FRACTION = 0.25
IMAGE_EXTENSIONS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".webp"}


def first_present(result: Mapping[str, Any], candidates: Iterable[str]) -> Any:
    return next((result[key] for key in candidates if key in result), None)


def to_box_list(raw: Any, width: int, height: int) -> list[Box]:
    """Coerce detector rows to ordered, clamped pixel boxes."""
    if hasattr(raw, "detach"):
        raw = raw.detach().cpu()
    if hasattr(raw, "tolist"):
        raw = raw.tolist()
    if not isinstance(raw, (list, tuple)):
        return []
    boxes: list[Box] = []
    for row in raw:
        if hasattr(row, "detach"):
            row = row.detach().cpu()
        if hasattr(row, "tolist"):
            row = row.tolist()
        if not isinstance(row, (list, tuple)) or len(row) < 4:
            continue
        try:
            values = [float(value) for value in row[:4]]
        except (TypeError, ValueError):
            continue
        x1, y1, x2, y2 = values
        if max(map(abs, values)) <= 1.0:
            x1, x2, y1, y2 = x1 * width, x2 * width, y1 * height, y2 * height
        xa, xb = sorted((x1, x2))
        ya, yb = sorted((y1, y2))
        box = [
            round(max(0, min(width, xa))),
            round(max(0, min(height, ya))),
            round(max(0, min(width, xb))),
            round(max(0, min(height, yb))),
        ]
        if box[2] > box[0] and box[3] > box[1]:
            boxes.append(box)
    return boxes


def extract_boxes(
    result: Mapping[str, Any], width: int, height: int
) -> tuple[list[Box], list[Box]]:
    return (
        to_box_list(first_present(result, PANEL_KEYS), width, height),
        to_box_list(first_present(result, TEXT_KEYS), width, height),
    )


def intersection(left: Sequence[int], right: Sequence[int]) -> Box | None:
    box = [
        max(left[0], right[0]),
        max(left[1], right[1]),
        min(left[2], right[2]),
        min(left[3], right[3]),
    ]
    return box if box[2] > box[0] and box[3] > box[1] else None


def normalize_boxes(
    boxes: Iterable[Sequence[float]], width: float, height: float
) -> list[list[float]]:
    if width <= 0 or height <= 0:
        return []
    return [
        [round(x1 / width, 4), round(y1 / height, 4), round(x2 / width, 4), round(y2 / height, 4)]
        for x1, y1, x2, y2, *_ in boxes
    ]


def clip_to_half(boxes: Iterable[Sequence[float]], start: float, end: float) -> list[list[float]]:
    clipped = []
    for x1, y1, x2, y2, *_ in boxes:
        ix1, ix2 = max(x1, start), min(x2, end)
        area = (x2 - x1) * (y2 - y1)
        if ix2 > ix1 and area > 0 and ((ix2 - ix1) * (y2 - y1)) / area >= SPREAD_KEEP_FRACTION:
            clipped.append([ix1 - start, y1, ix2 - start, y2])
    return clipped


def layout_records(
    page: str, source: str, width: int, height: int, panels: list[Box], texts: list[Box]
) -> list[dict[str, Any]]:
    if not panels:
        return []
    common = {"page": page, "source": source}
    if height <= 0 or width / height < SPREAD_ASPECT:
        return [
            {
                **common,
                "w": width,
                "h": height,
                "panels": normalize_boxes(panels, width, height),
                "texts": normalize_boxes(texts, width, height),
                "n_panels": len(panels),
                "spread": False,
            }
        ]
    midpoint = width / 2
    records = []
    for side, (start, end) in (("right", (midpoint, width)), ("left", (0.0, midpoint))):
        half_panels = clip_to_half(panels, start, end)
        if half_panels:
            half_width = end - start
            records.append(
                {
                    **common,
                    "w": round(half_width),
                    "h": height,
                    "panels": normalize_boxes(half_panels, half_width, height),
                    "texts": normalize_boxes(clip_to_half(texts, start, end), half_width, height),
                    "n_panels": len(half_panels),
                    "spread": True,
                    "side": side,
                }
            )
    return records


def process_page(
    original: Any,
    panels: list[Box],
    texts: list[Box],
    *,
    min_panel_size: int,
    text_padding: int,
    max_text_coverage: float,
) -> tuple[list[tuple[int, Any]], dict[str, int]]:
    crops = []
    stats = {
        "panels_detected": len(panels),
        "text_boxes_total": len(texts),
        "text_boxes_removed": 0,
        "skipped_small": 0,
        "skipped_mostly_text": 0,
    }
    for index, panel in enumerate(panels):
        px1, py1, px2, py2 = panel
        width, height = px2 - px1, py2 - py1
        if min(width, height) < min_panel_size:
            stats["skipped_small"] += 1
            continue
        crop = original.crop(tuple(panel)).copy()
        removed = text_area = 0
        for text in texts:
            overlap = intersection(panel, text)
            if overlap is None:
                continue
            local = (
                max(0, overlap[0] - px1 - text_padding),
                max(0, overlap[1] - py1 - text_padding),
                min(width, overlap[2] - px1 + text_padding),
                min(height, overlap[3] - py1 + text_padding),
            )
            if local[2] <= local[0] or local[3] <= local[1]:
                continue
            crop.paste((255, 255, 255), local)
            text_area += (local[2] - local[0]) * (local[3] - local[1])
            removed += 1
        if width * height and text_area / (width * height) > max_text_coverage:
            stats["skipped_mostly_text"] += 1
            continue
        stats["text_boxes_removed"] += removed
        crops.append((index, crop))
    return crops, stats


def collect_pages(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and not path.name.startswith(".")
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def output_directory(page: Path, input_dir: Path, output_dir: Path) -> Path:
    return output_dir / page.parent.relative_to(input_dir)


def done_marker(page: Path, input_dir: Path, output_dir: Path) -> Path:
    return output_directory(page, input_dir, output_dir) / f".{page.stem}.panels.done"


def load_dumped_pages(path: Path | None) -> set[str]:
    if path is None or not path.exists():
        return set()
    completed = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            completed.add(json.loads(line)["page"])
        except (KeyError, TypeError, ValueError):
            continue
    return completed
