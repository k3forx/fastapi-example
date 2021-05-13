#!/bin/bash

set -e
cd ./integration_test
pip install -r requirements.txt
pytest -v test_api_endpoints.py
