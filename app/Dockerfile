# Stage 1: Build dependencies in an isolated prefix
FROM python:3.9-slim AS builder

WORKDIR /install

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Minimal runtime container
FROM python:3.9-slim

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application source code
COPY . .

# Set environment path so Python imports work seamlessly
ENV PYTHONPATH=/app

EXPOSE 8000

# Default command (will be overridden by Docker Compose for Celery)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]