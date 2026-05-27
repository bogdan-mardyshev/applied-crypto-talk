# Demo 04 — ECDSA Nonce Reuse → Private Key Recovery

**Владелец:** Bogdan | **Блок:** Асимметричная криптография

## What it demonstrates

ECDSA требует уникального случайного nonce `k` для каждой подписи. Если два разных сообщения подписаны с одним `k`, атакующий восстанавливает приватный ключ целиком — зная только публичные значения `(r, s1, s2, h1, h2)`. Именно это произошло с Sony PS3 и сотнями Bitcoin-кошельков.

## How to run

```bash
make demo-04
# или:
python demos/04_ecdsa_nonce_reuse/demo.py
```

## Expected output

```
==============================================================
  ECDSA Nonce Reuse → Private Key Recovery
==============================================================

[*] Кривая:       secp256k1 (Bitcoin, Ethereum)
[!] БАГ: оба сообщения подписаны с ОДНИМ nonce k = 0xa1b2c3d4...

[!] r1 == r2: True  ← оба R = k*G одинаковы

[+] Восстановленный d:  0xc9afc3c6...
[*] Оригинальный d:     0xc9afc3c6...

[+] АТАКА УСПЕШНА: recovered_d == PRIVATE_KEY_D → True
```

## The math

```
ECDSA подпись (r, s):
  R = k * G
  r = R.x mod n
  s = k⁻¹ * (h + r*d) mod n

При одинаковом k для двух сообщений:
  s₁ = k⁻¹(h₁ + r*d) mod n
  s₂ = k⁻¹(h₂ + r*d) mod n
  ──────────────────────────
  s₁ - s₂ = k⁻¹(h₁ - h₂) mod n
  ⟹ k = (h₁ - h₂) * (s₁ - s₂)⁻¹ mod n
  ⟹ d = (s₁ * k - h₁) * r⁻¹ mod n
```

Всё вычисляется из публично наблюдаемых значений — никаких оракулов не нужно.

## How to fix

**RFC 6979** (deterministic ECDSA): `k = HMAC-SHA256(d, h || extra_entropy)` — детерминированный nonce из приватного ключа и хэша. Каждое уникальное сообщение → уникальный `k`. Нет RNG — нет баг.

**Ещё лучше: Ed25519** — EdDSA схема, где nonce детерминирован по дизайну, нет условных переходов, нет timing side-channels. Используйте `cryptography` или `PyNaCl`:

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

private_key = Ed25519PrivateKey.generate()
signature = private_key.sign(message)
public_key = private_key.public_key()
public_key.verify(signature, message)  # raises InvalidSignature if bad
```
