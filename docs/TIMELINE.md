# Timeline — 7-Day Plan

Дедлайн: выступление на день 7.

---

## Day 1 — Foundation

**Богдан (утром, 2–3 часа):**
- [ ] `git init`, создать репозиторий на GitHub
- [ ] Настроить branch protection на `main`
- [ ] Добавить Osman и Kirill как collaborators
- [ ] Залить scaffold (этот репозиторий)
- [ ] Убедиться что `make setup && make test` у всех работает

**Все (днём + вечером):**
- [ ] Установить Docker
- [ ] Сделать `make setup` — убедиться что собирается
- [ ] Прочитать README.md и CONTRIBUTING.md
- [ ] Каждый создаёт свою первую ветку (`feature/init-<имя>`) и открывает пустой PR

**Чек дня:**
- [ ] Все трое могут запустить `make test` локально
- [ ] GitHub Actions запускается при открытии PR

---

## Day 2 — Core Demos (часть 1)

**Osman:**
- [ ] `feature/demo-01-ecb-penguin` — завершить demo.py и smoke_test.py
- [ ] Скачать Tux PNG, добавить в assets/
- [ ] `make demo-01` показывает три картинки

**Bogdan:**
- [ ] `feature/demo-04-ecdsa-nonce-reuse` — завершить demo.py и smoke_test.py
- [ ] `make demo-04` показывает успешную атаку

**Kirill:**
- [ ] `feature/demo-06-md5-collision` — завершить demo.py и smoke_test.py
- [ ] `make demo-06` показывает коллизию

**Чек дня:**
- [ ] Три демки работают локально в Docker
- [ ] Smoke тесты зелёные для demo-01, demo-04, demo-06

---

## Day 3 — Core Demos (часть 2) + первые PRs

**Osman:**
- [ ] `feature/demo-02-gcm-nonce-reuse` — завершить demo.py и smoke_test.py
- [ ] Открыть PR для demo-01, пройти review у Bogdan
- [ ] Мердж demo-01

**Bogdan:**
- [ ] `feature/demo-03-textbook-rsa-cca` — завершить demo.py и smoke_test.py
- [ ] Открыть PR для demo-04, review у Kirill
- [ ] Мердж demo-04

**Kirill:**
- [ ] `feature/demo-05-length-extension` — server.py + demo.py + smoke_test.py
- [ ] Проверить что hashpumpy атака работает end-to-end
- [ ] Review PR Bogdan'a (demo-04)

**Чек дня:**
- [ ] demo-01, demo-04 в main
- [ ] Все 6 демок работают локально

---

## Day 4 — Все демки в main + старт слайдов

**Osman:**
- [ ] PR для demo-02 → review → мердж
- [ ] Начать `slides/01_osman_symmetric/slides.md`

**Bogdan:**
- [ ] PR для demo-03 → review → мердж
- [ ] Дополнить `slides/02_bogdan_asymmetric/slides.md`

**Kirill:**
- [ ] PR для demo-05 и demo-06 → review → мердж
- [ ] Начать `slides/03_kirill_hashes/slides.md`

**Чек дня:**
- [ ] `make smoke` — все 6 демок проходят
- [ ] Черновики слайдов у каждого есть

---

## Day 5 — Финализация слайдов + первая полная репетиция

**Все:**
- [ ] Финализировать слайды своего блока
- [ ] Заполнить speaker_notes.md
- [ ] Прогнать свой блок соло, замерить время

**Совместно (вечером ~2 часа):**
- [ ] Первая полная репетиция доклада подряд
- [ ] Внести хронометраж в `docs/timing.md`
- [ ] Список правок после репетиции → issues

**Чек дня:**
- [ ] Слайды всех трёх блоков в main
- [ ] Первый замер времени в timing.md

---

## Day 6 — Polish + Fallback-видео + вторая репетиция

**Все (днём):**
- [ ] Исправить замечания после репетиции
- [ ] Записать fallback-видео для каждой демки (`demos/XX/fallback/demo.mp4`)
- [ ] Проверить переходы между блоками

**Совместно (вечером ~2 часа):**
- [ ] Вторая полная репетиция с таймером
- [ ] Внести хронометраж в `docs/timing.md`
- [ ] Финальный `make smoke` — всё зелёное

**Чек дня:**
- [ ] 6 fallback-видео записано
- [ ] Второй замер в timing.md
- [ ] Итоговое время < лимит

---

## Day 7 — Final Rehearsal + Выступление

**За 2 часа до:**
- [ ] Финальная репетиция (без остановок)
- [ ] Проверить Docker на машине выступления
- [ ] Открыть fallback-видео в отдельном окне

**Выступление:**
- [ ] Osman: блок 1 (~11 мин)
- [ ] Bogdan: блок 2 (~14 мин)
- [ ] Kirill: блок 3 (~11 мин)
- [ ] Q&A: ~10 мин

---

## Критический путь

`demo-04` (ECDSA) — самая сложная демка. Если что-то пойдёт не так, первым ломать Bogdan.

`demo-05` (Length Extension) — зависит от Flask. Проверить что порт 5000 свободен на машине выступления.
