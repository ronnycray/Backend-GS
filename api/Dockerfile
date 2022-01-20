FROM python:3.10.0-buster

WORKDIR /app

ENV PYTHONPATH="${PYTHONPATH}:/app" \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.7

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry -V

COPY pyproject.toml poetry.lock ./


RUN poetry export -f requirements.txt | pip install -r /dev/stdin

COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY services ./services
COPY static ./static
COPY entrypoint.sh ./entrypoint.sh

# make entrypoint.sh executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh" ]
