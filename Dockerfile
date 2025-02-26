FROM python:3.10-slim

RUN apt update && apt install -y \
    chromium-driver \
    chromium \
    && pip install --upgrade pip setuptools wheel

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

COPY .env /app/.env

RUN mkdir -p /app/logs

CMD ["python", "main.py"]
