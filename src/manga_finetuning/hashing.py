"""Dependency-light perceptual hashing helpers."""

from __future__ import annotations

from typing import Protocol


class GrayImage(Protocol):
    def convert(self, mode: str): ...


def difference_hash(image: GrayImage, hash_size: int = 8) -> int:
    """Return a horizontal dHash compatible with the original preparation script."""
    if hash_size < 1:
        raise ValueError("hash_size must be positive")
    from PIL import Image

    gray = image.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixel_reader = getattr(gray, "get_flattened_data", gray.getdata)
    pixels = list(pixel_reader())
    value = 0
    for row in range(hash_size):
        for column in range(hash_size):
            index = row * (hash_size + 1) + column
            value = (value << 1) | (pixels[index] < pixels[index + 1])
    return value


def hamming_distance(left: int, right: int) -> int:
    """Count differing bits between two non-negative integer hashes."""
    if left < 0 or right < 0:
        raise ValueError("hashes must be non-negative")
    return (left ^ right).bit_count()


class HashIndex:
    """Simple exact dHash index; suitable for compact curated datasets."""

    def __init__(self, threshold: int = 8) -> None:
        if threshold < 0:
            raise ValueError("threshold must be non-negative")
        self.threshold = threshold
        self._hashes: list[int] = []

    def add_if_unique(self, value: int) -> bool:
        if any(hamming_distance(value, other) <= self.threshold for other in self._hashes):
            return False
        self._hashes.append(value)
        return True
