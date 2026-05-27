"""pytest конфигурация: sys.path + xfail для нереализованных функций."""

import sys
from pathlib import Path

import pytest

# Каждая demo-директория в sys.path, чтобы smoke_test.py мог `from demo import ...`
_DEMOS_DIR = Path(__file__).parent.parent / "demos"

for demo_dir in sorted(_DEMOS_DIR.iterdir()):
    if demo_dir.is_dir() and demo_dir.name[0].isdigit():
        sys.path.insert(0, str(demo_dir))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """NotImplementedError → xfail (ожидаемое падение для скелетов).

    Когда функция в demo.py ещё не реализована, тест помечается как
    'expected failure' (xfail) вместо 'error'. CI остаётся зелёным,
    а команда видит какие именно функции ещё не написаны.
    """
    outcome = yield
    if outcome.excinfo is not None and outcome.excinfo[0] is NotImplementedError:
        pytest.xfail("Не реализовано — напиши функцию в demo.py")
