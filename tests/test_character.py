import json
from pathlib import Path

from PIL import Image

from manga_finetuning.character import camera_caption, load_views, prepare_character_dataset


def test_camera_caption_describes_only_variable_view() -> None:
    view = {"azimuth": "right side view", "elevation": "low-angle shot", "distance": "close-up"}
    assert (
        camera_caption(view, "person_token")
        == "person_token, from side, profile, from below, portrait, close-up"
    )


def test_dataset_requires_matching_manifest(tmp_path: Path) -> None:
    images = tmp_path / "images"
    images.mkdir()
    Image.new("RGB", (8, 8)).save(images / "view.png")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"views": []}), encoding="utf-8")
    try:
        prepare_character_dataset(images, manifest, tmp_path / "out", "person_token")
    except ValueError as error:
        assert "missing manifest" in str(error)
    else:
        raise AssertionError("expected ValueError")


def test_dataset_writes_kohya_pairs(tmp_path: Path) -> None:
    images = tmp_path / "images"
    images.mkdir()
    Image.new("RGB", (8, 8)).save(images / "view.png")
    view = {
        "file": "view.png",
        "azimuth": "front view",
        "elevation": "eye-level shot",
        "distance": "wide shot",
    }
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"views": [view]}), encoding="utf-8")
    destination = prepare_character_dataset(
        images, manifest, tmp_path / "out", "person_token", repeats=5
    )
    assert destination.name == "5_person_token"
    assert (destination / "view.txt").read_text() == "person_token, facing viewer, full body\n"
    assert load_views(manifest)["view.png"] == view
