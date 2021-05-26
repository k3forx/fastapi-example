#!/bin/bash

set -e
pip3 install -r ./app/requirements.test.txt
echo "Start testing..."
pytest -vv ./app/integration_test/test_api_endpoints.py
