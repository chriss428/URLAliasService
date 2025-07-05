FROM python:3.13-alpine AS builder

WORKDIR /usr/local/myapp

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

FROM python:3.13-alpine

WORKDIR /usr/local/myapp

COPY --from=builder /usr/local /usr/local

COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["sh", "-c", "sleep 5 && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
