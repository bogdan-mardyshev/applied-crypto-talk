# Applied Cryptography Talk

> Командный учебный доклад: misuse-паттерны в криптографии — почему все катастрофы последних 20 лет это не взлом примитива, а ошибки использования.

## Quick Start

```bash
git clone <repo-url>
cd applied-crypto-talk
make setup   # собирает Docker-образ и устанавливает pre-commit hooks
make test    # запускает все pytest тесты внутри контейнера
make smoke   # запускает smoke-тесты всех 6 демок
```

> Docker должен быть установлен. После `make setup` всё запускается одной командой — никаких «у меня работает» разночтений.

---

## Структура проекта

```
applied-crypto-talk/
├── demos/                   # 6 демонстрационных атак
│   ├── 01_ecb_penguin/      # ECB vs CBC vs GCM на изображении
│   ├── 02_gcm_nonce_reuse/  # Восстановление открытого текста
│   ├── 03_textbook_rsa_cca/ # CCA атака на RSA без паддинга
│   ├── 04_ecdsa_nonce_reuse/ # Восстановление приватного ключа ECDSA
│   ├── 05_length_extension/ # Flask сервер + hashpumpy атака
│   └── 06_md5_collision/    # Коллизия Wang et al. (2004)
├── slides/                  # Marp-совместимые слайды
│   ├── 01_osman_symmetric/
│   ├── 02_bogdan_asymmetric/
│   └── 03_kirill_hashes/
├── docs/                    # ARCHITECTURE, CONTRIBUTING, TIMELINE, ADR
├── infrastructure/          # Dockerfile, docker-compose.yml, requirements.txt
├── tests/                   # conftest.py
└── scripts/                 # run_all_demos.sh
```

---

## Команда

| Участник | Роль | Зона ответственности |
|---------|------|---------------------|
| **Bogdan** | Tech Lead + Student 2 | Инфраструктура, demo-03 (RSA CCA), demo-04 (ECDSA), блок 2 слайдов |
| **Kirill** | Student 3 | demo-05 (Length Extension), demo-06 (MD5 Collision), блок 3 слайдов |
| **Osman** | Student 1 | demo-01 (ECB Penguin), demo-02 (GCM Nonce Reuse), блок 1 слайдов |

---

## Демонстрации

| # | Демка | Владелец | Что показывает |
|---|-------|---------|----------------|
| 01 | ECB Penguin | Osman | AES-ECB сохраняет паттерны изображения |
| 02 | GCM Nonce Reuse | Osman | Повторный nonce раскрывает открытый текст |
| 03 | Textbook RSA CCA | Bogdan | Мультипликативность RSA → атака через oracle |
| 04 | ECDSA Nonce Reuse | Bogdan | Повторный k → восстановление приватного ключа |
| 05 | Length Extension | Kirill | hash(secret‖msg) позволяет подделать токен |
| 06 | MD5 Collision | Kirill | Два разных файла, один MD5 хэш |

---

## Workflow

```
Issue → ветка feature/<demo-id>-<desc> → реализация → PR → review → мердж в main
```

Подробнее: [CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## Полезные ссылки

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — технические решения и обоснования
- [CONTRIBUTING.md](docs/CONTRIBUTING.md) — git workflow и правила review
- [TIMELINE.md](docs/TIMELINE.md) — 7-дневный план с чек-листами
- [docs/adr/](docs/adr/) — Architecture Decision Records

---

## Дедлайн

**7 дней** с момента создания репозитория. День 7 — выступление.
Критический путь: demo-04 (ECDSA) → сложнее всего, делать первым.
