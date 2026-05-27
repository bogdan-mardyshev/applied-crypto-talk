---
marp: true
theme: default
paginate: true
backgroundColor: "#1a1a2e"
color: "#eaeaea"
style: |
  h1 { color: #e94560; }
  h2 { color: #0f3460; background: #e94560; padding: 4px 12px; border-radius: 4px; }
  code { background: #16213e; color: #a8ff78; }
  strong { color: #f5a623; }
  table { font-size: 0.85em; }
---

# Асимметричная криптография: RSA, ECC и их провалы

**Student 2 — Bogdan**
Блок: RSA vs ECC, Diffie-Hellman, ECDSA Nonce Reuse

---

## Проблема симметрики

Алиса и Боб хотят общаться безопасно. У них нет общего секрета.
Как договориться о ключе по открытому каналу?

**Ответ Диффи и Хеллмана (1976):** можно.

---

## RSA vs ECC vs Curve25519

| | RSA-2048 | ECC (P-256) | Curve25519 |
|---|---|---|---|
| Длина ключа | 2048 бит | 256 бит | 256 бит |
| Подпись | ~3 ms | ~0.5 ms | ~0.05 ms |
| Проверка | ~0.1 ms | ~1 ms | ~0.1 ms |
| Side-channels | Сложно | Зависит | Константное время |
| Стандарт | RFC 3447 | NIST P-curves | RFC 7748 |
| Применение | TLS 1.2, S/MIME | TLS 1.3, ECDSA | SSH, Signal, WireGuard |

**ECC = тот же уровень безопасности при ключе в 10× короче**

---

## Diffie-Hellman: интуиция

Малые числа для наглядности. `g=5, p=23`.

```
Алиса выбирает a=6:   A = 5⁶ mod 23 = 8        (отправляет Бобу)
Боб выбирает b=15:    B = 5¹⁵ mod 23 = 19       (отправляет Алисе)

Алиса: S = B^a mod p = 19⁶ mod 23 = 2
Боб:   S = A^b mod p = 8¹⁵ mod 23 = 2  ✓ общий секрет!
```

Перехватчик видит `g, p, A=8, B=19`. Вычислить `a` из `A = g^a mod p` — это **проблема дискретного логарифма** (NP-hard при больших p).

---

## ECDHE в TLS 1.3

```
Client → Server:  ClientHello + key_share (X=a*G на Curve25519)
Server → Client:  ServerHello + key_share (Y=b*G на Curve25519)

Общий секрет: K = a*(b*G) = b*(a*G) = ab*G
```

**Forward Secrecy:** новый `a, b` для каждой сессии. Если сервер скомпрометирован — старые сессии не расшифровать.

---

## Почему нельзя реализовывать RSA самому

Казалось бы: `pow(m, e, n)` — что может пойти не так?

- **Padding Oracle** (PKCS#1 v1.5): RFC 3218, атака Bleichenbacher (1998), ROBOT (2017)
- **Timing attacks:** ветки по битам ключа → утечка приватного ключа
- **Textbook RSA (без паддинга):** мультипликативность → CCA
- **Малые e:** broadcast attack, Franklin-Reiter

**Нет паддинга → нет безопасности. Паддинг сложно реализовать корректно.**

---

## Textbook RSA: мультипликативность

```python
# Шифрование: C = M^e mod n  (без паддинга)
# Мультипликативность: E(M1) * E(M2) = E(M1 * M2)  mod n

# Атака:
# 1. Перехватить C = M^e mod n
# 2. Выбрать r, создать C' = C * r^e mod n = (M*r)^e mod n
# 3. Oracle(C') → M' = M*r mod n
# 4. M = M' * r^(-1) mod n
```

Oracle не видит исходный `C` — только «другой» шифртекст.

---

## Демо 3: Textbook RSA CCA

### → Переходим к демке

```bash
python demos/03_textbook_rsa_cca/demo.py
```

- RSA с малыми параметрами (n=3233, e=17, d=2753)
- Зашифруем `M=42`
- Восстановим без ключа через decryption oracle

---

## ECDSA: алгоритм подписи

Кривая secp256k1. Генератор `G`, порядок группы `n`, приватный ключ `d`.

```
Подпись (r, s):
  Выбрать случайный nonce k
  R = k * G
  r = R.x mod n
  s = k⁻¹ * (hash(msg) + r * d) mod n
```

**Безопасность полностью зависит от случайности k.**

---

## ECDSA Nonce Reuse: два сообщения, один k

```
s₁ = k⁻¹(h₁ + r*d) mod n
s₂ = k⁻¹(h₂ + r*d) mod n
──────────────────────────────────
s₁ - s₂ = k⁻¹(h₁ - h₂) mod n

k = (h₁ - h₂) * (s₁ - s₂)⁻¹ mod n
d = (s₁ * k - h₁) * r⁻¹ mod n
```

Публично известны: `r, s₁, s₂, h₁, h₂`. Приватный ключ — нет.

---

## Реальные случаи

**Sony PlayStation 3 (2010, fail0verflow):**
- Весь firmware подписан одним k
- Группа за несколько часов восстановила мастер-приватный ключ
- Результат: возможность запуска любого кода, открытие homebrew

**Bitcoin Android wallets (2012):**
- Android SecureRandom возвращал одинаковые значения
- ~150 кошельков опустошено
- Потери: сотни BTC (по тогдашнему курсу ~$5K, сейчас ~$7M+)

---

## Демо 4: ECDSA Nonce Reuse

### → Переходим к демке

```bash
python demos/04_ecdsa_nonce_reuse/demo.py
```

- Кривая secp256k1, фиксированный приватный ключ d и nonce k
- Подпишем два разных сообщения
- Покажем `r₁ == r₂`
- Восстановим k и d из публичных (r, s₁, s₂, h₁, h₂)

---

## Как фиксить

**RFC 6979** — детерминированный ECDSA:
```
k = HMAC-SHA256(private_key, hash(msg) ‖ extra_entropy)
```
Каждое уникальное сообщение → уникальный k. Нет RNG = нет бага.

**Ещё лучше: Ed25519**
```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
key = Ed25519PrivateKey.generate()
sig = key.sign(message)
key.public_key().verify(sig, message)
```
Детерминированный nonce по дизайну. Константное время. Нет timing side-channels.

---

## Переход к Kirill

Мы разобрали шифрование (симметрика, асимметрика). Но как проверить **целостность**?

Хэш-функции, MACs, подписи — это следующий блок.

→ Kirill расскажет почему MD5 мёртв, как работает HMAC и почему length extension — это не только теория.
