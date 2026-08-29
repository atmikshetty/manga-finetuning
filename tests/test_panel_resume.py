from pathlib import Path

from manga_finetuning.panels import collect_pages, done_marker, load_dumped_pages, output_directory


def test_resume_helpers_mirror_paths_and_ignore_bad_jsonl(tmp_path: Path) -> None:
    source, output = tmp_path / "source", tmp_path / "output"
    chapter = source / "chapter"
    chapter.mkdir(parents=True)
    page = chapter / "page.png"
    page.write_bytes(b"fixture")
    (chapter / ".hidden.jpg").write_bytes(b"skip")
    assert collect_pages(source) == [page]
    assert output_directory(page, source, output) == output / "chapter"
    assert done_marker(page, source, output) == output / "chapter" / ".page.panels.done"
    dump = tmp_path / "layouts.jsonl"
    dump.write_text('{"page":"a.png"}\ntruncated{\n{}\n', encoding="utf-8")
    assert load_dumped_pages(dump) == {"a.png"}
