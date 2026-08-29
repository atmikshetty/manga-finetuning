from pathlib import Path

from manga_finetuning.captions import process_caption, process_directory


def test_monochrome_caption_is_filtered_and_idempotent() -> None:
    once = process_caption("comic, Hero, speech bubble, monochrome, hero", "style_token")
    assert once == "style_token, monochrome, greyscale, Hero"
    assert process_caption(once, "style_token") == once


def test_color_keeps_monochrome_signal() -> None:
    assert (
        process_caption("greyscale, portrait", "color_token", color=True)
        == "color_token, greyscale, portrait"
    )


def test_directory_processes_only_top_level_captions(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("portrait\n", encoding="utf-8")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "b.txt").write_text("unchanged", encoding="utf-8")
    assert process_directory(tmp_path, "token") == 1
    assert (tmp_path / "a.txt").read_text() == "token, monochrome, greyscale, portrait\n"
    assert (nested / "b.txt").read_text() == "unchanged"
