#!/bin/bash

# Run only BDD UI tests

echo "Installing Playwright browsers..."
playwright install firefox

echo "Preparing report folder..."
mkdir -p reports

echo "Running BDD UI Tests in headed mode with Firefox..."
pytest tests/bdd/ -v --headed --browser firefox --alluredir=allure-results --cucumberjson=reports/cucumber-bdd.json --html=reports/pytest-bdd-ui.html --self-contained-html
