FROM python:3.12-slim-bookworm

WORKDIR /opt/events/

RUN pip install --no-cache-dir poetry==1.8.5
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /opt/events/
RUN poetry install --only main

COPY ./app /opt/events/app

RUN useradd --create-home appuser && chown -R appuser:appuser /opt/events
USER appuser

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
