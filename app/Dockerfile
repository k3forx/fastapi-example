FROM python:3.9-alpine3.12

WORKDIR /usr/src

COPY ./requirements.txt /usr/src/requirements.txt

RUN pip install -r ./requirements.txt --no-cache-dir

COPY main.py /usr/src/main.py
COPY mysql_client.py /usr/src/mysql_client.py
COPY api /usr/src/api
COPY log_config.json /usr/src/log_config.json

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "log_config.json", "--reload"]
