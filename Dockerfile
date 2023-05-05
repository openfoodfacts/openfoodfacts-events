FROM python:3.10

WORKDIR /opt/events/

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY alembic.ini pyproject.toml poetry.lock /opt/events/
RUN poetry install --no-dev

COPY ./app ./alembic /opt/events/app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
