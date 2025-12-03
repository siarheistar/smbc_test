# Playwright Test Reporting

**Date:** December 3, 2025
**Status:** ✅ CONFIGURED

## Overview

Playwright tests now automatically generate an HTML report after each test run, including screenshots, videos (on failure), and trace files for debugging.

## What Was Configured

### 1. HTML Report Generation

**File:** `pytest.ini`

```ini
[pytest]
addopts =
    --html=playwright-report.html
    --self-contained-html
    --screenshot=on
    --video=retain-on-failure
    --tracing=retain-on-failure
```

### 2. Dependencies Added

**File:** `requirements.txt`
```
pytest-html==4.1.1
```

### 3. Artifacts Excluded from Git

**File:** `.gitignore`
```
playwright-report.html
.playwright-screenshots/
test-results/
```

## Generated Artifacts

After running Playwright/BDD tests, you'll get:

### 1. HTML Report
- **File:** `playwright-report.html`
- **Location:** Project root
- **Contents:**
  - Test results summary
  - Pass/fail status for each test
  - Execution time
  - Environment details
  - Links to screenshots and videos

**View report:**
```bash
open playwright-report.html
```

### 2. Test Results Directory
- **Directory:** `test-results/`
- **Contents:**
  - Screenshots (always captured)
  - Videos (only for failed tests)
  - Trace files (only for failed tests)

**Structure:**
```
test-results/
└── tests-bdd-test-anagram-ui-py-test-check-if-two-strings-are-anagrams-listen-silent-true/
    ├── trace.zip          # Playwright trace (failures only)
    ├── video.webm         # Test recording (failures only)
    └── test-finished-1.png # Screenshot
```

## Usage

### Running Tests with Report

**BDD/UI Tests:**
```bash
# Run all BDD tests - generates playwright-report.html
pytest tests/bdd/

# Run specific test
pytest tests/bdd/test_anagram_ui.py::test_check_if_two_strings_are_anagrams[listen-silent-true]

# View report
open playwright-report.html
```

**With specific browser:**
```bash
pytest tests/bdd/ --browser firefox
pytest tests/bdd/ --browser chromium
pytest tests/bdd/ --browser webkit
```

**With headed mode (visible browser):**
```bash
pytest tests/bdd/ --headed
```

### What Gets Captured

| Artifact | When Captured | Location |
|----------|---------------|----------|
| **HTML Report** | Every run | `playwright-report.html` |
| **Screenshots** | Always | `test-results/*/test-*.png` |
| **Videos** | Failures only | `test-results/*/video.webm` |
| **Traces** | Failures only | `test-results/*/trace.zip` |

### Trace Files

**Trace files** are powerful debugging tools that capture:
- Network requests
- Console logs
- DOM snapshots
- Screenshots at each step
- Timing information

**View traces:**
```bash
# Install Playwright CLI (if not already installed)
playwright install

# Open trace viewer
playwright show-trace test-results/*/trace.zip
```

## Configuration Options

### pytest.ini Settings

```ini
--screenshot=on                  # Always capture screenshots
--video=retain-on-failure       # Record video only for failures
--tracing=retain-on-failure     # Capture trace only for failures
--html=playwright-report.html   # Generate HTML report
--self-contained-html           # Embed CSS/JS in HTML (portable)
```

### Alternative Configurations

**Capture everything (for debugging):**
```ini
--screenshot=on
--video=on                      # Always record video
--tracing=on                    # Always capture trace
```

**Minimal (fastest):**
```ini
--screenshot=off
--video=off
--tracing=off
--html=playwright-report.html
```

## CI/CD Integration

### GitHub Actions

The CI/CD pipeline should:

1. **Run tests** with artifacts
2. **Upload** playwright-report.html
3. **Upload** test-results directory
4. **Publish** to GitHub Pages or artifacts

**Example workflow step:**
```yaml
- name: Run BDD Tests
  run: |
    pytest tests/bdd/ \
      --browser firefox \
      --screenshot=on \
      --video=retain-on-failure

- name: Upload Playwright Report
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report.html

- name: Upload Test Results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: test-results/
```

## Viewing Reports

### Local Development

```bash
# Run tests
pytest tests/bdd/

# Open HTML report
open playwright-report.html

# View trace (if test failed)
playwright show-trace test-results/*/trace.zip
```

### CI/CD Artifacts

After pipeline runs:
1. Go to GitHub Actions run
2. Scroll to "Artifacts" section
3. Download `playwright-report` and `test-results`
4. Open `playwright-report.html` locally

## Report Features

The HTML report includes:

### Summary Section
- Total tests run
- Passed/Failed/Skipped counts
- Total execution time
- Environment information

### Test Details
- Individual test results
- Execution time per test
- Error messages (for failures)
- Stack traces (for failures)

### Links to Artifacts
- Screenshots embedded
- Links to videos (failures)
- Links to trace files (failures)

## Examples

### Successful Test Report
```
Test: test_check_if_two_strings_are_anagrams[listen-silent-true]
Status: PASSED ✓
Duration: 4.10s
Browser: firefox
Screenshot: ✓ Available
```

### Failed Test Report
```
Test: test_check_if_two_strings_are_anagrams[invalid-input-true]
Status: FAILED ✗
Duration: 3.45s
Browser: firefox
Screenshot: ✓ Available
Video: ✓ Available
Trace: ✓ Available
Error: AssertionError: Expected TRUE but got FALSE
```

## Debugging Failed Tests

### Step 1: Check HTML Report
```bash
open playwright-report.html
# Look at error message and stack trace
```

### Step 2: View Screenshot
```bash
# Screenshot is embedded in HTML report
# Or find in: test-results/*/test-*.png
```

### Step 3: Watch Video (if available)
```bash
open test-results/*/video.webm
```

### Step 4: Inspect Trace
```bash
# Most detailed debugging
playwright show-trace test-results/*/trace.zip

# Trace viewer shows:
# - Every action taken
# - Network requests
# - Console logs
# - DOM snapshots
# - Screenshots at each step
```

## Cleaning Up Artifacts

### Manual Cleanup
```bash
# Remove all artifacts
rm -rf playwright-report.html test-results/

# Artifacts are regenerated on next test run
```

### Automated Cleanup
Add to your test script:
```bash
#!/bin/bash
# Clean old artifacts
rm -rf playwright-report.html test-results/

# Run tests (generates new artifacts)
pytest tests/bdd/

# Open report
open playwright-report.html
```

## Best Practices

### 1. Always Capture Screenshots
- ✅ Minimal overhead
- ✅ Helpful for debugging
- ✅ Visual confirmation of test state

### 2. Videos on Failure Only
- ✅ Saves disk space
- ✅ Only captures when needed
- ✅ Faster test execution

### 3. Traces on Failure Only
- ✅ Most detailed debugging info
- ✅ Only when you need it
- ✅ Minimal performance impact

### 4. Self-Contained HTML
- ✅ Single file report
- ✅ Easy to share
- ✅ No external dependencies

## Troubleshooting

### Report Not Generated

**Check:**
```bash
# Verify pytest-html is installed
pip list | grep pytest-html

# Check pytest.ini has --html option
cat pytest.ini | grep html
```

**Fix:**
```bash
pip install pytest-html==4.1.1
```

### Screenshots Missing

**Check configuration:**
```ini
# pytest.ini should have:
--screenshot=on
```

### Videos Not Recording

**Check:**
```bash
# Videos only on failure by default
--video=retain-on-failure

# To always record:
--video=on
```

### Trace Files Too Large

**Reduce trace capture:**
```ini
# Only on failure (default)
--tracing=retain-on-failure

# Or disable entirely
--tracing=off
```

## Summary

✅ **Playwright reports configured**
- HTML report generated after each run
- Screenshots always captured
- Videos and traces on failure
- Self-contained, portable HTML
- Already excluded from git

**Quick commands:**
```bash
# Run tests → generates report
pytest tests/bdd/

# View report
open playwright-report.html

# View trace (if failed)
playwright show-trace test-results/*/trace.zip
```

---

**Related Files:**
- [pytest.ini](../pytest.ini) - Pytest configuration
- [.gitignore](../.gitignore) - Excludes artifacts
- [requirements.txt](../requirements.txt) - Dependencies
- [tests/bdd/test_anagram_ui.py](../tests/bdd/test_anagram_ui.py) - BDD tests

**Documentation:**
- [pytest-html docs](https://pytest-html.readthedocs.io/)
- [Playwright test docs](https://playwright.dev/python/docs/test-runners)
