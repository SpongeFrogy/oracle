FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY patch.py .
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 patch.py

COPY . .


CMD ["python3", "main.py"]