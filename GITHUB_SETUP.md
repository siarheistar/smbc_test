# GitHub Repository Setup Guide

This guide will help you create the GitHub repository "smbc_test" and push your code.

## Prerequisites

- GitHub account
- Git configured locally
- GitHub CLI (`gh`) installed (optional but recommended)

## Option 1: Using GitHub CLI (Recommended)

```bash
# Login to GitHub (if not already logged in)
gh auth login

# Create the repository
gh repo create smbc_test --public --description "Anagram Checker with comprehensive BDD, API, and Unit testing"

# Add the remote
git remote add origin https://github.com/siarheistar/smbc_test.git

# Commit all changes (if not done already)
git add .
git commit -m "Initial commit: Anagram Checker with comprehensive testing

- FastAPI web application with REST API and web UI
- SOLID principles implementation with OOP design patterns
- Comprehensive test suite (57 tests, 95% coverage):
  * 19 unit tests (pytest)
  * 22 API tests (pytest + FastAPI TestClient)
  * 16 BDD UI tests (pytest-bdd + Playwright + Firefox)
- Cucumber feature files split for parallel execution
- Allure reporting integration
- pytest-xdist for parallel test execution
- Complete documentation and setup scripts
- Advanced CI/CD pipeline with Docker matrix
- Custom Allure reports with historical tracking
- GitHub Pages integration

# Push to GitHub
git branch -M main
git push -u origin main

# Enable GitHub Pages
gh api repos/YOUR_USERNAME/smbc_test/pages -X POST -f source[branch]=gh-pages -f source[path]=/
```

## Option 2: Using GitHub Web Interface

1. **Create Repository on GitHub:**

   - Go to https://github.com/new
   - Repository name: `smbc_test`
   - Description: `Anagram Checker with comprehensive BDD, API, and Unit testing`
   - Choose: Public
   - Do NOT initialize with README, .gitignore, or license
   - Click "Create repository"
2. **Push Your Code:**

```bash
# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/smbc_test.git

# Commit all changes (if not done already)
git add .
git commit -m "Initial commit: Anagram Checker with comprehensive testing

- FastAPI web application with REST API and web UI
- SOLID principles implementation with OOP design patterns
- Comprehensive test suite (57 tests, 95% coverage):
  * 19 unit tests (pytest)
  * 22 API tests (pytest + FastAPI TestClient)
  * 16 BDD UI tests (pytest-bdd + Playwright + Firefox)
- Cucumber feature files split for parallel execution
- Allure reporting integration
- pytest-xdist for parallel test execution
- Complete documentation and setup scripts
- Advanced CI/CD pipeline with Docker matrix
- Custom Allure reports with historical tracking
- GitHub Pages integration

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

3. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Click "Settings" → "Pages"
   - Under "Source", select branch: `gh-pages`
   - Click "Save"

## Verify Setup

After pushing and the first workflow run completes:

1. **Check GitHub Actions:**

   - Go to the "Actions" tab in your repository
   - You should see the "Advanced CI/CD Pipeline with Docker Matrix" workflow running
2. **Access Reports:**

   - Once the workflow completes, GitHub Pages will be available at:
     - Main index: `https://YOUR_USERNAME.github.io/smbc_test/`
     - Latest Allure report: `https://YOUR_USERNAME.github.io/smbc_test/latest/index.html`
     - Coverage report: `https://YOUR_USERNAME.github.io/smbc_test/htmlcov/index.html`

## What the CI/CD Pipeline Does

The advanced pipeline includes:

### 1. **Parallel Test Execution**

- **Unit Tests**: Run in Python 3.11 container
- **API Tests**: Run in Python 3.11 container
- **BDD Tests**: Run in Docker matrix with 3 browsers (Firefox, Chromium, WebKit)

### 2. **Separate Allure Results**

- `allure-results-unit` - Unit test results
- `allure-results-api` - API test results
- `allure-results-bdd-firefox` - BDD tests with Firefox
- `allure-results-bdd-chromium` - BDD tests with Chromium
- `allure-results-bdd-webkit` - BDD tests with WebKit

### 3. **Aggregation & Reporting**

- Merges all test results into single Allure report
- Calculates comprehensive statistics
- Generates custom index page with historical tracking
- Deploys to GitHub Pages

### 4. **Custom Features**

- **Run ID**: Each run has unique identifier (e.g., `123-1234567890`)
- **Custom Index Page**: Beautiful dashboard showing:
  - Total tests executed
  - Pass rate
  - Coverage percentage
  - Links to Allure and coverage reports
  - Historical run tracking (last 20 runs)
- **Enhanced Allure Report**:
  - Custom header with Run ID
  - Links to coverage report
  - Links back to index page
- **Coverage Report**: Integrated into GitHub Pages

### 5. **GitHub Pages Structure**

```
https://YOUR_USERNAME.github.io/smbc_test/
├── index.html                    (Custom index with historical runs)
├── latest/
│   └── index.html               (Latest Allure report)
├── htmlcov/
│   └── index.html               (Coverage report)
└── [run-number]/
    └── index.html               (Historical Allure reports)
```

## Triggering the Pipeline

The pipeline runs automatically on:

- Push to `main`, `master`, or `develop` branches
- Pull requests to `main` or `master` branches

For pull requests, the pipeline will also post a comment with test results and links to reports.

## Troubleshooting

### Pipeline Not Running

- Check the `.github/workflows/ci.yml` file exists
- Verify GitHub Actions is enabled in repository settings
- Check for syntax errors in the workflow file

### GitHub Pages Not Working

- Ensure `gh-pages` branch exists (created after first successful run)
- Verify GitHub Pages is enabled in Settings → Pages
- Wait a few minutes for deployment to complete

### Tests Failing

- Check the "Actions" tab for detailed logs
- Unit and API tests should pass in containers
- BDD tests may have browser-specific issues

## Next Steps

After successful setup:

1. View the custom index page to see all reports
2. Explore the Allure report with detailed test results
3. Check coverage report to see code coverage
4. Monitor historical runs to track progress over time

## Customization

You can customize:

- **Index page styling**: Edit the HTML/CSS in the workflow's "Create custom index page" step
- **Allure customizations**: Modify the "Customize Allure Report" step
- **Browser matrix**: Add/remove browsers in the `bdd-tests` job matrix
- **Report retention**: Change `keep_reports: 20` to keep more/fewer historical reports

## Support

If you encounter issues:

1. Check GitHub Actions logs
2. Review the workflow file: [.github/workflows/ci.yml](.github/workflows/ci.yml)
3. Ensure all dependencies are in [requirements.txt](requirements.txt)
4. Verify Playwright browsers are compatible with your setup
