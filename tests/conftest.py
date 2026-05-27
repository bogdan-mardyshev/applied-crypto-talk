"""pytest конфигурация: sys.path + xfail для нереализованных функций."""

import sys
from pathlib import Path

import pytest

# Каждая demo-директория в sys.path, чтобы smoke_test.py мог `from demo import ...`
_DEMOS_DIR = Path(__file__).parent.parent / "demos"

for demo_dir in sorted(_DEMOS_DIR.iterdir()):
    if demo_dir.is_dir() and demo_dir.name[0].isdigit():
        sys.path.insert(0, str(demo_dir))


def pytest_collection_modifyitems(items: list) -> None:
    """Все тесты из demos/ помечаем xfail (скелеты ещё не реализованы).

    Это покрывает все случаи падения:
    - NotImplementedError прямо в тесте
    - Flask/HTTP ошибки (500), когда NotImplementedError внутри route
    - AssertionError из-за неожиданного поведения заглушки

    Как только студент реализует функцию — тест начинает проходить
    (xpass), и CI остаётся зелёным.
    """
    marker = pytest.mark.xfail(
        reason="Demo не реализована — напиши функцию в demo.py",
        strict=False,
    )
    for item in items:
        if _DEMOS_DIR in Path(str(item.fspath)).parents:
            item.add_marker(marker, append=False)
