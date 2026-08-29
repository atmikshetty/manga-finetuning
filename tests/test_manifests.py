import hashlib
from pathlib import Path

from manga_finetuning.manifests import artifact_manifest, run_manifest, sha256


def test_artifact_manifest_is_sorted_and_checksummed(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_bytes(b"b")
    (tmp_path / "a.txt").write_bytes(b"a")
    manifest = artifact_manifest(tmp_path)
    files = manifest["files"]
    assert [entry["path"] for entry in files] == ["a.txt", "b.txt"]
    assert files[0]["sha256"] == hashlib.sha256(b"a").hexdigest()
    assert sha256(tmp_path / "b.txt") == hashlib.sha256(b"b").hexdigest()


def test_run_manifest_hashes_config_without_environment(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    config.write_text("seed = 42\n", encoding="utf-8")
    manifest = run_manifest(config)
    assert manifest["config_sha256"] == hashlib.sha256(b"seed = 42\n").hexdigest()
    assert "environment" not in manifest
