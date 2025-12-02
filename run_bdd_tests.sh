#!/bin/bash

# Run only BDD UI tests

echo "Installing Playwright browsers..."
playwright install firefox

echo "Running BDD UI Tests in headed mode with Firefox..."
pytest tests/bdd/ -v --headed --browser firefox --alluredir=allure-results
