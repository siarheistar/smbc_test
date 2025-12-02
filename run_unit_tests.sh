#!/bin/bash

# Run only unit tests

echo "Running Unit Tests..."
pytest tests/unit/ -v -m unit --cov=src --cov-report=html --cov-report=term-missing --alluredir=allure-results
