#!/bin/bash

# Run only API tests

echo "Running API Tests..."
pytest tests/api/ -v -m api --alluredir=allure-results
