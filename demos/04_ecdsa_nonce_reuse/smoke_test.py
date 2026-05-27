"""Smoke-тест для демки 04: ECDSA Nonce Reuse."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from demo import (
    G,
    MESSAGE_1,
    MESSAGE_2,
    N,
    NONCE_K,
    PRIVATE_KEY_D,
    ecdsa_sign_with_k,
    ecdsa_verify,
    hash_message,
    main,
    recover_private_key,
)


def test_signatures_are_valid() -> None:
    """Обе подписи должны проверяться публичным ключом."""
    pub = PRIVATE_KEY_D * G
    r1, s1 = ecdsa_sign_with_k(MESSAGE_1, PRIVATE_KEY_D, NONCE_K)
    r2, s2 = ecdsa_sign_with_k(MESSAGE_2, PRIVATE_KEY_D, NONCE_K)
    assert ecdsa_verify(MESSAGE_1, (r1, s1), pub)
    assert ecdsa_verify(MESSAGE_2, (r2, s2), pub)


def test_same_nonce_gives_same_r() -> None:
    """Одинаковый nonce k должен давать одинаковое r."""
    r1, _ = ecdsa_sign_with_k(MESSAGE_1, PRIVATE_KEY_D, NONCE_K)
    r2, _ = ecdsa_sign_with_k(MESSAGE_2, PRIVATE_KEY_D, NONCE_K)
    assert r1 == r2, "Разные r при одинаковом k — ошибка в реализации"


def test_private_key_recovery() -> None:
    """Восстановленный приватный ключ должен совпасть с оригинальным."""
    h1 = hash_message(MESSAGE_1)
    h2 = hash_message(MESSAGE_2)
    r, s1 = ecdsa_sign_with_k(MESSAGE_1, PRIVATE_KEY_D, NONCE_K)
    _, s2 = ecdsa_sign_with_k(MESSAGE_2, PRIVATE_KEY_D, NONCE_K)

    recovered = recover_private_key(h1, h2, r, s1, s2)
    assert recovered == PRIVATE_KEY_D, (
        f"Восстановленный d={hex(recovered)} != оригинальный d={hex(PRIVATE_KEY_D)}"
    )


def test_recovered_key_can_sign() -> None:
    """Восстановленный ключ должен создавать подписи, проверяемые публичным ключом."""
    h1 = hash_message(MESSAGE_1)
    h2 = hash_message(MESSAGE_2)
    r, s1 = ecdsa_sign_with_k(MESSAGE_1, PRIVATE_KEY_D, NONCE_K)
    _, s2 = ecdsa_sign_with_k(MESSAGE_2, PRIVATE_KEY_D, NONCE_K)

    recovered_d = recover_private_key(h1, h2, r, s1, s2)
    pub = PRIVATE_KEY_D * G  # публичный ключ остаётся тем же

    test_msg = b"attacker controls victim wallet now"
    new_r, new_s = ecdsa_sign_with_k(test_msg, recovered_d, NONCE_K + 999)
    assert ecdsa_verify(test_msg, (new_r, new_s), pub)


def test_main_runs_without_error() -> None:
    """main() должен завершиться без исключений."""
    main()
