.PHONY: help install setup run check-venv test test-unit test-api test-bdd test-parallel clean coverage report lint

help:
	@echo "Anagram Checker - Available Commands"
	@echo "===================================="
	@echo "make install      - Install dependencies"
	@echo "make setup        - Complete setup (venv + deps + browsers)"
	@echo "make run          - Start the application"
	@echo "make test         - Run all tests"
	@echo "make test-unit    - Run unit tests only"
	@echo "make test-api     - Run API tests only"
	@echo "make test-bdd     - Run BDD UI tests only"
	@echo "make test-parallel- Run tests in parallel"
	@echo "make coverage     - Generate coverage report"
	@echo "make report       - Generate and open Allure report"
	@echo "make clean        - Clean test artifacts"
	@echo "make lint         - Lint codebase"

install:
	pip install -r requirements.txt
	playwright install

setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && playwright install

check-venv:
	@test -x venv/bin/pytest || (echo "Virtualenv not found. Run 'make setup' first." && exit 1)

run:
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

test: check-venv
	mkdir -p reports
	. venv/bin/activate && pytest tests/ -v --browser firefox --cov=src --cov-report=html --cov-report=term-missing --alluredir=allure-results --cucumberjson=reports/cucumber.json --html=reports/pytest-bdd.html --self-contained-html

test-unit: check-venv
	. venv/bin/activate && pytest tests/unit/ -v -m unit --cov=src --cov-report=html --alluredir=allure-results

test-api: check-venv
	. venv/bin/activate && pytest tests/api/ -v -m api --alluredir=allure-results

test-bdd: check-venv
	mkdir -p reports
	. venv/bin/activate && pytest tests/bdd/ -v -n 5 --browser firefox --headed --alluredir=allure-results --cucumberjson=reports/cucumber-bdd.json --html=reports/pytest-bdd-ui.html --self-contained-html

test-parallel: check-venv
	mkdir -p reports
	. venv/bin/activate && pytest tests/bdd/test_anagram_ui.py -v -n 5 --browser firefox --alluredir=allure-results --cucumberjson=reports/cucumber-bdd-parallel.json --html=reports/pytest-bdd-parallel.html --self-contained-html

coverage:
	pytest tests/unit/ --cov=src --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

report:
	allure generate allure-results --clean -o allure-report
	allure open allure-report

clean:
	rm -rf allure-results allure-report htmlcov .pytest_cache .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	. venv/bin/activate && ruff check .
