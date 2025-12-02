# FROM python:3.11.4 AS builder

# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1
# WORKDIR /app


# RUN python -m venv .venv
# COPY requirements.txt ./
# RUN .venv/bin/pip install -r requirements.txt
# FROM python:3.11.4-slim
# WORKDIR /app
# COPY --from=builder /app/.venv .venv/
# COPY . .
# CMD ["/app/.venv/bin/fastapi", "run"]

# Dockerfile
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Fly sets PORT at runtime; use a shell to expand it with a default for local builds
CMD ["sh", "-c", "uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
