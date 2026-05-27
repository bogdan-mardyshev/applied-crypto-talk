# ONBOARDING — Добро пожаловать в applied-crypto-talk

Привет, Kirill и Osman! 👋

Это онбординг-документ. Прочитай **один раз** от начала до конца —
после него у тебя будет понимание что делать, как делать и зачем.

---

## Статус репозитория

| Что готово (инфраструктура) | Что делаете вы (контент) |
|---|---|
| ✅ Docker-среда | 🔲 Реализация demo.py (6 штук) |
| ✅ GitHub Actions CI | 🔲 Слайды (slides.md) |
| ✅ Makefile команды | 🔲 Speaker notes |
| ✅ pre-commit хуки | 🔲 Fallback-видео |
| ✅ Структура демок | 🔲 Хронометраж |
| ✅ Smoke-тесты (контракт) | |
| ✅ Документация | |

**Репозиторий готов к работе СЕЙЧАС.**
Ваша задача — реализовать функции в `demo.py` и написать слайды.

---

## Быстрый старт (5 минут)

```bash
# 1. Клонировать репо (после того как Bogdan пушнет на GitHub и добавит вас)
git clone https://github.com/<bogdan-github>/applied-crypto-talk
cd applied-crypto-talk

# 2. Поднять среду
make setup          # собирает Docker образ + pre-commit hooks (~3-5 мин первый раз)

# 3. Убедиться что тесты запускаются (будут красными — это нормально!)
make test
# Увидишь: NotImplementedError — это ваши задачи

# 4. Войти в контейнер и работать там
make shell
python demos/04_ecdsa_nonce_reuse/demo.py
```

> 💡 **Почему Docker?** У нас три человека на Mac/Win/Linux.
> Без Docker: «у меня работает» × 3 = три разных бага.
> С Docker: одна среда для всех.

---

## Структура репозитория

```
applied-crypto-talk/
├── demos/                    ← ЗДЕСЬ ВАША ОСНОВНАЯ РАБОТА
│   ├── 01_ecb_penguin/       ← Osman
│   ├── 02_gcm_nonce_reuse/   ← Osman
│   ├── 03_textbook_rsa_cca/  ← Bogdan
│   ├── 04_ecdsa_nonce_reuse/ ← Bogdan
│   ├── 05_length_extension/  ← Kirill
│   └── 06_md5_collision/     ← Kirill
│
├── slides/                   ← ЗДЕСЬ СЛАЙДЫ
│   ├── 01_osman_symmetric/
│   ├── 02_bogdan_asymmetric/
│   └── 03_kirill_hashes/
│
├── docs/                     ← документация (уже написана)
├── infrastructure/           ← Docker, requirements (не трогать)
├── Makefile                  ← все команды здесь
└── .github/                  ← CI, templates (не трогать)
```

---

## Как работать с демками

Каждая демка состоит из трёх файлов:

```
demos/XX_name/
├── demo.py        ← ТВОЙ ФАЙЛ: реализуй функции
├── smoke_test.py  ← тесты: они определяют что должно работать
└── README.md      ← объяснение задачи, математика, как фиксить
```

### Рабочий цикл:

```
1. Читаешь README.md демки         ← понимаешь задачу
2. Читаешь demo.py                 ← видишь скелет + docstrings с математикой
3. Реализуешь функции              ← убираешь NotImplementedError
4. Запускаешь локально:
   python demos/04_ecdsa_nonce_reuse/demo.py
5. Запускаешь тест:
   pytest demos/04_ecdsa_nonce_reuse/smoke_test.py -v
6. Тест зелёный → открываешь PR   ← см. Git Workflow ниже
```

> ⚠️ **Важно:** smoke_test.py — это контракт. Он говорит что должно работать.
> Не меняй smoke_test.py под свою реализацию — меняй реализацию под тест.

---

## Задачи по блокам

### Osman — Блок 1: Симметричное шифрование

**Демки:**

| Файл | Что реализовать | Ключевой вопрос |
|---|---|---|
| `demos/01_ecb_penguin/demo.py` | `encrypt_ecb()`, `encrypt_cbc()`, `encrypt_gcm()` | Почему ECB "читаемый"? |
| `demos/02_gcm_nonce_reuse/demo.py` | `xor_bytes()`, `encrypt_gcm()`, `attack_nonce_reuse()` | Почему CT1⊕CT2 = PT1⊕PT2? |

**Что нужно понять:**
- Чем отличается блочный шифр от потокового?
- Что такое keystream и почему GCM его повторяет при одном nonce?
- Почему CBC лучше ECB, но хуже GCM?

**Минимальный чекпоинт:**
```bash
python demos/01_ecb_penguin/demo.py    # три PNG файла
python demos/02_gcm_nonce_reuse/demo.py # "Атака успешна: True"
```

**Полезные ресурсы:**
- [Cryptopals Set 1](https://cryptopals.com/) — задачи 1-6, практика
- Dan Boneh "Cryptography I" на Coursera, Week 2 — блочные шифры
- Wikipedia "Block cipher mode of operation" — с картинками
- [crypto.stackexchange.com/q/2169](https://crypto.stackexchange.com/questions/2169) — GCM nonce reuse

---

### Bogdan — Блок 2: Асимметричная криптография

**Демки:**

| Файл | Что реализовать | Ключевой вопрос |
|---|---|---|
| `demos/03_textbook_rsa_cca/demo.py` | `rsa_encrypt()`, `rsa_decrypt()`, `cca_attack()` | Как мультипликативность ломает RSA? |
| `demos/04_ecdsa_nonce_reuse/demo.py` | `ecdsa_sign_with_k()`, `ecdsa_verify()`, `recover_private_key()` | Как из двух подписей вывести уравнение для d? |

**Что нужно понять:**
- Почему `pow(m, e, n)` это RSA, но это не безопасно?
- Что такое скалярное умножение на эллиптической кривой `k * G`?
- Как связаны `r`, `s`, `k`, `d` в ECDSA?

**Минимальный чекпоинт:**
```bash
python demos/03_textbook_rsa_cca/demo.py   # "Атака успешна: True"
python demos/04_ecdsa_nonce_reuse/demo.py  # "recovered_d == PRIVATE_KEY_D → True"
```

**Полезные ресурсы:**
- Dan Boneh "Cryptography I" Week 6 — RSA и паддинг
- [blog.trailofbits.com/2020/06/11/ecdsa-handles-the-truth](https://blog.trailofbits.com/2020/06/11/ecdsa-handles-the-truth/) — разбор ECDSA атак
- Документация библиотеки `ecdsa`: [github.com/tlsfuzzer/python-ecdsa](https://github.com/tlsfuzzer/python-ecdsa)
- fail0verflow PS3 слайды: [media.ccc.de/v/27c3-4087](https://media.ccc.de/v/27c3-4087-en-console_hacking_2010)

---

### Kirill — Блок 3: Хэши, MAC, подписи

**Демки:**

| Файл | Что реализовать | Ключевой вопрос |
|---|---|---|
| `demos/05_length_extension/server.py` | `make_vulnerable_token()`, `make_safe_token()` | Чем HMAC принципиально отличается от hash(key\|\|msg)? |
| `demos/05_length_extension/demo.py` | `attack_length_extension()` | Как hashpumpy продолжает хэш без знания секрета? |
| `demos/06_md5_collision/demo.py` | `find_collision()` | Как birthday attack находит коллизию? |

**Что нужно понять:**
- Что такое Merkle-Damgård конструкция и почему она уязвима?
- Почему `hmac.new(key, msg, md5)` безопасен, а `md5(key + msg)` нет?
- Что такое birthday bound и как считается 2^(n/2)?

**Минимальный чекпоинт:**
```bash
python demos/05_length_extension/demo.py  # "АТАКА УСПЕШНА"
python demos/06_md5_collision/demo.py     # коллизия за <100ms
```

**Полезные ресурсы:**
- [blog.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks](https://blog.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks) — доступное объяснение
- hashpumpy docs: `python3 -c "import hashpumpy; help(hashpumpy.hashpump)"`
- [sha-mbles.github.io](https://sha-mbles.github.io/) — chosen-prefix SHA-1 коллизия
- Dan Boneh "Cryptography I" Week 5 — MAC и collision resistance

---

## Git Workflow

```bash
# 1. Создать ветку для своей задачи
git checkout -b feature/demo-01-ecb-penguin

# 2. Реализовать, проверить
python demos/01_ecb_penguin/demo.py
pytest demos/01_ecb_penguin/smoke_test.py -v

# 3. Закоммитить
git add demos/01_ecb_penguin/demo.py
git commit -m "feat: реализовать demo-01 ECB penguin"

# 4. Пушнуть и открыть PR
git push origin feature/demo-01-ecb-penguin
# GitHub → New Pull Request → заполнить шаблон

# 5. Ждать review (12 часов максимум)
```

**Правила:**
- Одна ветка = одна задача
- PR всегда через шаблон (`.github/PULL_REQUEST_TEMPLATE.md`)
- Мержить только после review
- CI должен быть зелёным перед мержем

---

## Полезные команды

```bash
make shell         # войти в Docker контейнер
make test          # запустить все тесты
make demo-04       # запустить конкретную демку
make lint          # проверить стиль кода
make format        # автоформатирование

# Внутри контейнера:
pytest demos/04_ecdsa_nonce_reuse/smoke_test.py -v   # один тест
pytest -k "test_collision" -v                         # по имени теста
python demos/04_ecdsa_nonce_reuse/demo.py            # запустить демку
```

---

## FAQ

**Q: Тесты красные. Это нормально?**
A: Да! Все тесты красные до тех пор пока ты не реализуешь функции.
Красный тест = «вот что нужно сделать». Зелёный тест = «готово».

**Q: Можно ли посмотреть примеры реализации в интернете?**
A: Да, это учебный проект. Главное — понять КАК работает атака, а не скопировать.
Если смотришь готовый код — разберись в нём, потом напиши свой.

**Q: Как понять правильную математику?**
A: Читай docstring в demo.py — там расписаны формулы. Читай README.md демки —
там объяснён математический смысл. Если непонятно — спроси в команде.

**Q: У меня другая ОС, Docker не ставится.**
A: Попробуй установить зависимости напрямую:
```bash
pip install -r infrastructure/requirements.txt
python demos/04_ecdsa_nonce_reuse/demo.py
```
Если не работает — скажи Bogdan'у, разберёмся.

**Q: Когда нужно записывать fallback-видео?**
A: День 6. Сначала сделай рабочую демку, потом запись.
Формат: `demos/XX_name/fallback/demo.mp4`

---

## Чеклист первого дня

- [ ] Клонировал репо
- [ ] `make setup` прошёл без ошибок
- [ ] `make test` запускается (тесты красные — OK)
- [ ] Прочитал README.md своих демок
- [ ] Создал ветку для первой задачи
- [ ] Написал хотя бы одну функцию и запустил тест

---

## Контакт

Вопросы → Telegram или создай GitHub Issue с тегом `question`.
Срочные вопросы (за 2 дня до выступления) → Bogdan напрямую.

**Удачи! Проект крутой — криптографические атаки это то что реально работает в production.**
