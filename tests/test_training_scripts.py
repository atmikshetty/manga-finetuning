from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_scripts_have_no_fixed_workspace_or_personal_paths() -> None:
    for path in (ROOT / "scripts").glob("*.sh"):
        text = path.read_text(encoding="utf-8")
        assert "/workspace/" not in text
        assert "/Users/" not in text
        assert "SD_SCRIPTS_DIR" in text


def test_vpred_flags_remain_present() -> None:
    text = (ROOT / "scripts" / "train_style.sh").read_text(encoding="utf-8")
    assert "--v_parameterization" in text
    assert "--zero_terminal_snr" in text
    assert "--scale_v_pred_loss_like_noise_pred" in text
