from manga_finetuning.evaluation import MONOCHROME, build_prompt


def test_prompt_order_and_palette() -> None:
    prompt = build_prompt("style_token", "solo, portrait")
    assert prompt.index("style_token") < prompt.index(MONOCHROME) < prompt.index("solo")
    assert MONOCHROME not in build_prompt("color_token", "solo", monochrome=False)
