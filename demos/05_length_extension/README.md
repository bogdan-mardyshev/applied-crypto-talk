# Demo 05 — Length Extension Attack

**Владелец:** Kirill | **Блок:** Хэши, MACs, подписи

## What it demonstrates

Хэш-функции MD5, SHA-1, SHA-256 построены на конструкции Merkle-Damgård: внутреннее состояние после обработки `m` является достаточным для продолжения. Если сервер использует `token = MD5(SECRET || payload)`, атакующий может взять легитимный токен и вычислить токен для `payload + padding + "&role=admin"` — без знания SECRET. Flask-сервер демонстрирует уязвимую схему и HMAC-фикс рядом.

## How to run

```bash
# Сервер запускается автоматически в отдельном потоке
make demo-05
# или:
python demos/05_length_extension/demo.py

# Запустить сервер вручную (порт 5000):
python demos/05_length_extension/server.py
```

## Expected output

```
============================================================
  Length Extension Attack on hash(secret || msg)
============================================================

[*] Шаг 1: Логинимся как 'alice', получаем легитимный токен
    payload:    username=alice&role=user
    token:      a3f8...

[*] Шаг 2: Применяем length extension — добавляем '&role=admin'
    new_token:   d91c...
    new_payload: 'username=alice&role=user\x80\x00...\x00\x50&role=admin'

[+] АТАКА УСПЕШНА! Ответ: {"secret": "FLAG{length_extension_pwned_naive_mac}"}

  HMAC Fix:
[+] Расширенный токен валиден против HMAC: False  (ожидается False)
```

## The math

Merkle-Damgård padding добавляет `\x80 || 0x00...0x00 || length_bits` после сообщения. После этого паддинга хэш-функция обновляет своё состояние. Это состояние и есть `MD5(SECRET || msg)`.

hashpumpy знает это состояние (из `original_token`) и продолжает хэширование:

```
MD5(SECRET || msg || padding || new_data)
```

Сервер вычисляет `MD5(SECRET || new_payload)` где `new_payload = msg || padding || new_data`, и получает то же самое! Токен валиден.

**HMAC** использует два уровня хэширования:
```
HMAC(K, m) = H( (K ⊕ opad) || H( (K ⊕ ipad) || m ) )
```
Внешний хэш принимает результат внутреннего как часть сообщения — продолжить невозможно без внутреннего состояния.

## How to fix

```python
import hmac, hashlib

# Вместо:
token = hashlib.md5(secret + payload).hexdigest()  # УЯЗВИМО

# Использовать:
token = hmac.new(secret, payload, hashlib.sha256).hexdigest()  # БЕЗОПАСНО
```
