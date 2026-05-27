# Demo 03 — Textbook RSA: Chosen-Ciphertext Attack

**Владелец:** Bogdan | **Блок:** Асимметричная криптография

## What it demonstrates

RSA без паддинга (textbook RSA) обладает **мультипликативным свойством**: `E(M1) * E(M2) ≡ E(M1 * M2) (mod n)`. Это позволяет атакующему, имеющему доступ к decryption oracle, восстановить любой шифртекст — не взламывая ключ. Oracle при этом никогда не видит запрещённый шифртекст напрямую.

## How to run

```bash
make demo-03
# или:
python demos/03_textbook_rsa_cca/demo.py
```

## Expected output

```
============================================================
  Textbook RSA — Chosen-Ciphertext Attack
============================================================

[*] Параметры RSA: n=3233, e=17, d=2753
[*] Секретное сообщение M = 42
[*] Шифртекст C = M^e mod n = 2557

[*] Атакующий выбирает r = 2
[*] C' = C * r^e mod n = ...  (отправляем в oracle)
[*] Oracle возвращает M' = ...  (= M*r mod n = 84)

[+] Восстановленный M = ... = 42
[+] Атака успешна: True
```

## The math

```
RSA: C = M^e mod n,   M = C^d mod n

Мультипликативность:
  E(M) * E(r) = M^e * r^e = (M*r)^e = E(M*r)   (mod n)

Атака:
  1. Перехватить C = M^e mod n
  2. Выбрать r: gcd(r, n) = 1
  3. C' = C * r^e mod n  →  отправить в oracle
  4. M' = oracle(C') = (C')^d = (M*r)^(e*d) = M*r  (mod n)
  5. M  = M' * r^(-1) mod n
```

Атакующий задаёт вопрос oracle о `C'`, а не `C` — oracle не может отличить один от другого. Это называется **adaptive chosen-ciphertext attack (CCA2)**.

## How to fix

Использовать **OAEP** (Optimal Asymmetric Encryption Padding, RFC 8017):
```python
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

ciphertext = public_key.encrypt(
    plaintext,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)
```

OAEP вносит случайность и структуру, которую проверяет при расшифровании. `C' = C * r^e` расшифруется как мусор, unpad вернёт ошибку — oracle откажет. Никогда не реализуйте RSA вручную.
