# Contributing

## Git Workflow

Trunk-based development. Ветка `main` защищена:
- Прямые коммиты запрещены
- Мердж только через PR с одобренным review
- CI должен быть зелёным

## Branch Naming

```
feature/<demo-id>-<short-desc>    # demo-04-ecdsa-nonce-reuse
fix/<short-desc>                   # fix-smoke-test-import
docs/<short-desc>                  # docs-timeline-update
infra/<short-desc>                 # infra-add-hashpumpy
slides/<block-id>-<short-desc>    # slides-02-rsa-cca-slide
```

## Conventional Commits

```
feat: добавить demo-04 ECDSA nonce reuse
fix: исправить импорт в smoke_test demo-01
docs: добавить speaker notes блок 2
infra: добавить hashpumpy в requirements.txt
test: добавить тест на HMAC в smoke_test demo-05
chore: обновить pre-commit hooks
slides: закончить слайды блок 3 Kirill
```

Формат: `<type>: <что сделано>` (нижний регистр, без точки в конце).

## PR Процесс

1. Создать ветку от `main`
2. Сделать коммиты
3. Открыть **Draft PR** с заполненным PULL_REQUEST_TEMPLATE
4. Перевести в **Ready for Review** когда CI зелёный
5. Назначить reviewer (по CODEOWNERS)
6. Мердж после одобрения

## Review Rules

- **12 часов** на review с момента перевода в Ready (уважаем время друг друга)
- Реально читать код, не просто одобрять
- Отвечать на **каждый** комментарий: либо fix, либо объяснение почему нет
- Мелкие замечания (опечатки, стиль) — оформлять как `nit:` чтобы reviewer мог сам решить

## Что запрещено

- Force push в `main`
- Коммит секретов (ключей, паролей, API tokens)
- Мердж с красным CI
- Открывать PR без заполненного темплейта
- Мерджить свой же PR без review (кроме hotfix за час до выступления)
