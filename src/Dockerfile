FROM python:3.9-alpine3.12

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r ./requirements.txt --no-cache-dir

COPY . /usr/src/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
