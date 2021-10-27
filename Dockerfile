FROM python:3.9

WORKDIR /opt/events

COPY ./requirements.txt /opt/events/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /opt/events/requirements.txt

COPY ./app /opt/events/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
