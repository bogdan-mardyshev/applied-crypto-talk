.PHONY: setup shell test smoke lint format clean help \
        demo-01 demo-02 demo-03 demo-04 demo-05 demo-06

DOCKER_COMPOSE = docker compose -f infrastructure/docker-compose.yml --project-directory .
RUN = $(DOCKER_COMPOSE) run --rm app

## setup: собрать Docker-образ и установить pre-commit хуки локально
setup:
	$(DOCKER_COMPOSE) build
	pip install pre-commit && pre-commit install

## shell: войти в bash контейнера
shell:
	$(DOCKER_COMPOSE) run --rm app bash

## test: запустить pytest внутри контейнера
test:
	$(RUN) bash -c "cd /workspace && pytest -v --tb=short"

## smoke: запустить дымовые тесты всех демок
smoke:
	$(RUN) bash -c "cd /workspace && bash scripts/run_all_demos.sh"

## lint: ruff check + mypy
lint:
	$(RUN) bash -c "cd /workspace && ruff check demos/ slides/ tests/ scripts/ && mypy demos/"

## format: black + ruff format
format:
	$(RUN) bash -c "cd /workspace && black demos/ tests/ && ruff format demos/ tests/"

## demo-01: ECB Penguin — визуализация режимов блочного шифра
demo-01:
	$(RUN) bash -c "cd /workspace && python demos/01_ecb_penguin/demo.py"

## demo-02: GCM Nonce Reuse — восстановление открытого текста при повторном nonce
demo-02:
	$(RUN) bash -c "cd /workspace && python demos/02_gcm_nonce_reuse/demo.py"

## demo-03: Textbook RSA CCA — атака выбранным шифртекстом
demo-03:
	$(RUN) bash -c "cd /workspace && python demos/03_textbook_rsa_cca/demo.py"

## demo-04: ECDSA Nonce Reuse — восстановление приватного ключа
demo-04:
	$(RUN) bash -c "cd /workspace && python demos/04_ecdsa_nonce_reuse/demo.py"

## demo-05: Length Extension — атака на схему hash(secret || msg)
demo-05:
	$(RUN) bash -c "cd /workspace && python demos/05_length_extension/demo.py"

## demo-06: MD5 Collision — два разных файла с одинаковым хэшем
demo-06:
	$(RUN) bash -c "cd /workspace && python demos/06_md5_collision/demo.py"

## clean: удалить контейнеры и кэш
clean:
	$(DOCKER_COMPOSE) down --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

## help: показать все доступные команды
help:
	@grep -E '^## ' Makefile | sed 's/## /  make /'
