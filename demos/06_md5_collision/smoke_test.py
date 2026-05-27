"""Smoke-тест для демки 06: MD5 Collision."""

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from demo import BLOCK_A, BLOCK_B, EXPECTED_MD5, main, md5hex


def test_collision_is_real() -> None:
    """MD5(BLOCK_A) должен равняться MD5(BLOCK_B)."""
    assert md5hex(BLOCK_A) == md5hex(BLOCK_B), (
        "MD5 хэши не совпадают — коллизионные константы неверны"
    )


def test_blocks_are_different() -> None:
    """Блоки должны быть реально разными."""
    assert BLOCK_A != BLOCK_B, "Блоки идентичны — это не коллизия"


def test_blocks_have_equal_length() -> None:
    """Оба блока должны быть одинакового размера (128 байт)."""
    assert len(BLOCK_A) == 128
    assert len(BLOCK_B) == 128


def test_known_md5_value() -> None:
    """MD5 должен совпасть с известным значением из публикации Wang et al."""
    assert md5hex(BLOCK_A) == EXPECTED_MD5, (
        f"Ожидали {EXPECTED_MD5}, получили {md5hex(BLOCK_A)}"
    )


def test_sha256_no_collision() -> None:
    """SHA-256 хэши блоков должны быть разными (демонстрация что SHA-256 устойчив)."""
    sha_a = hashlib.sha256(BLOCK_A).hexdigest()
    sha_b = hashlib.sha256(BLOCK_B).hexdigest()
    assert sha_a != sha_b, "SHA-256 тоже дал коллизию — это невозможно"


def test_main_runs_without_error() -> None:
    """main() должен завершиться без исключений."""
    main()
