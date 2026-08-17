lint:
    #!/usr/bin/env bash
    for dir in apps/*/; do
        service=$(basename "$dir")
        echo "lint $service"
        uv run mypy "./apps/$service"
    done

format:
    uv run ruff check --fix ./

pre-commit: lint format
    uv run pre-commit

logs service:
    docker compose logs -f {{ service }}

migration service message:
    docker compose exec -it {{ service }} bash -c "cd ./apps/{{ service }} && alembic revision --autogenerate -m '{{ message }}'"

migrate service:
    docker compose exec -it {{ service }} bash -c "cd ./apps/{{ service }} && alembic upgrade head"

migrate-all:
    #!/usr/bin/env bash
    for dir in apps/*/; do
        service=$(basename "$dir")
        echo "migrate $service"
        docker compose exec -it "$service" bash -c "cd ./apps/$service && alembic upgrade head"
    done

dev:
    docker compose up -d
