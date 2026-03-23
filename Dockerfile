FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/
COPY app/ app/
COPY assets/ assets/
COPY run.py .

RUN pip install --no-cache-dir .

CMD exec gunicorn run:app.server --bind 0.0.0.0:$PORT --workers 2 --timeout 120
