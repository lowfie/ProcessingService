include .env

compose = docker compose

init: up revision upgrade-head create-admin

up:
	$(compose) -f docker-compose.yaml up --build -d

logs:
	$(compose) logs -f --no-log-prefix api

logs-db:
	$(compose) logs -f db

down:
	$(compose) down

shell:
	$(compose) exec api python -m ptpython

shell-sql:
	$(compose) exec db psql postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_SERVER):$(POSTGRES_PORT)/$(POSTGRES_DB)

revision:
	$(compose) exec api python -m alembic revision --autogenerate

upgrade:
	$(compose) exec api python -m alembic upgrade +1

upgrade-head:
	$(compose) exec api python -m alembic upgrade head

downgrade:
	$(compose) exec api python -m alembic downgrade -1

clean-migrations:
	find . -path "*/alembic/versions/*.py" -not -path "*/venv/*" -not -path "*/__init__.py" -delete

clean: clean-migrations

restart: down up

create-admin:
	$(compose) exec api python src/scripts/admin.py
