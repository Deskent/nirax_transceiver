FROM python:3.10-alpine as builder

RUN python3 -m pip install --no-cache-dir --upgrade pip

FROM builder

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY src .

CMD gunicorn main:app --workers ${WORKERS} --timeout 120 --graceful-timeout 120 --keep-alive 5 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
