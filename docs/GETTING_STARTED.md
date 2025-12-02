# Getting Started with Anagram Checker

Welcome! This guide will help you get the Anagram Checker application up and running in minutes.

## Prerequisites

You need:
- Python 3.9 or higher
- pip (Python package manager)
- Git
- 5 minutes of your time

## Step-by-Step Installation

### Step 1: Verify Setup

Run the verification script to check your environment:

```bash
chmod +x verify_setup.sh
./verify_setup.sh
```

This will check:
- Python installation
- pip availability
- Project structure
- Required files

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (server)
- Pytest (testing)
- Playwright (browser automation)
- Allure (reporting)
- And more...

### Step 5: Install Playwright Browsers

```bash
playwright install
```

This downloads the browsers needed for UI testing.

### Step 6: Verify Installation

```bash
./verify_setup.sh
```

All checks should pass with green ✓ marks.

## Running the Application

### Option 1: Using the Startup Script

```bash
./start_app.sh
```

### Option 2: Using Make

```bash
make run
```

### Option 3: Manual Start

```bash
uvicorn src.app:app --reload
```

The application will start at: **http://localhost:8000**

## Testing the Application

### Test the Web UI

1. Open your browser
2. Go to http://localhost:8000
3. Enter two strings:
   - Input 1: `listen`
   - Input 2: `silent`
4. Click "Check Anagram"
5. See result: **TRUE**

### Test the API

In a new terminal:

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

### View API Documentation

Visit: http://localhost:8000/docs

Interactive documentation where you can test all endpoints.

## Running Tests

### Quick Test - All Tests

```bash
make test
```

Or:

```bash
./run_tests.sh
```

### Run Specific Test Types

**Unit tests only:**
```bash
make test-unit
```

**API tests only:**
```bash
make test-api
```

**BDD UI tests only:**
```bash
make test-bdd
```

**Parallel execution:**
```bash
make test-parallel
```

## Viewing Reports

### Coverage Report

After running tests:

```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html
```

### Allure Report

First, install Allure:

**macOS:**
```bash
brew install allure
```

**Windows:**
Download from: https://docs.qameta.io/allure/#_installing_a_commandline

**Linux:**
```bash
# Follow instructions at:
# https://docs.qameta.io/allure/#_linux
```

Then generate and view:

```bash
make report
```

Or:

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

## Project Structure Overview

```
SMBC/
├── src/              # Application code
├── tests/            # Test files
├── features/         # BDD feature files
├── README.md         # Full documentation
├── SETUP.md          # Setup guide
├── DEMO.md           # Demo walkthrough
└── Makefile          # Convenient commands
```

## Quick Reference

### Make Commands

```bash
make help          # Show all commands
make install       # Install dependencies
make run           # Start application
make test          # Run all tests
make test-unit     # Unit tests
make test-api      # API tests
make test-bdd      # BDD tests
make test-parallel # Parallel tests
make coverage      # Coverage report
make report        # Allure report
make clean         # Clean artifacts
```

### Scripts

```bash
./start_app.sh          # Start application
./run_tests.sh          # All tests
./run_unit_tests.sh     # Unit tests
./run_api_tests.sh      # API tests
./run_bdd_tests.sh      # BDD tests
./run_parallel_tests.sh # Parallel tests
./verify_setup.sh       # Verify setup
```

## Common Issues and Solutions

### Port 8000 Already in Use

```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn src.app:app --port 8001
```

### Playwright Browsers Not Found

```bash
playwright install --force
playwright install-deps
```

### Permission Denied on Scripts

```bash
chmod +x *.sh
```

### Virtual Environment Issues

```bash
# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## What's Next?

### 1. Explore the Code

- [src/anagram_checker.py](src/anagram_checker.py) - Core logic with SOLID principles
- [src/app.py](src/app.py) - FastAPI application
- [tests/](tests/) - All test files

### 2. Read the Documentation

- [README.md](README.md) - Comprehensive documentation
- [DEMO.md](DEMO.md) - Complete demo walkthrough
- [EVALUATION_CHECKLIST.md](EVALUATION_CHECKLIST.md) - Criteria verification

### 3. Try the Examples

All test scenarios:
- `listen` and `silent` → TRUE
- `hello` and `world` → FALSE
- `conversation` and `voices rant on` → TRUE
- `school master` and `the classroom` → TRUE
- `a gentleman` and `elegant man` → TRUE
- `eleven plus two` and `twelve plus one` → TRUE
- `apple` and `paple` → TRUE
- `rat` and `car` → FALSE

### 4. Modify and Experiment

Try:
- Adding new test scenarios
- Implementing a different validation algorithm
- Customizing the UI
- Adding new API endpoints

### 5. Deploy

Set up CI/CD:
1. Push to GitHub
2. Enable GitHub Actions
3. Configure GitHub Pages
4. Reports auto-deploy

## Learning Path

If you're using this for learning, explore in this order:

1. **Basic Usage**
   - Run the app
   - Test web UI
   - Test API

2. **Code Structure**
   - Read [src/anagram_checker.py](src/anagram_checker.py)
   - Understand SOLID principles
   - See OOP design

3. **Testing**
   - Run unit tests
   - Run API tests
   - Run BDD tests
   - View coverage

4. **BDD Features**
   - Read feature files
   - Understand scenarios
   - Run with Playwright

5. **Reports**
   - Generate coverage
   - Create Allure report
   - Analyze results

6. **CI/CD**
   - Understand workflow
   - Set up GitHub Actions
   - Deploy to Pages

## Getting Help

### Documentation

- **Main docs**: [README.md](README.md)
- **Setup**: [SETUP.md](SETUP.md)
- **Demo**: [DEMO.md](DEMO.md)
- **Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### Commands

```bash
make help  # All make commands
```

### Troubleshooting

See README.md → Troubleshooting section

## Success Checklist

After setup, you should have:

- ✅ Virtual environment created
- ✅ Dependencies installed
- ✅ Playwright browsers installed
- ✅ Application running at http://localhost:8000
- ✅ Web UI working
- ✅ API responding
- ✅ All tests passing
- ✅ Coverage report generated
- ✅ Allure report available

## Next Steps

Choose your path:

**For Users:**
- Use the web UI
- Integrate the API
- Read API docs

**For Developers:**
- Read the code
- Run tests
- Modify features
- Add new validators

**For Learners:**
- Study SOLID principles
- Understand BDD
- Learn testing patterns
- Explore CI/CD

**For Evaluators:**
- Check [EVALUATION_CHECKLIST.md](EVALUATION_CHECKLIST.md)
- Run all tests
- View reports
- Verify criteria

## Welcome Aboard! 🚀

You're all set! The Anagram Checker is ready to use.

Key URLs:
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Happy coding!
