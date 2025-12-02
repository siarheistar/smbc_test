# Quick Setup Guide

## Prerequisites
- Python 3.9 or higher
- pip
- Git

## Installation Steps

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
```bash
playwright install
```

## Running the Application

### Option 1: Using the startup script
```bash
chmod +x start_app.sh
./start_app.sh
```

### Option 2: Manual start
```bash
source venv/bin/activate
uvicorn src.app:app --reload
```

Visit http://localhost:8000 in your browser.

## Running Tests

### All Tests
```bash
chmod +x run_tests.sh
./run_tests.sh
```

### Unit Tests Only
```bash
pytest tests/unit/ -v -m unit --cov=src
```

### API Tests Only
```bash
pytest tests/api/ -v -m api
```

### BDD UI Tests Only
```bash
pytest tests/bdd/ -v -m bdd --headed
```

### Parallel Test Execution
```bash
pytest tests/bdd/test_anagram_ui.py -v -n 2
```

## Viewing Reports

### Coverage Report
```bash
open htmlcov/index.html
```

### Allure Report
```bash
# Install Allure first
brew install allure  # macOS

# Generate and open report
allure generate allure-results --clean -o allure-report
allure open allure-report
```

## Troubleshooting

### Port 8000 in use
```bash
uvicorn src.app:app --port 8001
```

### Playwright issues
```bash
playwright install --force
playwright install-deps
```

### Permission denied on scripts
```bash
chmod +x *.sh
```

## Project Structure
```
SMBC/
├── src/                    # Application source code
├── tests/                  # Test files
│   ├── unit/              # Unit tests
│   ├── api/               # API tests
│   └── bdd/               # BDD UI tests
├── features/              # Cucumber feature files
└── .github/workflows/     # CI/CD configuration
```

## Next Steps

1. Start the application: `./start_app.sh`
2. Open http://localhost:8000
3. Try checking some anagrams
4. Run the tests: `./run_tests.sh`
5. View the reports in `htmlcov/` and `allure-report/`

## API Usage Example

```bash
curl -X POST "http://localhost:8000/api/check" \
  -H "Content-Type: application/json" \
  -d '{"input1":"listen","input2":"silent"}'
```

Expected response:
```json
{
  "input1": "listen",
  "input2": "silent",
  "result": true
}
```
