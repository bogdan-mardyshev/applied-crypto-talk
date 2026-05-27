"""Smoke-тест для демки 01: ECB Penguin."""

import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from demo import ASSETS_DIR, main


def test_outputs_created(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """После запуска main() должны появиться три выходных файла."""
    monkeypatch.chdir(Path(__file__).parent)
    main()

    assert (ASSETS_DIR / "tux_ecb.png").exists(), "tux_ecb.png не создан"
    assert (ASSETS_DIR / "tux_cbc.png").exists(), "tux_cbc.png не создан"
    assert (ASSETS_DIR / "tux_gcm.png").exists(), "tux_gcm.png не создан"


def test_outputs_non_empty() -> None:
    """Каждый выходной файл должен иметь ненулевой размер."""
    for name in ("tux_ecb.png", "tux_cbc.png", "tux_gcm.png"):
        path = ASSETS_DIR / name
        assert path.stat().st_size > 0, f"{name} пустой"


def test_ecb_and_cbc_differ() -> None:
    """ECB и CBC версии не должны совпадать побайтово."""
    ecb_hash = hashlib.sha256((ASSETS_DIR / "tux_ecb.png").read_bytes()).digest()
    cbc_hash = hashlib.sha256((ASSETS_DIR / "tux_cbc.png").read_bytes()).digest()
    assert ecb_hash != cbc_hash, "ECB и CBC версии идентичны — что-то пошло не так"


def test_cbc_and_gcm_differ() -> None:
    """CBC и GCM версии не должны совпадать."""
    cbc_hash = hashlib.sha256((ASSETS_DIR / "tux_cbc.png").read_bytes()).digest()
    gcm_hash = hashlib.sha256((ASSETS_DIR / "tux_gcm.png").read_bytes()).digest()
    assert cbc_hash != gcm_hash, "CBC и GCM версии идентичны — что-то пошло не так"
