# ===============================
# Base image
# ===============================
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ===============================
# Install system dependencies
# ===============================
RUN apt-get update && apt-get install -y \
build-essential \
curl \
&& rm -rf /var/lib/apt/lists/*

# ===============================
# Install python dependencies
# ===============================
COPY pyproject.toml ./

RUN pip install --upgrade pip && \
pip install .

# ===============================
# Copy source
# ===============================
COPY app ./app

# ===============================
# Expose port
# ===============================
EXPOSE 8000

# ===============================
# Run server
# ===============================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]