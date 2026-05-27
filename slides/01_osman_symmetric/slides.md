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

# Симметричная криптография: режимы и их провалы

**Student 1 — Osman**
Блок: AES, ChaCha20, ECB/CBC/GCM, GCM Nonce Reuse

---

## Что мы разберём

- Блочный vs потоковый шифр: AES и ChaCha20
- Почему **ECB — мем** (и почему это катастрофа на практике)
- Почему CBC без MAC — полубезопасность
- **AEAD** (GCM, ChaCha20-Poly1305) как правильный ответ
- Демо 1: Tux в ECB/CBC/GCM — увидим разницу визуально
- Демо 2: GCM nonce reuse — восстанавливаем открытый текст

---

## AES vs ChaCha20

| | AES-256-GCM | ChaCha20-Poly1305 |
|---|---|---|
| Тип | Блочный (16 байт) | Потоковый |
| Скорость (sw) | Медленнее без AES-NI | Быстрее везде |
| Скорость (hw) | Быстрее с AES-NI | Чуть медленнее |
| Side-channels | Timing без AES-NI | Константное время |
| Рекомендован | TLS 1.3, iOS | TLS 1.3, Android |

**Оба в TLS 1.3. Оба безопасны при правильном использовании. Ключ — в «правильном».**

---

## Режимы блочного шифра

Блочный шифр шифрует **ровно 16 байт**. Для длинных сообщений нужен **режим**.

```
ECB:  C_i = AES_K(P_i)                         ← каждый блок независимо
CBC:  C_i = AES_K(P_i ⊕ C_{i-1}), C_0 = IV    ← цепочка XOR
CTR:  C_i = P_i ⊕ AES_K(nonce ‖ counter)       ← stream cipher из block cipher
GCM:  CTR + Poly1305 MAC                         ← AEAD
```

---

## ECB: почему это мем

![height:180px](https://upload.wikimedia.org/wikipedia/commons/f/f0/Tux_ecb.jpg)

**ECB (Electronic Codebook):** одинаковые блоки открытого текста → одинаковые блоки шифртекста.

Изображение зашифровано ECB: структура пингвина **полностью видна**.

> "Используйте ECB — и ваши данные выглядят как логотип Linux"

---

## Демо 1: ECB Penguin

### → Переходим к демке

```bash
python demos/01_ecb_penguin/demo.py
```

Три варианта одного изображения:
- `tux_ecb.png` — структура видна
- `tux_cbc.png` — случайный шум
- `tux_gcm.png` — случайный шум

**ECB никогда не используйте. Ни в каком виде. Даже для «тестов».**

---

## CBC: лучше, но не достаточно

```
C_i = AES_K(P_i ⊕ C_{i-1})
```

CBC скрывает паттерны. Но:

- **Нет аутентификации** — шифртекст можно модифицировать
- **Padding Oracle** (POODLE, Lucky 13) — атаки на CBC + PKCS#7
- Нужен отдельный MAC (Encrypt-then-MAC)

Правило: **если вы пишете CBC + MAC вручную — вы уже делаете ошибку**

---

## AEAD: правильный ответ

**AEAD = Authenticated Encryption with Associated Data**

```python
# ChaCha20-Poly1305
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

key = ChaCha20Poly1305.generate_key()
nonce = os.urandom(12)
ct = ChaCha20Poly1305(key).encrypt(nonce, plaintext, aad)
pt = ChaCha20Poly1305(key).decrypt(nonce, ct, aad)  # InvalidTag если изменён
```

Один примитив = шифрование + целостность + аутентичность.
**Дефолт в 2024: AES-256-GCM или ChaCha20-Poly1305.**

---

## GCM Nonce Reuse: катастрофа

GCM — это stream cipher (`CTR-mode`). Keystream зависит только от `(K, nonce)`.

```
C₁ = P₁ ⊕ KeyStream(K, N)
C₂ = P₂ ⊕ KeyStream(K, N)  ← тот же nonce!
────────────────────────────
C₁ ⊕ C₂ = P₁ ⊕ P₂
```

**Один повторный nonce = раскрытие XOR двух открытых текстов.**
Знаешь одно сообщение → знаешь второе.
**Forbidden Attack** → восстановление ключа аутентификации → подделка тегов.

---

## Демо 2: GCM Nonce Reuse

### → Переходим к демке

```bash
python demos/02_gcm_nonce_reuse/demo.py
```

Покажем:
1. Два разных сообщения, один `(K, nonce)` → одинаковый keystream
2. `C₁ ⊕ C₂ == P₁ ⊕ P₂` — keystream сокращается
3. Восстановление `P₂` из `P₁` и двух шифртекстов

---

## Как фиксить

| Ошибка | Правильно |
|--------|-----------|
| ECB для шифрования | AES-GCM / ChaCha20-Poly1305 |
| CBC без MAC | Encrypt-then-HMAC или AEAD |
| Статический / counter nonce в GCM | `os.urandom(12)` каждый раз |
| «Придумать свой режим» | Использовать TLS/libsodium |

**Криптография — это не выбор алгоритма, это выбор конструкции и режима.**

---

## Переход к Bogdan

Симметричная криптография — это **разделённый секрет**: обе стороны знают ключ.

**Вопрос:** как безопасно договориться о ключе в первый раз по открытому каналу?

→ Богдан расскажет про **асимметричную криптографию** и **Diffie-Hellman**.
