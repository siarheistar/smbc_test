#!/bin/bash

# Anagram Checker Test Runner Script

set -e

echo "======================================"
echo "Anagram Checker - Test Suite"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Clean previous results
echo -e "\n${YELLOW}Cleaning previous test results...${NC}"
rm -rf allure-results allure-report htmlcov .pytest_cache
mkdir -p allure-results

# Install Playwright browsers if not installed
echo -e "\n${YELLOW}Installing Playwright browsers...${NC}"
playwright install firefox

# Run Unit Tests
echo -e "\n${GREEN}Running Unit Tests...${NC}"
pytest tests/unit/ -v -m unit --cov=src --cov-report=html --cov-report=term-missing --alluredir=allure-results

# Run API Tests
echo -e "\n${GREEN}Running API Tests...${NC}"
pytest tests/api/ -v -m api --alluredir=allure-results

# Run BDD Tests (UI)
echo -e "\n${GREEN}Running BDD UI Tests with Firefox...${NC}"
pytest tests/bdd/ -v --browser firefox --alluredir=allure-results

# Run parallel test execution (Part 1 and Part 2 features)
echo -e "\n${GREEN}Running BDD Tests in Parallel with Firefox...${NC}"
pytest tests/bdd/test_anagram_ui.py -v -n 2 --browser firefox --alluredir=allure-results

# Generate Allure Report
echo -e "\n${YELLOW}Generating Allure Report...${NC}"
if command -v allure &> /dev/null; then
    allure generate allure-results --clean -o allure-report
    echo -e "${GREEN}Allure report generated in allure-report/${NC}"
    echo -e "To view the report, run: allure open allure-report"
else
    echo -e "${RED}Allure command-line tool not installed.${NC}"
    echo -e "Install it from: https://docs.qameta.io/allure/#_installing_a_commandline"
fi

echo -e "\n${GREEN}======================================"
echo "All Tests Completed!"
echo "======================================${NC}"
echo -e "Coverage report: ${YELLOW}htmlcov/index.html${NC}"
echo -e "Allure report: ${YELLOW}allure-report/index.html${NC}"
