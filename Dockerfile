FROM python:3.10

WORKDIR /opt/events/

# Poetry is pinned to a version compatible with this project's currently
# locked, older dependencies (e.g. packaging==21.3). Newer Poetry releases
# require packaging>=22.0 internally, which conflicts with this lockfile
# under `virtualenvs.create false` and breaks the build.
# TODO: bump this pin (or remove it) once dependencies in pyproject.toml
# are modernized at that point a newer Poetry should work fine.
RUN pip install poetry==1.7.1
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /opt/events/
RUN poetry install --without dev --no-root

COPY ./app /opt/events/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
