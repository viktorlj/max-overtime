FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    "dash>=2.18" \
    "dash-bootstrap-components>=1.6" \
    "plotly>=5.24" \
    "polars>=1.0" \
    "gunicorn>=22.0" \
    "kaleido>=0.2" \
    "xlsxwriter>=3.2" \
    "openpyxl>=3.1"

CMD exec gunicorn run:server --bind 0.0.0.0:$PORT --workers 2 --timeout 120
