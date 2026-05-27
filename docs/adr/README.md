# Architecture Decision Records

ADR (Architecture Decision Record) — это краткая запись о значимом архитектурном решении: контекст, что решили и почему, последствия. Формат позволяет новым участникам понять почему система выглядит именно так, а не иначе.

## Как добавить новый ADR

1. Создать файл `docs/adr/NNN-short-title.md` где `NNN` — следующий номер
2. Заполнить по шаблону:

```markdown
# NNN. Заголовок

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN

## Context
Что за проблема или ситуация привела к этому решению?

## Decision
Что именно решили сделать?

## Consequences
Что становится лучше? Что хуже? Какие trade-offs?
```

3. Добавить ссылку в этот README

## Список ADR

| # | Заголовок | Статус |
|---|-----------|--------|
| [001](001-docker-environment.md) | Docker для воспроизводимой среды | Accepted |
| [002](002-ecdsa-library-choice.md) | Выбор библиотеки ecdsa для demo-04 | Accepted |
