# syntax = docker/dockerfile:1.4

# ── Builder Stage ──
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user --no-warn-script-location -r requirements.txt

# ── Runtime Stage ──
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ ./app/
COPY alembic.ini ./
COPY alembic/ ./alembic/

# Create SQLite database directory
RUN mkdir -p /data
ENV DATABASE_URL=sqlite:////data/wine.db

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import http.client; c=http.client.HTTPConnection('localhost',8000); c.request('GET','/health'); exit(0 if c.getresponse().status==200 else 1)"

CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
