from pathlib import Path

from PIL import Image

from manga_finetuning.dataset import collect_images, prepare_dataset


def save_pattern(path: Path, *, invert: bool = False, size: tuple[int, int] = (24, 16)) -> None:
    image = Image.new("RGB", size)
    image.putdata(
        [
            ((x * 31) % 256,) * 3 if not invert else ((255 - x * 31) % 256,) * 3
            for y in range(size[1])
            for x in range(size[0])
        ]
    )
    image.save(path)


def test_preparation_filters_resizes_and_deduplicates(tmp_path: Path) -> None:
    source, output = tmp_path / "source", tmp_path / "output"
    source.mkdir()
    save_pattern(source / "a.png")
    save_pattern(source / "duplicate.png")
    save_pattern(source / "different.png", invert=True)
    Image.new("RGB", (4, 4)).save(source / "small.png")
    (source / "bad.png").write_bytes(b"not an image")

    stats = prepare_dataset(source, output, min_side=8, max_side=20, duplicate_threshold=0)

    assert (stats.kept, stats.duplicate, stats.too_small, stats.corrupt) == (2, 1, 1, 1)
    assert collect_images(output) == [output / "panel_00000.png", output / "panel_00001.png"]
    with Image.open(output / "panel_00000.png") as image:
        assert image.size == (20, 13)


def test_preparation_rejects_in_place_output(tmp_path: Path) -> None:
    try:
        prepare_dataset(tmp_path, tmp_path)
    except ValueError as error:
        assert "must differ" in str(error)
    else:
        raise AssertionError("expected ValueError")
