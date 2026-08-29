from PIL import Image

from manga_finetuning.panels import process_page


def test_whiteout_uses_panel_local_coordinates_and_padding() -> None:
    page = Image.new("RGB", (20, 20), "black")
    crops, stats = process_page(
        page,
        [[5, 5, 15, 15]],
        [[8, 8, 10, 10]],
        min_panel_size=5,
        text_padding=1,
        max_text_coverage=0.5,
    )
    assert len(crops) == 1
    assert crops[0][1].getpixel((2, 2)) == (255, 255, 255)
    assert crops[0][1].getpixel((0, 0)) == (0, 0, 0)
    assert stats["text_boxes_removed"] == 1


def test_filters_small_and_mostly_text_panels() -> None:
    page = Image.new("RGB", (20, 20), "black")
    crops, stats = process_page(
        page,
        [[0, 0, 4, 4], [5, 5, 15, 15]],
        [[5, 5, 15, 15]],
        min_panel_size=5,
        text_padding=0,
        max_text_coverage=0.5,
    )
    assert crops == []
    assert stats["skipped_small"] == 1
    assert stats["skipped_mostly_text"] == 1
