FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD sh -c 'uvicorn service:app --host 0.0.0.0 --port $PORT'
