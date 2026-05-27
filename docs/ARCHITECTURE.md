# Architecture

## Tech Stack

### Docker
Всё запускается внутри контейнера. Три участника на Mac, Windows и Linux — Docker гарантирует одинаковую среду. Без Docker: «у меня работает» × 3 человека = 3 разных баги.

Образ: `python:3.11-slim` + build-essential для компиляции cryptography (C-расширения).

### Python 3.11
- Встроенный `tomllib` (не нужен `toml`)
- `pow(a, -1, n)` — модульное обращение в стандартной библиотеке (нужно для ECDSA демки)
- Улучшенные error messages

### Ключевые библиотеки

| Библиотека | Зачем | Альтернативы отброшены |
|---|---|---|
| `cryptography` | AES-GCM, ChaCha20, Ed25519 — production-grade | `pycryptodome` хуже API |
| `pycryptodome` | AES-ECB/CBC для demo-01 (Cipher API) | `cryptography` также работает |
| `ecdsa` | Demo-04: доступ к промежуточным значениям (k, r, s) | `coincurve` не даёт сырой k |
| `hashpumpy` | Demo-05: length extension | Вручную было бы сложнее и ненаглядно |
| `Pillow` | Demo-01: работа с PNG пикселями | OpenCV — лишняя зависимость |
| `Flask` | Demo-05: уязвимый веб-сервер | FastAPI — overkill для одной демки |

### ruff + black
Два инструмента потому что ruff — linter (ошибки), black — formatter (стиль). ruff format пока не полностью заменяет black для исторических проектов.

---

## Структура demos/

Каждая демка — самостоятельный модуль:

```
demos/XX_name/
├── demo.py        — runnable скрипт, main() на последней строке
├── smoke_test.py  — pytest, проверяет что демка работает корректно
├── README.md      — What / How to run / Expected output / Math / Fix
└── assets/        — статические файлы (только demo-01)
```

**Принципы:**
- `demo.py` должен запускаться без аргументов: `python demo.py`
- Все значения детерминированы: никаких `os.urandom()` в критическом пути
- `smoke_test.py` — gate перед мерджем, должен проходить в CI

---

## Структура slides/

```
slides/NN_name/
├── slides.md        — Marp-совместимый Markdown
└── speaker_notes.md — заметки докладчика с тайминговыми ориентирами
```

Marp: `npx @marp-team/marp-cli slides.md --html -o slides.html`

---

## Принципы

**Детерминированность демок:** все ключи, nonce, приватные ключи — константы. Демка запускается 10 раз — 10 одинаковых выводов. Это упрощает отладку и запись fallback-видео.

**Smoke-тесты как gate:** CI не пройдёт пока хоть один smoke_test.py красный. Это предотвращает мердж сломанного кода перед выступлением.

**Fallback-видео:** если на выступлении что-то упадёт (библиотека, Docker, сеть), использовать заранее записанное видео из `demos/XX_name/fallback/`. Записывать на день 6.
