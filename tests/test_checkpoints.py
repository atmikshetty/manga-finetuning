import json
import struct
from pathlib import Path

from manga_finetuning.checkpoints import (
    checkpoint_is_vpred,
    discover_checkpoints,
    read_safetensors_header,
)


def write_header(path: Path, header: dict) -> None:
    payload = json.dumps(header).encode()
    path.write_bytes(struct.pack("<Q", len(payload)) + payload)


def test_checkpoint_discovery_is_numeric_and_filterable(tmp_path: Path) -> None:
    for name in ("run-step0010.safetensors", "run-step2.safetensors", "other.safetensors"):
        (tmp_path / name).touch()
    assert [step for step, _ in discover_checkpoints(tmp_path)] == [2, 10]
    assert [step for step, _ in discover_checkpoints(tmp_path, {10})] == [10]


def test_vpred_header_metadata_is_detected(tmp_path: Path) -> None:
    checkpoint = tmp_path / "base.safetensors"
    write_header(checkpoint, {"__metadata__": {"prediction_type": "v_prediction"}})
    assert read_safetensors_header(checkpoint)["__metadata__"]
    assert checkpoint_is_vpred(checkpoint)


def test_bad_header_fails_closed(tmp_path: Path) -> None:
    checkpoint = tmp_path / "bad.safetensors"
    checkpoint.write_bytes(b"bad")
    assert not checkpoint_is_vpred(checkpoint)
