"""Smoke-тест для демки 06: MD5 Birthday Attack."""

import sys
from pathlib import Path

sys.modules.pop("demo", None)
sys.path.insert(0, str(Path(__file__).parent))

from demo import find_collision, truncated_md5


def test_collision_found_16bit() -> None:
    """find_collision(16) должен найти два разных сообщения с одинаковым 16-бит хэшем."""
    msg1, msg2, attempts = find_collision(16)
    assert msg1 != msg2, "msg1 и msg2 должны быть разными"
    assert truncated_md5(msg1, 16) == truncated_md5(msg2, 16), "Хэши должны совпадать"
    assert attempts > 0, "Число попыток должно быть положительным"


def test_collision_valid_types() -> None:
    """find_collision должен возвращать кортеж (bytes, bytes, int)."""
    msg1, msg2, attempts = find_collision(16)
    assert isinstance(msg1, bytes)
    assert isinstance(msg2, bytes)
    assert isinstance(attempts, int)


def test_birthday_bound_16bit() -> None:
    """Число попыток должно быть разумным — не превышать 10 * 2^(bits/2)."""
    _, _, attempts = find_collision(16)
    # Теоретически ≈ 323 попытки; даём запас 10×
    assert attempts < 10 * (2**8), f"Слишком много попыток: {attempts} (ожидали < {10 * 2**8})"


def test_main_runs_without_error() -> None:
    """main() должен завершиться без исключений."""
    from demo import main

    main()
