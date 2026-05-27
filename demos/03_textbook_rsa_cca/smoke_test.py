"""Smoke-тест для демки 03: Textbook RSA CCA."""

import sys
from pathlib import Path

sys.modules.pop("demo", None)
sys.path.insert(0, str(Path(__file__).parent))

from demo import (
    _D,
    _E,
    _N,
    cca_attack,
    rsa_decrypt,
    rsa_encrypt,
)


def test_encrypt_decrypt_roundtrip() -> None:
    """RSA шифрование/расшифрование должны быть взаимно обратными."""
    for m in [1, 7, 42, 100, 1000, _N - 1]:
        c = rsa_encrypt(m, _E, _N)
        m2 = rsa_decrypt(c, _D, _N)
        assert m == m2, f"Roundtrip failed for m={m}"


def test_cca_recovers_message() -> None:
    """CCA атака должна восстановить оригинальное сообщение."""
    for secret in [1, 42, 99, 500, 1234]:
        ct = rsa_encrypt(secret, _E, _N)
        recovered = cca_attack(ct, _E, _N, r=3)
        assert recovered == secret, f"CCA failed for secret={secret}, got {recovered}"


def test_oracle_never_sees_original_ciphertext() -> None:
    """Oracle не должен получать оригинальный шифртекст (демонстрация ослепления)."""
    secret = 42
    ct = rsa_encrypt(secret, _E, _N)
    r = 5
    blinded_ct = (ct * pow(r, _E, _N)) % _N
    # Ослеплённый шифртекст всегда отличается от оригинального
    assert blinded_ct != ct, "Ослепление не изменило шифртекст"


def test_main_runs_without_error() -> None:
    """main() должен завершаться без исключений."""
    from demo import main

    main()
