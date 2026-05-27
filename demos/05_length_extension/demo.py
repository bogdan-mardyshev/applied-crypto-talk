"""
Demo 05 — Length Extension Attack на схему hash(secret || msg).

Задача: получить /admin доступ используя только легитимный токен,
без знания SECRET.

Инструмент: hashpumpy
    new_token, new_payload = hashpumpy.hashpump(
        original_token,    # известный MD5(SECRET || payload)
        original_payload,  # известный payload (без секрета)
        data_to_add,       # что добавляем
        secret_length,     # длина секрета (обычно перебирается 1..32)
    )

Запуск: python demo.py  (запускает сервер автоматически в отдельном потоке)
"""

import sys
import threading
import time
import urllib.parse

import hashpumpy
import requests

sys.path.insert(0, __file__.rsplit("/", 1)[0])

SERVER_URL = "http://127.0.0.1:5000"


def start_server() -> None:
    import logging

    from server import app

    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


def wait_for_server(timeout: int = 10) -> bool:
    for _ in range(timeout * 10):
        try:
            requests.get(f"{SERVER_URL}/", timeout=0.5)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.1)
    return False


# ---------------------------------------------------------------------------
# ТВОЯ ЗАДАЧА
# ---------------------------------------------------------------------------


def attack_length_extension(
    original_token: str,
    original_payload: str,
    secret_len: int,
    data_to_add: str = "&role=admin",
) -> tuple[str, str]:
    """Выполнить length extension атаку.

    Шаги:
        1. Вызвать hashpumpy.hashpump(original_token, original_payload,
                                       data_to_add, secret_len)
        2. Получить (new_token_hex, new_payload_bytes)
        3. Декодировать new_payload_bytes через .decode("latin-1")
           (latin-1 сохраняет MD5-паддинг байты без искажений)
        4. URL-encode payload для передачи в query string:
           urllib.parse.quote(new_payload_str, safe="=&")

    Returns:
        (new_payload_url_encoded, new_token_hex)
    """
    raise NotImplementedError("Реализуй length extension атаку через hashpumpy")


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


def main() -> bool:
    print("=" * 58)
    print("  Length Extension Attack")
    print("=" * 58)

    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()
    print("\n[*] Запускаем сервер...")
    if not wait_for_server():
        print("[!] Сервер не поднялся — запусти server.py вручную")
        sys.exit(1)

    # Шаг 1: легитимный логин
    print("[*] Шаг 1: получаем токен для 'alice'")
    resp = requests.post(f"{SERVER_URL}/login", json={"username": "alice"})
    data = resp.json()
    print(f"    payload:    {data['payload']}")
    print(f"    token:      {data['token']}")
    print(f"    secret_len: {data['secret_len']}")

    # Шаг 2: атака
    print("\n[*] Шаг 2: length extension → добавляем '&role=admin'")
    new_payload_url, new_token = attack_length_extension(
        data["token"], data["payload"], data["secret_len"]
    )
    print(f"    new_token:   {new_token}")
    print(f"    new_payload: {urllib.parse.unquote(new_payload_url)!r}")

    # Шаг 3: отправляем на сервер
    print("\n[*] Шаг 3: отправляем /admin с поддельным токеном")
    resp2 = requests.get(
        f"{SERVER_URL}/admin",
        params={"payload": urllib.parse.unquote(new_payload_url), "token": new_token},
    )
    if resp2.status_code == 200:
        print(f"\n[+] АТАКА УСПЕШНА: {resp2.json()}")
        return True
    else:
        print(f"\n[-] Не сработало: {resp2.status_code} — {resp2.json()}")
        return False


if __name__ == "__main__":
    main()
