# Build Stage
FROM --platform=linux/amd64 python:3.10-slim-bullseye AS builder
USER root

# 1. Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Install uv directly into the path
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# 3. Create an app directory and copy requirements
WORKDIR /app
COPY requirements.txt .

# 4. Use uv to install dependencies into the system's Python site-packages
RUN uv pip install --no-cache --system -r requirements.txt

# Final Stage
FROM --platform=linux/amd64 python:3.10-slim-bullseye

# 1. Install only the RUNTIME system dependencies (e.g., libpq5 for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copy the installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
# Also copy any executable scripts installed by packages (e.g., uvicorn)
COPY --from=builder /usr/local/bin /usr/local/bin

# 3. Copy the application code and expose the port app
COPY app .
EXPOSE 8082

# 4. Command to run the FastAPI app
ENTRYPOINT ["python", "main.py"]