FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.7.12-bookworm-slim /usr/local/bin/ /bin/
WORKDIR /app
COPY .python-version pyproject.toml uv.lock .
RUN uv sync --locked --no-cache --no-dev
COPY . .
CMD ["uv", "run", "streamlit", "run", "src/app.py"]


FROM base AS testing
ENV MLMODEL_URI=ommited-in-unit-testing
ENV MLMODELS_DIR=ommited-in-unit-testing
COPY . .
CMD ["echo", "testing..."]
# CMD ["pytest", "-q", "--tb=short", "--disable-warnings"]


FROM base AS service
ENV ASSETS_DIR=/assets
ENV MLMODELS_DIR=/models
ENV PYTHONPATH=/app
COPY assets/ /assets/
COPY src/ .
CMD ["sh", "-c", "uv run fastapi run /app/app.py --port ${PORT:-80}"]
