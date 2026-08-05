FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=apps/auth/pyproject.toml,target=apps/auth/pyproject.toml \
    --mount=type=bind,source=packages/common/pyproject.toml,target=packages/common/pyproject.toml \
    uv sync --frozen --no-install-workspace --no-dev

ADD apps/auth/ ./apps/auth
ADD packages/common ./packages/common

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --all-packages

FROM python:3.13-slim-bookworm

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

RUN chown -R app:app /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/apps/auth /app/apps/auth
COPY --from=builder --chown=app:app /app/packages/common /app/packages/common/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/apps/auth"

USER app

CMD ["python", "-m", "apps.auth.app"]
