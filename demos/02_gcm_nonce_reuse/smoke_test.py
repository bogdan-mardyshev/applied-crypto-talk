"""Smoke-тест для демки 02: GCM Nonce Reuse."""

import sys
from pathlib import Path

sys.modules.pop("demo", None)
sys.path.insert(0, str(Path(__file__).parent))

from demo import KEY, NONCE, PLAINTEXT_1, PLAINTEXT_2, attack_nonce_reuse, encrypt_gcm, xor_bytes


def test_xor_cancels_keystream() -> None:
    """CT1 XOR CT2 должен равняться PT1 XOR PT2 при одинаковом nonce."""
    ct1 = encrypt_gcm(PLAINTEXT_1, KEY, NONCE)
    ct2 = encrypt_gcm(PLAINTEXT_2, KEY, NONCE)

    xor_ct = xor_bytes(ct1, ct2)
    xor_pt = xor_bytes(PLAINTEXT_1, PLAINTEXT_2)

    assert xor_ct == xor_pt, "Keystream не сократился — проверьте шифрование"


def test_attack_recovers_plaintext_2() -> None:
    """Атака должна точно восстановить PT2 из CT1, CT2 и известного PT1."""
    ct1 = encrypt_gcm(PLAINTEXT_1, KEY, NONCE)
    ct2 = encrypt_gcm(PLAINTEXT_2, KEY, NONCE)

    recovered = attack_nonce_reuse(ct1, ct2, PLAINTEXT_1)
    assert recovered == PLAINTEXT_2, f"Ожидали {PLAINTEXT_2!r}, получили {recovered!r}"


def test_different_nonces_are_safe() -> None:
    """С разными nonce XOR шифртекстов НЕ равен XOR открытых текстов."""
    import os

    nonce2 = os.urandom(12)
    ct1 = encrypt_gcm(PLAINTEXT_1, KEY, NONCE)
    ct2 = encrypt_gcm(PLAINTEXT_2, KEY, nonce2)

    xor_ct = xor_bytes(ct1, ct2)
    xor_pt = xor_bytes(PLAINTEXT_1, PLAINTEXT_2)

    # Вероятность случайного совпадения пренебрежимо мала
    assert xor_ct != xor_pt, "Разные nonce дали одинаковый keystream — не должно быть"
