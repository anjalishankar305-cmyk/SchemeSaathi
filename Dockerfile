# Multi-stage or optimized production container for SchemeSaathi
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy pre-indexed data and application code
COPY input/ ./input/
COPY data/ ./data/
COPY app/ ./app/
COPY static/ ./static/
COPY schemes_dataset.csv ./
COPY schemes_dataset.json ./
COPY Scheme_Dataset.pdf ./
COPY Scheme_Explainer_Datasets.pdf ./

EXPOSE 8000

ENV PORT=8000
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
