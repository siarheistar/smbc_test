# Quick Command Reference

All available commands for the Anagram Checker project.

## Make Commands

```bash
make help          # Show all available commands
make install       # Install Python dependencies
make setup         # Complete setup (venv + deps + browsers)
make run           # Start the FastAPI application
make test          # Run all tests
make test-unit     # Run unit tests only
make test-api      # Run API tests only
make test-bdd      # Run BDD UI tests only
make test-parallel # Run tests in parallel
make coverage      # Generate coverage report
make report        # Generate and open Allure report
make clean         # Clean test artifacts
```

## Shell Scripts

### Application
```bash
./start_app.sh              # Start the FastAPI server
```

### Testing
```bash
./run_tests.sh              # Run all tests (unit, API, BDD)
./run_unit_tests.sh         # Run unit tests with coverage
./run_api_tests.sh          # Run API tests
./run_bdd_tests.sh          # Run BDD UI tests with Playwright
./run_parallel_tests.sh     # Run BDD tests in parallel
```

### Utilities
```bash
./verify_setup.sh           # Verify project setup and dependencies
```

## Direct pytest Commands

### All Tests
```bash
pytest tests/ -v --cov=src --cov-report=html --alluredir=allure-results
```

### Unit Tests
```bash
pytest tests/unit/ -v -m unit --cov=src --cov-report=html
```

### API Tests
```bash
pytest tests/api/ -v -m api
```

### BDD Tests
```bash
pytest tests/bdd/ -v -m bdd --headed
```

### Parallel Tests
```bash
pytest tests/bdd/test_anagram_ui.py -v -n 2
```

### Specific Test File
```bash
pytest tests/unit/test_anagram_checker.py -v
```

### Specific Test Class
```bash
pytest tests/unit/test_anagram_checker.py::TestAnagramChecker -v
```

### Specific Test Method
```bash
pytest tests/unit/test_anagram_checker.py::TestAnagramChecker::test_check_valid_anagrams -v
```

## Application Commands

### Start Server
```bash
# Development mode with auto-reload
uvicorn src.app:app --reload

# Specific host and port
uvicorn src.app:app --host 0.0.0.0 --port 8000

# Production mode
uvicorn src.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Background Server
```bash
# Start in background
uvicorn src.app:app --host 0.0.0.0 --port 8000 &

# Find and kill
lsof -ti:8000 | xargs kill -9
```

## Python Virtual Environment

### Create
```bash
python3 -m venv venv
```

### Activate
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Deactivate
```bash
deactivate
```

## Dependency Management

### Install All
```bash
pip install -r requirements.txt
```

### Update Requirements
```bash
pip freeze > requirements.txt
```

### Install Specific
```bash
pip install fastapi
pip install pytest
```

## Playwright Commands

### Install Browsers
```bash
playwright install
```

### Install Specific Browser
```bash
playwright install chromium
```

### Install System Dependencies
```bash
playwright install-deps
```

### Reinstall
```bash
playwright install --force
```

## Coverage Commands

### Generate HTML Report
```bash
pytest tests/unit/ --cov=src --cov-report=html
```

### Generate Terminal Report
```bash
pytest tests/unit/ --cov=src --cov-report=term
```

### Generate XML Report
```bash
pytest tests/unit/ --cov=src --cov-report=xml
```

### View HTML Report
```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html
```

## Allure Commands

### Generate Report
```bash
allure generate allure-results --clean -o allure-report
```

### Open Report
```bash
allure open allure-report
```

### Serve Report
```bash
allure serve allure-results
```

### Generate and Open
```bash
allure generate allure-results --clean -o allure-report && allure open allure-report
```

## API Testing with cURL

### Check Anagram
```bash
curl -X POST "http://localhost:8000/api/check" \
  -H "Content-Type: application/json" \
  -d '{"input1":"listen","input2":"silent"}'
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Get OpenAPI JSON
```bash
curl http://localhost:8000/openapi.json
```

### Pretty Print JSON
```bash
curl -X POST "http://localhost:8000/api/check" \
  -H "Content-Type: application/json" \
  -d '{"input1":"listen","input2":"silent"}' | python -m json.tool
```

## Git Commands

### Initialize
```bash
git init
```

### Add All Files
```bash
git add .
```

### Commit
```bash
git commit -m "Initial commit: Anagram Checker"
```

### Push to GitHub
```bash
git remote add origin <your-repo-url>
git push -u origin main
```

## File Operations

### List All Python Files
```bash
find . -name "*.py" -type f | grep -v venv
```

### Count Lines of Code
```bash
find src -name "*.py" -type f -exec wc -l {} + | tail -1
```

### Find TODO Comments
```bash
grep -r "TODO" src/
```

### Clean Python Cache
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

## Clean Up Commands

### Remove Test Artifacts
```bash
rm -rf allure-results allure-report htmlcov .pytest_cache .coverage
```

### Remove Python Cache
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
```

### Complete Clean
```bash
make clean
```

## Development Commands

### Format Code (if black installed)
```bash
black src/ tests/
```

### Lint Code (if flake8 installed)
```bash
flake8 src/ tests/
```

### Type Check (if mypy installed)
```bash
mypy src/
```

## Docker Commands (if Dockerfile exists)

### Build
```bash
docker build -t anagram-checker .
```

### Run
```bash
docker run -p 8000:8000 anagram-checker
```

### Run Tests in Docker
```bash
docker run anagram-checker pytest
```

## Useful One-Liners

### Complete Setup
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && playwright install
```

### Quick Test
```bash
source venv/bin/activate && pytest tests/ -v
```

### Quick Start
```bash
source venv/bin/activate && uvicorn src.app:app --reload
```

### Full Test with Reports
```bash
pytest tests/ -v --cov=src --cov-report=html --alluredir=allure-results && allure generate allure-results --clean -o allure-report
```

### Parallel Test with Coverage
```bash
pytest tests/ -v -n auto --cov=src --cov-report=html
```

## Environment Variables

### Set Python Path
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Set Custom Port
```bash
export PORT=8001
uvicorn src.app:app --port $PORT
```

## Shortcuts

### Development Workflow
```bash
# Terminal 1: Start server
make run

# Terminal 2: Run tests
make test

# Terminal 3: View coverage
make coverage
```

### Quick Demo
```bash
# 1. Setup
make setup

# 2. Run app in background
make run &

# 3. Test
make test

# 4. View reports
make report
```

## Help Commands

### Pytest Help
```bash
pytest --help
```

### Playwright Help
```bash
playwright --help
```

### Allure Help
```bash
allure --help
```

### Make Help
```bash
make help
```

## Verification Commands

### Check Python Version
```bash
python3 --version
```

### Check pip Version
```bash
pip --version
```

### Check Installed Packages
```bash
pip list
```

### Check Specific Package
```bash
pip show pytest
```

### Verify Playwright
```bash
playwright --version
```

### Check Ports
```bash
lsof -i :8000
```

## Debugging Commands

### Run with Debug Output
```bash
pytest tests/ -v -s
```

### Run with pdb on Failure
```bash
pytest tests/ --pdb
```

### Run Last Failed
```bash
pytest --lf
```

### Run Failed First
```bash
pytest --ff
```

### Show Slowest Tests
```bash
pytest tests/ --durations=10
```

## Performance Commands

### Time Tests
```bash
time pytest tests/
```

### Profile Tests
```bash
pytest tests/ --profile
```

### Parallel Execution
```bash
pytest tests/ -n auto
```

## CI/CD Commands

### Simulate CI Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
pytest tests/ -v --cov=src
```

### Generate CI Reports
```bash
pytest tests/ --cov=src --cov-report=xml --alluredir=allure-results
```

## Documentation Commands

### View README
```bash
cat README.md
```

### Search Documentation
```bash
grep -r "SOLID" *.md
```

### List All Docs
```bash
ls -la *.md
```

## Quick Reference Summary

```bash
# Setup
make setup

# Run
make run

# Test
make test

# Reports
make coverage
make report

# Clean
make clean

# Help
make help
```

## Tips

1. Always activate virtual environment first
2. Use `make` commands for convenience
3. Run `./verify_setup.sh` to check setup
4. Use `make help` to see all options
5. Check logs if tests fail
6. Use `-v` for verbose output
7. Use `--headed` to see browser during BDD tests
8. Use `-n 2` for parallel execution with 2 workers

## Common Workflows

### First Time Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
./verify_setup.sh
```

### Daily Development
```bash
source venv/bin/activate
make run  # in one terminal
make test # in another terminal
```

### Before Commit
```bash
make test
make coverage
# Review reports
git add .
git commit -m "Your message"
```

### Generate Reports
```bash
make test
make coverage
make report
```

For more information, see:
- [README.md](README.md) - Complete documentation
- [GETTING_STARTED.md](GETTING_STARTED.md) - Quick start guide
- [INDEX.md](INDEX.md) - Documentation navigator
