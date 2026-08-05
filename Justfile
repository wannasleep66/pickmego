lint:
    uv run mypy ./apps/auth
    uv run mypy ./apps/device
    uv run mypy ./apps/ingest
    uv run mypy ./apps/tracker

format:
    uv run ruff check --fix ./

pre-commit: lint format
    uv run pre-commit

logs:
    docker compose logs -f

dev:
    docker compose up -d
