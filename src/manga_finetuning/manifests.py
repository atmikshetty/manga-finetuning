"""Create deterministic artifact checksums and sanitized run manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_manifest(root: Path) -> dict[str, object]:
    files = []
    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return {"algorithm": "sha256", "files": files}


def run_manifest(config: Path | None = None) -> dict[str, object]:
    try:
        revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    return {
        "captured_at": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "git_revision": revision,
        "config_sha256": sha256(config) if config else None,
        "argv": sys.argv[1:],
    }


def artifact_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a recursive SHA-256 artifact manifest")
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    args.output.write_text(
        json.dumps(artifact_manifest(args.root), indent=2) + "\n", encoding="utf-8"
    )
    return 0


def run_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Capture a sanitized execution environment manifest"
    )
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    args.output.write_text(json.dumps(run_manifest(args.config), indent=2) + "\n", encoding="utf-8")
    return 0
