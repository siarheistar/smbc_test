# Anagram Checker - Demo Guide

This guide walks you through a complete demonstration of the Anagram Checker application.

## Prerequisites

Ensure you have completed the setup:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Demo Walkthrough

### Part 1: Application Features

#### 1.1 Start the Application

```bash
./start_app.sh
```

Or using Make:
```bash
make run
```

#### 1.2 Test the Web UI

1. Open browser: http://localhost:8000
2. Try these examples:

   **Example 1 - Valid Anagram:**
   - Input 1: `listen`
   - Input 2: `silent`
   - Click "Check Anagram"
   - Result: ✅ TRUE (green background)

   **Example 2 - Not an Anagram:**
   - Input 1: `hello`
   - Input 2: `world`
   - Click "Check Anagram"
   - Result: ❌ FALSE (red background)

   **Example 3 - Case Insensitive with Spaces:**
   - Input 1: `A gentleman`
   - Input 2: `Elegant Man`
   - Click "Check Anagram"
   - Result: ✅ TRUE

   **Example 4 - Long Phrase:**
   - Input 1: `eleven plus two`
   - Input 2: `twelve plus one`
   - Click "Check Anagram"
   - Result: ✅ TRUE

#### 1.3 Test the API

Open a new terminal and try these API calls:

**Example 1 - Using curl:**
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

**Example 2 - Non-anagram:**
```bash
curl -X POST "http://localhost:8000/api/check" \
  -H "Content-Type: application/json" \
  -d '{"input1":"rat","input2":"car"}'
```

Expected response:
```json
{
  "input1": "rat",
  "input2": "car",
  "result": false
}
```

#### 1.4 Interactive API Documentation

Visit http://localhost:8000/docs

1. Find the `POST /api/check` endpoint
2. Click "Try it out"
3. Enter test data:
   ```json
   {
     "input1": "school master",
     "input2": "the classroom"
   }
   ```
4. Click "Execute"
5. See the response

### Part 2: Code Quality (SOLID Principles)

#### 2.1 View the Core Logic

Open [src/anagram_checker.py](src/anagram_checker.py) and observe:

**Single Responsibility Principle:**
- `CaseInsensitiveNormalizer` - Only normalizes strings
- `SortedAnagramValidator` - Only validates anagrams
- `AnagramChecker` - Only orchestrates

**Open/Closed Principle:**
- `AnagramValidator` abstract class allows new validators
- Can add `FrequencyAnagramValidator` without changing existing code

**Dependency Inversion:**
- `AnagramChecker` depends on `AnagramValidator` abstraction
- Dependencies injected via constructor

#### 2.2 Code Structure

```
src/
├── anagram_checker.py  # Core business logic (SOLID)
├── models.py           # Data models (Pydantic)
└── app.py             # FastAPI application
```

### Part 3: Testing

#### 3.1 Unit Tests

Run unit tests with coverage:
```bash
make test-unit
```

Or:
```bash
pytest tests/unit/ -v -m unit --cov=src --cov-report=html
```

Expected output:
```
tests/unit/test_anagram_checker.py::TestCaseInsensitiveNormalizer::test_normalize_lowercase PASSED
tests/unit/test_anagram_checker.py::TestCaseInsensitiveNormalizer::test_normalize_removes_spaces PASSED
...
Coverage: >90%
```

View coverage:
```bash
open htmlcov/index.html
```

#### 3.2 API Tests

Run API tests:
```bash
make test-api
```

Or:
```bash
pytest tests/api/ -v -m api
```

Tests verify:
- ✅ Health check endpoint
- ✅ Root endpoint returns HTML
- ✅ API endpoint with valid anagrams
- ✅ API endpoint with non-anagrams
- ✅ Input validation
- ✅ Error handling

#### 3.3 BDD UI Tests

Run BDD tests with UI:
```bash
make test-bdd
```

Or:
```bash
pytest tests/bdd/ -v -m bdd --headed
```

Watch the browser automation:
1. Browser opens automatically
2. Navigates to http://localhost:8000
3. Fills in input fields
4. Clicks button
5. Verifies result
6. Takes screenshots
7. Closes browser

#### 3.4 Parallel Execution

Run tests in parallel:
```bash
make test-parallel
```

Or:
```bash
pytest tests/bdd/test_anagram_ui.py -v -n 2
```

Features:
- Part 1 and Part 2 run simultaneously
- 2 browser instances
- Faster execution
- Results merged

### Part 4: Reports

#### 4.1 Coverage Report

After running unit tests:
```bash
open htmlcov/index.html
```

Report shows:
- Overall coverage percentage
- Per-file coverage
- Line-by-line coverage
- Uncovered code highlighted in red

#### 4.2 Allure Report

Generate Allure report:
```bash
make report
```

Or:
```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Report includes:
- **Overview**: Total tests, pass rate, duration
- **Suites**: Tests organized by file
- **Behaviors**: BDD-style organization
- **Timeline**: Parallel execution visualization
- **Graphs**: Pie charts, trends
- **Screenshots**: UI test evidence

Navigate through:
1. Click "Suites" → "test_anagram_ui.py"
2. See all scenarios with parameters
3. Click on a test
4. See step-by-step execution
5. View screenshots
6. Check execution time

### Part 5: Demonstrating Test Failures

#### 5.1 Modify a Scenario to Fail

Edit [features/Anagram_Checker.feature](features/Anagram_Checker.feature):

Change:
```gherkin
| listen | silent | true |
```

To:
```gherkin
| listen | silent | false |
```

#### 5.2 Run Tests

```bash
pytest tests/bdd/ -v
```

#### 5.3 Observe Failure

Expected output:
```
FAILED tests/bdd/test_anagram_ui.py::test_check_if_two_strings_are_anagrams[listen-silent-false]
AssertionError: Expected FALSE but got: TRUE - These are anagrams!
```

#### 5.4 View Failure in Report

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Report shows:
- Failed test highlighted in red
- Error message
- Screenshot of failure state
- Expected vs actual values
- Stack trace

#### 5.5 Revert Changes

Change back to:
```gherkin
| listen | silent | true |
```

### Part 6: CI/CD

#### 6.1 GitHub Actions Workflow

View [.github/workflows/ci.yml](.github/workflows/ci.yml)

The workflow:
1. Runs on push/PR
2. Tests on Python 3.9, 3.10, 3.11
3. Executes all test suites
4. Generates coverage reports
5. Creates Allure reports
6. Publishes to GitHub Pages

#### 6.2 Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Anagram Checker with complete test suite"
git remote add origin <your-repo-url>
git push -u origin main
```

#### 6.3 Enable GitHub Pages

1. Go to repository Settings
2. Click "Pages"
3. Select "gh-pages" branch
4. Save

After the first workflow run, reports will be available at:
`https://<username>.github.io/<repository-name>/`

### Part 7: Feature Highlights

#### 7.1 OOP and SOLID

The code demonstrates:
- ✅ Single Responsibility Principle
- ✅ Open/Closed Principle
- ✅ Liskov Substitution Principle
- ✅ Interface Segregation Principle
- ✅ Dependency Inversion Principle

See [src/anagram_checker.py](src/anagram_checker.py) for implementation.

#### 7.2 Test Coverage

- **Unit Tests**: Core logic validation
- **API Tests**: Backend endpoint testing
- **BDD Tests**: User acceptance testing
- **Integration**: End-to-end scenarios

#### 7.3 Tools and Technologies

- ✅ FastAPI - Modern web framework
- ✅ Pytest - Testing framework
- ✅ pytest-bdd - BDD support
- ✅ Playwright - Browser automation
- ✅ Allure - Beautiful reports
- ✅ pytest-cov - Coverage analysis
- ✅ GitHub Actions - CI/CD

### Part 8: All Test Scenarios

| # | Input 1           | Input 2          | Expected | Status |
|---|-------------------|------------------|----------|--------|
| 1 | listen            | silent           | TRUE     | ✅     |
| 2 | hello             | world            | FALSE    | ✅     |
| 3 | conversation      | voices rant on   | TRUE     | ✅     |
| 4 | school master     | the classroom    | TRUE     | ✅     |
| 5 | a gentleman       | elegant man      | TRUE     | ✅     |
| 6 | eleven plus two   | twelve plus one  | TRUE     | ✅     |
| 7 | apple             | paple            | TRUE     | ✅     |
| 8 | rat               | car              | FALSE    | ✅     |

## Quick Demo Commands

```bash
# Complete demo in one go:

# 1. Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install

# 2. Start app (in background)
uvicorn src.app:app --host 0.0.0.0 --port 8000 &

# 3. Test with curl
curl -X POST "http://localhost:8000/api/check" \
  -H "Content-Type: application/json" \
  -d '{"input1":"listen","input2":"silent"}'

# 4. Run all tests
make test

# 5. View reports
open htmlcov/index.html
allure generate allure-results --clean -o allure-report
allure open allure-report
```

## Troubleshooting

### Issue: Port 8000 already in use
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn src.app:app --port 8001
```

### Issue: Playwright browsers not installed
```bash
playwright install --force
playwright install-deps
```

### Issue: Permission denied
```bash
chmod +x *.sh
```

## Success Criteria

After completing this demo, you should have:

✅ Running web application
✅ Working API endpoints
✅ All tests passing
✅ Coverage report >90%
✅ Allure report with screenshots
✅ Understanding of SOLID principles
✅ Parallel test execution demonstrated
✅ CI/CD pipeline configured

## Next Steps

1. Explore the code in [src/](src/)
2. Review tests in [tests/](tests/)
3. Examine feature files in [features/](features/)
4. Customize for your use case
5. Add more test scenarios
6. Deploy to production

## Contact

For questions or issues, refer to:
- [README.md](README.md) - Main documentation
- [SETUP.md](SETUP.md) - Setup guide
- [EVALUATION_CHECKLIST.md](EVALUATION_CHECKLIST.md) - Evaluation criteria
