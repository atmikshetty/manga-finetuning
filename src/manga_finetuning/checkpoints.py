"""Checkpoint discovery and safe safetensors header inspection."""

from __future__ import annotations

import json
import re
import struct
from pathlib import Path

STEP_PATTERN = re.compile(r"-step0*(\d+)\.safetensors$")
MAX_HEADER_BYTES = 100 * 1024 * 1024


def discover_checkpoints(directory: Path, wanted: set[int] | None = None) -> list[tuple[int, Path]]:
    checkpoints = []
    for path in directory.glob("*-step*.safetensors"):
        match = STEP_PATTERN.search(path.name)
        if match:
            step = int(match.group(1))
            if wanted is None or step in wanted:
                checkpoints.append((step, path))
    return sorted(checkpoints, key=lambda item: (item[0], item[1].name))


def read_safetensors_header(path: Path) -> dict[str, object]:
    with path.open("rb") as handle:
        raw_length = handle.read(8)
        if len(raw_length) != 8:
            raise ValueError("truncated safetensors length")
        length = struct.unpack("<Q", raw_length)[0]
        if length > MAX_HEADER_BYTES:
            raise ValueError("safetensors header is unreasonably large")
        raw_header = handle.read(length)
        if len(raw_header) != length:
            raise ValueError("truncated safetensors header")
    header = json.loads(raw_header)
    if not isinstance(header, dict):
        raise ValueError("safetensors header must be an object")
    return header


def checkpoint_is_vpred(path: Path) -> bool:
    try:
        header = read_safetensors_header(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    metadata = header.get("__metadata__", {})
    return "v_pred" in header or (
        isinstance(metadata, dict)
        and ("v_pred" in metadata or metadata.get("prediction_type") == "v_prediction")
    )
