from PIL import Image

from manga_finetuning.hashing import HashIndex, difference_hash, hamming_distance


def test_dhash_tracks_horizontal_gradient() -> None:
    image = Image.new("L", (9, 8))
    image.putdata([column * 28 for _row in range(8) for column in range(9)])
    assert difference_hash(image) == (1 << 64) - 1


def test_hamming_and_index_threshold() -> None:
    assert hamming_distance(0b1010, 0b0011) == 2
    index = HashIndex(threshold=1)
    assert index.add_if_unique(0)
    assert not index.add_if_unique(1)
    assert index.add_if_unique(3)
