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
---

# Хэши, MACs и цифровые подписи: что может пойти не так

**Student 3 — Kirill**
Блок: MD5/SHA-1 смерть, HMAC, Length Extension, Ed25519

---

## Collision vs Preimage: в чём разница

**Preimage resistance:** Дано `h = H(m)`. Невозможно найти `m`.
→ Нарушение: злоумышленник восстанавливает пароль из хэша.

**Collision resistance:** Невозможно найти `m₁ ≠ m₂` такие что `H(m₁) = H(m₂)`.
→ Нарушение: два разных файла, одна подпись.

**Second preimage resistance:** Дано `m₁`. Невозможно найти `m₂ ≠ m₁` с `H(m₁) = H(m₂)`.

Коллизия сломана раньше preimage: Shannon — около `2^(n/2)` vs `2^n`.

---

## Смерть MD5 и SHA-1

| Хэш | Коллизия найдена | Стоимость сегодня |
|-----|-----------------|------------------|
| MD5 | Wang et al., 2004 | < $1 (секунды на CPU) |
| SHA-1 | SHAttered, 2017 (Google) | ~$75k GPU-часов (2017), дешевле сейчас |
| SHA-256 | Не найдена | Теоретически 2^128 операций |
| SHA-3 (Keccak) | Не найдена | Другой принцип, нет MD слабости |

SHA-1 официально deprecate в TLS/X.509 с 2017. Но он всё ещё есть везде.

---

## Где MD5/SHA-1 всё ещё прячутся

- **Checksums дистрибутивов:** `md5sum ubuntu.iso` — до сих пор часто
- **Git object IDs:** SHA-1 (переходят на SHA-256, но медленно)
- **TLS legacy handshakes:** SHA-1 в certificate signatures до 2019
- **Корпоративные PKI:** старые CA с SHA-1 сертификатами
- **IoT прошивки:** ресурсы ограничены, обновления редки
- **Java keystore:** JKS использует MD5 внутри до JDK 11

**Правило:** если видите MD5/SHA-1 в security-контексте — флажок.

---

## Наивный MAC: hash(key + msg)

Предположим: `token = MD5(secret || payload)`

Выглядит разумно. На самом деле — катастрофа.

Merkle-Damgård конструкция: внутреннее состояние хэша после обработки
`secret || payload` — это и есть `MD5(secret || payload)`.

Атакующий может **продолжить** хэш: вычислить
`MD5(secret || payload || padding || extension)` без знания secret.

---

## Length Extension Attack

```
Сервер:    token = MD5(SECRET || "role=user")
Атакующий: знает token и "role=user", хочет "role=admin"

hashpump(token, "role=user", "&role=admin", len(SECRET))
→ new_token, new_payload = ("role=user" + MD5_padding + "&role=admin")

Сервер проверяет: MD5(SECRET || new_payload) == new_token  ✓
```

Атакующий добавил `&role=admin` без знания SECRET.

---

## Демо 5: Length Extension + HMAC Fix

### → Переходим к демке

```bash
python demos/05_length_extension/demo.py
```

Покажем:
1. Получить легитимный токен (`role=user`)
2. hashpumpy → расширить до `role=admin`
3. Получить флаг от сервера
4. Та же атака на HMAC-токен → fail

---

## HMAC: правильный MAC

```
HMAC(K, m) = H( (K ⊕ opad) ‖ H( (K ⊕ ipad) ‖ m ) )
```

Два уровня хэширования с ключом. Внутренний хэш «запечатан» ключом.
Length extension невозможен: атакующий не знает состояние внутреннего хэша.

```python
import hmac, hashlib

# Уязвимо:
token = hashlib.md5(secret + payload).hexdigest()

# Безопасно:
token = hmac.new(secret, payload, hashlib.sha256).hexdigest()
```

---

## Ed25519: цифровые подписи без footgun'ов

| | ECDSA (secp256k1) | Ed25519 |
|---|---|---|
| Nonce | Случайный (RNG зависимость) | Детерминированный |
| Nonce reuse | Приватный ключ скомпрометирован | Невозможно по дизайну |
| Timing | Возможны side-channels | Константное время |
| Скорость | ~0.5 ms | ~0.05 ms |
| Используется | Bitcoin, старый TLS | SSH, Signal, WireGuard, TLS 1.3 |

**Ed25519 = ECDSA без возможности выстрелить себе в ногу.**

---

## Демо 6: MD5 Collision (бонус)

```bash
python demos/06_md5_collision/demo.py
```

Два блока по 128 байт. Три отличия в битах. Один MD5.

```
MD5(BLOCK_A) = 79054025255fb1a26e4bc422aef54eb4
MD5(BLOCK_B) = 79054025255fb1a26e4bc422aef54eb4
BLOCK_A != BLOCK_B  ✓
```

Коллизия Wang et al. (2004). Стоила нескольких часов на PC 2004 года.
Сегодня: секунды на ноутбуке.

---

## Главный тезис доклада

**Все криптографические катастрофы последних 20 лет:**

| Катастрофа | Примитив | Ошибка |
|---|---|---|
| PS3 hack | ECDSA | Nonce reuse (k = const) |
| Bitcoin theft | ECDSA | Сломанный RNG (k повторяются) |
| POODLE | CBC | Padding oracle |
| Flame (2012) | MD5 | Chosen-prefix коллизия |
| ROBOT (2017) | RSA | Padding oracle (Bleichenbacher) |
| GCM атаки | AES-GCM | Nonce reuse |

**Ни один примитив не был сломан. Все ошибки — в использовании.**

---

## Q & A

**Главные правила:**
- Симметрика: AES-256-GCM или ChaCha20-Poly1305
- MAC: HMAC-SHA256, никогда не `hash(key || msg)`
- Подписи: Ed25519, или ECDSA с RFC 6979
- Хэши: SHA-256 минимум, SHA-3 или BLAKE3 для новых систем
- Не реализовывать RSA, ECDSA, CBC+MAC вручную

**Если сомневаетесь: используйте libsodium или TLS 1.3.**
