from manga_finetuning.panels import extract_boxes, intersection, to_box_list


def test_bbox_parsing_normalizes_orders_clamps_and_skips() -> None:
    raw = [[0.8, 0.9, 0.2, 0.1], [-10, 2, 20, 30], [1, 2, 1, 3], ["x", 0, 1, 1]]
    assert to_box_list(raw, 100, 200) == [[20, 20, 80, 180], [0, 2, 20, 30]]


def test_extract_boxes_accepts_aliases() -> None:
    panels, texts = extract_boxes(
        {"panel_bboxes": [[1, 2, 8, 9]], "balloons": [[2, 3, 4, 5]]}, 10, 10
    )
    assert panels == [[1, 2, 8, 9]]
    assert texts == [[2, 3, 4, 5]]


def test_intersection_excludes_touching_edges() -> None:
    assert intersection([0, 0, 5, 5], [4, 3, 9, 9]) == [4, 3, 5, 5]
    assert intersection([0, 0, 5, 5], [5, 0, 9, 9]) is None
