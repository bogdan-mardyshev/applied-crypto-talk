---
name: Demo task
about: Реализация или улучшение одной из демонстраций
labels: demo
---

## Goal

<!-- Что должна демонстрировать атака/уязвимость после закрытия issue -->

## Acceptance criteria

- [ ] `demo.py` запускается без ошибок в Docker-контейнере
- [ ] Smoke-тест проходит: `pytest demos/XX_*/smoke_test.py -v`
- [ ] README.md содержит разделы What / How to run / Expected output / The math / How to fix
- [ ] Все значения детерминированы (seed / hardcoded keys)
- [ ] Fallback-видео записано в `demos/XX_name/fallback/`
- [ ] PR создан, CI зелёный

## Estimate

<!-- Примерное количество часов: X ч -->

## Dependencies

<!-- Issues или PRs, которые должны быть закрыты до этого -->

## Notes

<!-- Ссылки на papers, PoC-репо, специфика библиотек -->
