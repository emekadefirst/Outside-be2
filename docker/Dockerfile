FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Disable bytecode compilation to avoid BuildKit timeout
ENV UV_COMPILE_BYTECODE=0
ENV UV_LINK_MODE=copy
ENV PYTHONDONTWRITEBYTECODE=1

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy project code
COPY . /app

# Install project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

EXPOSE 8080
CMD ["gunicorn", "src.server:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]
