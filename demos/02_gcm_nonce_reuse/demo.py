"""
Demo 02 — GCM Nonce Reuse: восстановление открытого текста.

Задача: показать что при reuse nonce в AES-GCM
  C1 ⊕ C2 = P1 ⊕ P2  (keystream сокращается)

Зная P1, атакующий восстанавливает P2 полностью.

Запуск: python demo.py
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# --- Детерминированные параметры ---
KEY: bytes = bytes.fromhex("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4")
NONCE: bytes = bytes.fromhex("000102030405060708090a0b")  # ← ОДИН nonce для обоих!

PLAINTEXT_1 = b"transfer: alice -> bob  $10000"
PLAINTEXT_2 = b"transfer: alice -> eve  $99999"


# ---------------------------------------------------------------------------
# ТВОЯ ЗАДАЧА
# ---------------------------------------------------------------------------


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """Побайтовый XOR двух последовательностей (до длины наименьшей).

    Подсказка: bytes(x ^ y for x, y in zip(a, b))
    """
    raise NotImplementedError("Реализуй XOR байт")


def encrypt_gcm(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    """AES-GCM шифрование. Вернуть только шифртекст (без 16-байт тега).

    Подсказка:
        AESGCM(key).encrypt(nonce, plaintext, None)
        Результат содержит [ciphertext (len(pt) bytes) | tag (16 bytes)]
        Верни только шифртекст.
    """
    raise NotImplementedError("Реализуй AES-GCM шифрование")


def attack_nonce_reuse(ct1: bytes, ct2: bytes, known_pt1: bytes) -> bytes:
    """Восстановить PT2 из двух шифртекстов и известного PT1.

    Математика:
        CT1 = PT1 ⊕ KeyStream(K, N)
        CT2 = PT2 ⊕ KeyStream(K, N)   ← тот же KeyStream!
        ─────────────────────────────
        CT1 ⊕ CT2 = PT1 ⊕ PT2         (KeyStream сокращается)

        PT2 = (CT1 ⊕ CT2) ⊕ PT1

    Шаги:
        1. xor_ct = xor_bytes(ct1, ct2)   → это PT1 ⊕ PT2
        2. pt2    = xor_bytes(xor_ct, known_pt1)
    """
    raise NotImplementedError("Реализуй атаку nonce reuse")


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 58)
    print("  GCM Nonce Reuse Attack")
    print("=" * 58)

    aesgcm = AESGCM(KEY)
    ct1_full = aesgcm.encrypt(NONCE, PLAINTEXT_1, None)
    ct2_full = aesgcm.encrypt(NONCE, PLAINTEXT_2, None)

    ct1 = ct1_full[: len(PLAINTEXT_1)]
    ct2 = ct2_full[: len(PLAINTEXT_2)]

    print(f"\n[!] Один nonce для двух сообщений: {NONCE.hex()}")
    print(f"[*] CT1: {ct1.hex()}")
    print(f"[*] CT2: {ct2.hex()}")

    xor_ct = xor_bytes(ct1, ct2)
    xor_pt = xor_bytes(PLAINTEXT_1, PLAINTEXT_2)
    print(f"\n[*] CT1 ⊕ CT2 = {xor_ct.hex()}")
    print(f"[*] PT1 ⊕ PT2 = {xor_pt.hex()}")
    print(f"[*] Равны: {xor_ct == xor_pt}  ← keystream сократился!")

    recovered = attack_nonce_reuse(ct1, ct2, PLAINTEXT_1)
    print(f"\n[+] Восстановленный PT2: {recovered}")
    print(f"[+] Оригинальный PT2:    {PLAINTEXT_2}")
    print(f"[+] Атака успешна: {recovered == PLAINTEXT_2}")


if __name__ == "__main__":
    main()
