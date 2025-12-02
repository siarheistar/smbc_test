#!/bin/bash

# Run BDD tests in parallel (Part 1 and Part 2 features)
# Note: Headed mode doesn't work well with parallel execution
# Use headless mode for parallel tests

echo "Installing Playwright browsers..."
playwright install firefox

echo "Running BDD Tests in Parallel (2 workers) with Firefox..."
pytest tests/bdd/test_anagram_ui.py -v -n 2 --browser firefox --alluredir=allure-results

echo "Parallel test execution completed!"
