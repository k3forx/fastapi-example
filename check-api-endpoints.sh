#!/bin/bash

set -e
pip3 install -r ./app/requirements.test.txt

if [[ ${AUTH_SECRET_KEY} = '' ]]; then
  echo "Generate secret key for authorization"
  AUTH_SECRET_KEY=$(openssl rand -hex 32)
else
  echo "Secret key for authorization is already generated"
fi

echo "Register a new user"
STATUS_CODE=$(curl -X POST -H "Content-Type: application/json" -d '{"username": "test", "raw_password": "test"}' localhost:8000/register -o /dev/null -w '%{http_code}\n' -s)
if [[ ${STATUS_CODE} = 200 ]]; then
  echo "The user is successfully created"
else
  echo "The user already exists"
fi

echo "Start testing..."
pytest -vvv ./app/integration_test/test_api_endpoints.py
