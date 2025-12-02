# CI/CD Pipeline Architecture

## Overview

The Advanced CI/CD Pipeline implements a sophisticated testing and reporting infrastructure using Docker containers, parallel execution, and automated deployment to GitHub Pages.

## Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GitHub Push/PR Trigger                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PARALLEL EXECUTION PHASE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────────┐   │
│  │  Unit Tests      │  │  API Tests       │  │  BDD Tests (Matrix)    │   │
│  │                  │  │                  │  │                        │   │
│  │  Container:      │  │  Container:      │  │  Container:            │   │
│  │  python:3.11     │  │  python:3.11     │  │  playwright:v1.40.0    │   │
│  │                  │  │                  │  │                        │   │
│  │  Output:         │  │  Output:         │  │  Matrix Strategy:      │   │
│  │  • allure-       │  │  • allure-       │  │  ┌──────────────────┐ │   │
│  │    results-unit  │  │    results-api   │  │  │ Firefox          │ │   │
│  │  • htmlcov       │  │                  │  │  │ Chromium         │ │   │
│  │  • coverage.xml  │  │                  │  │  │ WebKit           │ │   │
│  │                  │  │                  │  │  └──────────────────┘ │   │
│  │  Tests: 19       │  │  Tests: 22       │  │                        │   │
│  │  Coverage: 97%   │  │  Tests: API      │  │  Output per browser:   │   │
│  └──────────────────┘  └──────────────────┘  │  • allure-results-     │   │
│           │                     │             │    bdd-{browser}       │   │
│           │                     │             │                        │   │
│           │                     │             │  Tests: 16 × 3 = 48    │   │
│           │                     │             └────────────────────────┘   │
│           │                     │                        │                 │
└───────────┼─────────────────────┼────────────────────────┼─────────────────┘
            │                     │                        │
            └─────────────────────┴────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AGGREGATION & REPORTING PHASE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Step 1: Download All Artifacts                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  artifacts/                                                         │    │
│  │  ├── allure-results-unit/                                           │    │
│  │  ├── allure-results-api/                                            │    │
│  │  ├── allure-results-bdd-firefox/                                    │    │
│  │  ├── allure-results-bdd-chromium/                                   │    │
│  │  ├── allure-results-bdd-webkit/                                     │    │
│  │  └── coverage-report/                                               │    │
│  │      ├── htmlcov/                                                   │    │
│  │      └── coverage.xml                                               │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                  │                                           │
│                                  ▼                                           │
│  Step 2: Merge Allure Results                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  cp artifacts/allure-results-*/* → allure-results/                 │    │
│  │                                                                     │    │
│  │  Result: Single directory with all test results                    │    │
│  │  (~85 test result JSON files)                                      │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                  │                                           │
│                                  ▼                                           │
│  Step 3: Calculate Statistics                                               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  • Total Tests: Count all *-result.json files                      │    │
│  │  • Coverage: Extract from coverage.xml                             │    │
│  │  • Pass Rate: Count passed/failed tests                            │    │
│  │  • Passed/Failed: Parse JSON status fields                         │    │
│  │                                                                     │    │
│  │  Output Variables:                                                 │    │
│  │  - total_tests: 57 (19 unit + 22 API + 16 BDD)                    │    │
│  │  - coverage: 95.0%                                                 │    │
│  │  - passed: 57                                                      │    │
│  │  - failed: 0                                                       │    │
│  │  - pass_rate: 100.0%                                               │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                  │                                           │
│                                  ▼                                           │
│  Step 4: Generate Allure Report                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  Input: allure-results/                                            │    │
│  │  Output: allure-report/                                            │    │
│  │  History: allure-history/ (from gh-pages branch)                   │    │
│  │                                                                     │    │
│  │  Features:                                                         │    │
│  │  • Trend graphs across runs                                        │    │
│  │  • Detailed test results                                           │    │
│  │  • Duration statistics                                             │    │
│  │  • Attachments (screenshots, logs)                                 │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                  │                                           │
│                                  ▼                                           │
│  Step 5: Create Custom Index Page                                           │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  allure-history/index.html                                         │    │
│  │                                                                     │    │
│  │  Features:                                                         │    │
│  │  • Beautiful gradient UI design                                    │    │
│  │  • Current run statistics cards                                    │    │
│  │  • Historical run tracking (last 20)                               │    │
│  │  • Links to Allure & coverage reports                              │    │
│  │  • localStorage for client-side history                            │    │
│  │  • Run ID, pass rate, coverage display                             │    │
│  │  • Color-coded pass rates (green/yellow/red)                       │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                  │                                           │
│                                  ▼                                           │
│  Step 6: Customize Allure Report                                            │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  Add custom elements:                                              │    │
│  │  • Custom header with Run ID                                       │    │
│  │  • Links to coverage report                                        │    │
│  │  • Link back to index page                                         │    │
│  │  • Custom widgets with metadata                                    │    │
│  │                                                                     │    │
│  │  Inject into allure-report/index.html                              │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                  │                                           │
│                                  ▼                                           │
│  Step 7: Prepare Deployment Structure                                       │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  allure-history/                                                   │    │
│  │  ├── index.html              (Custom index page)                   │    │
│  │  ├── latest/                 (Latest Allure report)                │    │
│  │  │   └── index.html                                                │    │
│  │  ├── htmlcov/                (Coverage report)                     │    │
│  │  │   └── index.html                                                │    │
│  │  └── [previous-runs]/        (Historical reports)                  │    │
│  │      └── index.html                                                │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                  │                                           │
│                                  ▼                                           │
│  Step 8: Deploy to GitHub Pages                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  Branch: gh-pages                                                  │    │
│  │  Directory: allure-history/                                        │    │
│  │  Keep files: true (preserve history)                               │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GITHUB PAGES (PUBLIC)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  URL: https://YOUR_USERNAME.github.io/smbc_test/                            │
│                                                                              │
│  Available Pages:                                                            │
│  1. Main Index:    /index.html                                              │
│  2. Latest Report: /latest/index.html                                       │
│  3. Coverage:      /htmlcov/index.html                                      │
│  4. Historical:    /[run-number]/index.html                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Docker Containers Used

### 1. Unit Tests Container
```dockerfile
FROM python:3.11-slim
```
- **Purpose**: Isolated Python environment for unit tests
- **Dependencies**: pip packages from requirements.txt
- **Output**: Unit test results + coverage data

### 2. API Tests Container
```dockerfile
FROM python:3.11-slim
```
- **Purpose**: Isolated Python environment for API tests
- **Dependencies**: pip packages from requirements.txt
- **Output**: API test results

### 3. BDD Tests Container
```dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-jammy
```
- **Purpose**: Pre-configured with Playwright browsers
- **Browsers**: Firefox, Chromium, WebKit
- **Matrix**: 3 parallel jobs (one per browser)
- **Output**: BDD test results per browser

## Test Execution Metrics

| Test Type | Container | Tests | Coverage | Parallel | Duration |
|-----------|-----------|-------|----------|----------|----------|
| Unit      | Python 3.11 | 19 | 97% | No | ~30s |
| API       | Python 3.11 | 22 | 90% | No | ~45s |
| BDD (Firefox) | Playwright | 16 | N/A | Yes | ~2m |
| BDD (Chromium) | Playwright | 16 | N/A | Yes | ~2m |
| BDD (WebKit) | Playwright | 16 | N/A | Yes | ~2m |
| **Total** | - | **89** | **95%** | - | **~3m** |

*Note: BDD tests run in parallel across browsers, so total duration is ~3 minutes, not 6 minutes*

## Allure Results Aggregation

### Input Files Structure
```
artifacts/
├── allure-results-unit/
│   ├── [uuid]-result.json (×19)
│   ├── [uuid]-container.json
│   └── environment.properties
├── allure-results-api/
│   ├── [uuid]-result.json (×22)
│   ├── [uuid]-container.json
│   └── environment.properties
├── allure-results-bdd-firefox/
│   ├── [uuid]-result.json (×16)
│   └── ...
├── allure-results-bdd-chromium/
│   ├── [uuid]-result.json (×16)
│   └── ...
└── allure-results-bdd-webkit/
    ├── [uuid]-result.json (×16)
    └── ...
```

### Merged Structure
```
allure-results/
├── [uuid]-result.json (×89 total)
├── [uuid]-container.json
├── environment.properties
└── ... (all merged)
```

## Custom Index Page Features

### Statistics Cards
- **Total Tests**: Aggregated count from all test types
- **Pass Rate**: Percentage of passing tests
- **Coverage**: From coverage.xml
- **Latest Run**: Run number for easy identification

### Historical Tracking
- Stores last 20 runs in browser localStorage
- Each run includes:
  - Run ID (GitHub run number + run ID)
  - Total tests executed
  - Coverage percentage
  - Pass rate
  - Passed/Failed counts
  - Timestamp
  - Links to reports

### Color Coding
- **Green (≥90%)**: Excellent pass rate
- **Yellow (70-89%)**: Warning, needs attention
- **Red (<70%)**: Critical, action required

## Allure Report Customizations

### Custom Header
```html
<div style="background: gradient; color: white;">
  <h2>Run ID: {RUN_ID}</h2>
  <a href="../index.html">← Back to Index</a> |
  <a href="../htmlcov/index.html">View Coverage</a>
</div>
```

### Custom Widgets
1. **custom-links.json**: Links to coverage and index
2. **summary-custom.json**: Run metadata (ID, tests, coverage, pass rate)

## GitHub Pages Structure

```
gh-pages branch
├── index.html                    (Custom dashboard)
├── latest/                       (Symlink/copy of most recent report)
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── data/
├── htmlcov/                      (Coverage report)
│   ├── index.html
│   ├── *.html (source files)
│   └── *.css
├── 123/                          (Run #123)
│   └── [allure report]
├── 124/                          (Run #124)
│   └── [allure report]
└── ... (up to 20 historical runs)
```

## Run ID Format

```
{GitHub Run Number}-{GitHub Run ID}

Example: 123-1234567890
         │   │
         │   └── Unique GitHub run ID (internal)
         └────── Sequential run number (visible)
```

## Workflow Triggers

### Push Events
```yaml
on:
  push:
    branches: [main, master, develop]
```
- Triggers full test suite
- Generates reports
- Deploys to GitHub Pages

### Pull Request Events
```yaml
on:
  pull_request:
    branches: [main, master]
```
- Runs full test suite
- Generates reports
- Posts comment with results (doesn't deploy to Pages)

## Benefits of This Architecture

1. **Speed**: Parallel execution reduces total time from ~8m to ~3m
2. **Isolation**: Each test type runs in dedicated container
3. **Browser Coverage**: BDD tests verify across 3 browsers
4. **Historical Tracking**: 20 runs preserved for trend analysis
5. **User-Friendly**: Beautiful UI for non-technical stakeholders
6. **Comprehensive**: Unit, API, and UI tests all in one pipeline
7. **Transparency**: All reports publicly accessible via GitHub Pages
8. **PR Integration**: Automatic comments on pull requests
9. **Trend Analysis**: Allure history shows trends over time
10. **Professional**: Production-ready reporting infrastructure

## Maintenance

### Keeping Reports
- **Default**: Last 20 runs preserved
- **Modify**: Change `keep_reports: 20` in workflow

### Adding Browsers
```yaml
matrix:
  browser: [firefox, chromium, webkit, edge, safari]
```

### Adjusting Resources
- Container sizes can be increased if tests timeout
- Parallel workers can be increased for faster execution

## Future Enhancements

Possible additions:
- Slack/Email notifications on failures
- Performance benchmarking
- Visual regression testing
- Security scanning integration
- Dependency vulnerability checks
- Code quality metrics (SonarQube)
- Deployment to staging environment
- Load testing integration
