FROM python:3.12

WORKDIR /code

COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock

RUN pip install pipenv && pipenv sync --system

COPY ./app /code/app

ADD https://truststore.pki.us-gov-west-1.rds.amazonaws.com/global/global-bundle.pem \
    /usr/local/share/ca-certificates/global-bundle.pem

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
