"""Smoke-тест для демки 05: Length Extension Attack."""

import hashlib
import hmac
import sys
import threading
import time
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).parent))


@pytest.fixture(scope="module")
def flask_server():
    """Запустить Flask-сервер один раз для всех тестов модуля."""
    from server import app

    import logging

    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False),
        daemon=True,
    )
    thread.start()

    # Ждать пока сервер поднимется
    for _ in range(50):
        try:
            requests.get("http://127.0.0.1:5001/", timeout=0.5)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.1)

    yield "http://127.0.0.1:5001"


def test_login_returns_token(flask_server: str) -> None:
    """POST /login должен возвращать token, payload и secret_len."""
    resp = requests.post(f"{flask_server}/login", json={"username": "testuser"})
    assert resp.status_code == 200
    data = resp.json()
    assert "token" in data
    assert "payload" in data
    assert "secret_len" in data
    assert len(data["token"]) == 32  # MD5 hex


def test_length_extension_attack_succeeds(flask_server: str) -> None:
    """Атака должна пройти на /admin с уязвимым MD5(secret||payload) токеном."""
    import urllib.parse

    import hashpumpy

    resp = requests.post(f"{flask_server}/login", json={"username": "alice"})
    data = resp.json()

    new_token, new_payload_bytes = hashpumpy.hashpump(
        data["token"], data["payload"], "&role=admin", data["secret_len"]
    )
    new_payload = new_payload_bytes.decode("latin-1")

    resp2 = requests.get(
        f"{flask_server}/admin",
        params={"payload": new_payload, "token": new_token},
    )
    assert resp2.status_code == 200, f"Атака не сработала: {resp2.json()}"
    assert "secret" in resp2.json()


def test_hmac_blocks_length_extension() -> None:
    """HMAC-MD5 должен отвергать расширенный токен."""
    from server import SECRET, make_safe_token, make_vulnerable_token

    import hashpumpy

    original = b"username=alice&role=user"
    vuln_token = make_vulnerable_token(original)
    safe_token = make_safe_token(original)

    # Расширяем уязвимый токен — должен работать
    new_vuln, new_payload = hashpumpy.hashpump(
        vuln_token, original.decode(), "&role=admin", len(SECRET)
    )
    expected_vuln = hashlib.md5(SECRET + new_payload).hexdigest()
    assert new_vuln == expected_vuln, "Length extension не сработал на уязвимой схеме"

    # Расширяем safe токен — не должен совпасть с HMAC от расширенного payload
    new_safe_attempt, new_payload2 = hashpumpy.hashpump(
        safe_token, original.decode(), "&role=admin", len(SECRET)
    )
    actual_hmac = hmac.new(SECRET, new_payload2, hashlib.md5).hexdigest()
    assert new_safe_attempt != actual_hmac, "HMAC уязвим к length extension — что-то не так"
