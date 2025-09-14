# ----------------------
# Stage 1: Build deps
# ----------------------
FROM python:3.11-slim AS builder

# Set work directory
WORKDIR /app

# Install system deps (for pip, psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt .

# Install Python deps to a temp dir (cached layer)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ----------------------
# Stage 2: Runtime image
# ----------------------
FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI with Gunicorn + Uvicorn workers
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
