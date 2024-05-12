include .env

compose = docker compose

up:
	sudo $(compose) -f docker-compose.yaml up --build -d

logs:
	sudo $(compose) logs -f --no-log-prefix api

logs-db:
	sudo $(compose) logs -f db

down:
	sudo $(compose) down

shell:
	sudo $(compose) exec api python -m ptpython

shell-sql:
	sudo $(compose) exec db psql postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_SERVER):$(POSTGRES_PORT)/$(POSTGRES_DB)

revision:
	sudo $(compose) exec api python -m alembic revision --autogenerate

upgrade:
	sudo $(compose) exec api python -m alembic upgrade +1

upgrade-head:
	sudo $(compose) exec api python -m alembic upgrade head

downgrade:
	sudo $(compose) exec api python -m alembic downgrade -1

clean-migrations:
	find . -path "*/alembic/versions/*.py" -not -path "*/venv/*" -not -path "*/__init__.py" -delete

clean-db:
	rm -rf .docker/postgres

clean: clean-db clean-migrations

restart: down up

create-admin:
	sudo $(compose) exec api python src/scripts/admin.py
