# Stage 1 — install dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install --no-cache-dir -r requirements.txt


# Stage 2 — runtime image
FROM python:3.12-slim AS runner

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app/ ./app/

# SQLite data directory
RUN mkdir -p /app/data

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
