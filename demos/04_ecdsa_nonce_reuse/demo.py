"""
Demo 04 — ECDSA Nonce Reuse: восстановление приватного ключа.

Это главная демка Bogdan'a.

История: именно этот баг позволил взломать PS3 (fail0verflow, 2010) и украсть
биткоины (~150 кошельков, 2012, Android RNG bug).

== Как работает ECDSA (кривая secp256k1) ==

Параметры: G — генератор кривой, n — порядок группы, d — приватный ключ.

Подпись (r, s):
    R = k * G           ← k — случайный nonce
    r = R.x mod n
    s = k⁻¹ * (h + r*d) mod n    где h = SHA256(message)

Верификация:
    s_inv = s⁻¹ mod n
    u1 = h * s_inv mod n
    u2 = r * s_inv mod n
    Проверить: (u1*G + u2*Q).x mod n == r    где Q = d*G (публичный ключ)

== Атака при nonce reuse (тот же k для двух сообщений) ==

Если k использован дважды, r₁ = r₂ (= R.x, R = k*G одно и то же).

    s₁ = k⁻¹(h₁ + r*d) mod n
    s₂ = k⁻¹(h₂ + r*d) mod n
    ─────────────────────────────
    s₁ - s₂ = k⁻¹(h₁ - h₂) mod n

    k = (h₁ - h₂) * (s₁ - s₂)⁻¹ mod n
    d = (s₁ * k - h₁) * r⁻¹ mod n

Всё вычисляется из ПУБЛИЧНО наблюдаемых значений!

Запуск: python demo.py
"""

import hashlib

from ecdsa import SECP256k1
from ecdsa.ellipticcurve import PointJacobi

CURVE = SECP256k1
G: PointJacobi = CURVE.generator
N: int = CURVE.order

# --- Захардкоженные параметры (для воспроизводимости) ---
PRIVATE_KEY_D: int = int(
    "c9afc3c6e4b3a8e2f1d5c7b9a2e4d6f8"
    "1a3c5e7b9d2f4a6c8e0b2d4f6a8c0e2b", 16,
)
NONCE_K: int = int(
    "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
    "e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2", 16,
)
MESSAGE_1 = b"Pay 1 BTC to Alice"
MESSAGE_2 = b"Pay 1 BTC to Bob"


# ---------------------------------------------------------------------------
# Вспомогательная функция (уже реализована)
# ---------------------------------------------------------------------------

def hash_message(msg: bytes) -> int:
    """SHA-256 хэш сообщения как целое число (стандарт для ECDSA)."""
    return int.from_bytes(hashlib.sha256(msg).digest(), "big")


# ---------------------------------------------------------------------------
# ТВОЯ ЗАДАЧА
# ---------------------------------------------------------------------------

def ecdsa_sign_with_k(message: bytes, d: int, k: int) -> tuple[int, int]:
    """ECDSA подпись с явным nonce k.

    ВНИМАНИЕ: в реальном ECDSA k должен быть случайным (RFC 6979).
    Здесь k фиксирован намеренно — это и есть уязвимость.

    Шаги:
        h = hash_message(message)
        R = k * G                       ← скалярное умножение точки на число
        r = int(R.x()) % N              ← x-координата точки R mod n
        k_inv = pow(k, -1, N)           ← модульное обратное
        s = (k_inv * (h + r * d)) % N

    Подсказка: R.x() возвращает x-координату точки R.
    Проверь: r != 0 и s != 0 (иначе k невалиден).

    Returns:
        (r, s) — пара подписи
    """
    raise NotImplementedError("Реализуй ECDSA подпись")


def ecdsa_verify(message: bytes, sig: tuple[int, int], public_key: PointJacobi) -> bool:
    """Верификация ECDSA подписи.

    Шаги:
        r, s = sig
        h = hash_message(message)
        s_inv = pow(s, -1, N)
        u1 = (h * s_inv) % N
        u2 = (r * s_inv) % N
        point = u1 * G + u2 * public_key   ← операции над точками кривой
        Вернуть: int(point.x()) % N == r

    Returns:
        True если подпись валидна
    """
    raise NotImplementedError("Реализуй ECDSA верификацию")


def recover_private_key(h1: int, h2: int, r: int, s1: int, s2: int) -> int:
    """Восстановить приватный ключ d из двух подписей с одинаковым k.

    Вывод формулы (сделай сам из системы уравнений выше в docstring модуля):

        k = (h1 - h2) * pow(s1 - s2, -1, N) % N
        d = (s1 * k - h1) * pow(r, -1, N) % N

    Все операции mod N. pow(x, -1, N) = модульное обратное.

    Args:
        h1, h2: хэши двух сообщений (уже вычисленные int)
        r:      общее r из обеих подписей (r1 == r2 при одном k)
        s1, s2: s-компоненты подписей

    Returns:
        Восстановленный приватный ключ d
    """
    raise NotImplementedError("Реализуй восстановление ключа!")


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  ECDSA Nonce Reuse → Private Key Recovery")
    print("=" * 60)

    public_key = PRIVATE_KEY_D * G

    print(f"\n[*] Кривая: secp256k1  (Bitcoin, Ethereum)")
    print(f"[*] d (приватный): {hex(PRIVATE_KEY_D)[:18]}...")
    print(f"[!] БАГ: оба сообщения подписаны с одним k")

    h1 = hash_message(MESSAGE_1)
    h2 = hash_message(MESSAGE_2)

    r1, s1 = ecdsa_sign_with_k(MESSAGE_1, PRIVATE_KEY_D, NONCE_K)
    r2, s2 = ecdsa_sign_with_k(MESSAGE_2, PRIVATE_KEY_D, NONCE_K)

    print(f"\n[*] r1={hex(r1)[:18]}...")
    print(f"[*] r2={hex(r2)[:18]}...")
    print(f"[!] r1 == r2: {r1 == r2}  ← R = k*G одинаково → уязвимость видна")

    v1 = ecdsa_verify(MESSAGE_1, (r1, s1), public_key)
    v2 = ecdsa_verify(MESSAGE_2, (r2, s2), public_key)
    print(f"\n[*] Подписи валидны: msg1={v1}, msg2={v2}")

    recovered_d = recover_private_key(h1, h2, r1, s1, s2)

    print(f"\n[+] Восстановленный d: {hex(recovered_d)}")
    print(f"[*] Оригинальный d:    {hex(PRIVATE_KEY_D)}")
    print(f"[+] Атака успешна: {recovered_d == PRIVATE_KEY_D}")


if __name__ == "__main__":
    main()
