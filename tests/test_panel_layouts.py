from manga_finetuning.panels import clip_to_half, layout_records


def test_normal_page_is_normalized() -> None:
    records = layout_records("page.png", "licensed", 100, 200, [[10, 20, 90, 180]], [])
    assert records == [
        {
            "page": "page.png",
            "source": "licensed",
            "w": 100,
            "h": 200,
            "panels": [[0.1, 0.1, 0.9, 0.9]],
            "texts": [],
            "n_panels": 1,
            "spread": False,
        }
    ]


def test_spread_splits_right_to_left() -> None:
    records = layout_records(
        "spread.png", "licensed", 400, 200, [[210, 0, 390, 200], [10, 0, 190, 200]], []
    )
    assert [record["side"] for record in records] == ["right", "left"]
    assert all(record["w"] == 200 and record["spread"] for record in records)


def test_fold_sliver_does_not_duplicate_panel() -> None:
    assert clip_to_half([[192, 0, 232, 100]], 0, 200) == []
    assert clip_to_half([[192, 0, 232, 100]], 200, 400) == [[0, 0, 32, 100]]
