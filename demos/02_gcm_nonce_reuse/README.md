# Demo 02 — GCM Nonce Reuse

**Владелец:** Osman | **Блок:** Симметричное шифрование

## What it demonstrates

AES-GCM — это stream cipher под капотом: keystream зависит только от `(K, nonce)`. Если один nonce использован дважды с одним ключом, XOR двух шифртекстов равен XOR двух открытых текстов. Зная одно сообщение (или формат), атакующий восстанавливает второе. Расширенная «Forbidden Attack» дополнительно восстанавливает секретный ключ аутентификации `H = AES_K(0)`, что позволяет подделывать теги GCM.

## How to run

```bash
make demo-02
# или:
python demos/02_gcm_nonce_reuse/demo.py
```

## Expected output

```
============================================================
  GCM Nonce Reuse Attack
============================================================

[*] Ключ (K):       603deb10...
[*] Нonce (ОДИНАК): 000102030405060708090a0b  ← ОШИБКА: один nonce для двух сообщений

[*] CT1 ⊕ CT2: ...
[*] PT1 ⊕ PT2: ...
    Равны:     True  ← keystream сократился!

[+] Восстановленный PT2: b'transfer: alice -> eve  $99999'
[+] Совпадают: True
```

## The math

AES-GCM работает в CTR-режиме:

```
C₁ = P₁ ⊕ KeyStream(K, N)
C₂ = P₂ ⊕ KeyStream(K, N)   ← тот же keystream при том же N!
──────────────────────────────
C₁ ⊕ C₂ = P₁ ⊕ P₂
```

Keystream сокращается в XOR. Зная `P₁`, атакующий вычисляет `P₂ = (C₁ ⊕ C₂) ⊕ P₁`.

**Forbidden Attack** (Joux, 2006): из двух шифртекстов с одним nonce восстанавливается `H = AES_K(0)` — основа MAC Poly1305-GCM. После этого можно подделывать теги для произвольных сообщений, полностью обходя аутентификацию.

## How to fix

```python
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)

# ПРАВИЛЬНО: случайный nonce каждый раз
nonce = os.urandom(12)
ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
```

Альтернатива при необходимости детерминизма: **AES-SIV** (RFC 5297) — синтетический IV вычисляется из самого сообщения, nonce-misuse resistant.
