#!/bin/bash

set -e
cd ./integration_test
pip install -r requirements.txt
pytest test_api_endpoints.py
