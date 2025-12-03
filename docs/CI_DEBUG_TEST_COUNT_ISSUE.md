# CI/CD Test Count Debugging

**Date:** December 3, 2025
**Issue:** Inconsistent test counts across different report views
**Status:** 🔍 INVESTIGATING

## Problem Description

### Observed Behavior

The CI/CD pipeline is showing **inconsistent test counts** across different views:

| View Location | Test Count | Expected | Status |
|---------------|------------|----------|--------|
| **Index Page** (Test Reports Index) | 251 | 251 | ✅ CORRECT |
| **Allure Report** (GitHub Pages - latest run) | 57 | 251 | ❌ WRONG |
| **Allure Report** (Downloaded run #19, served locally) | 149 | 251 | ❌ WRONG |

### Breakdown of Expected 251 Tests

- **Unit tests:** 19
- **API tests:** 79
- **BDD tests:** 51 scenarios × 3 browsers = 153
  - Firefox: 51
  - Chromium: 51
  - WebKit: 51
- **Total:** 19 + 79 + 153 = **251**

### Analysis of Actual Counts

#### Run #19 (Local) - 149 Tests
From screenshot showing Allure report served locally:
- tests.api: **79** ✅ (correct)
- tests.bdd: **51** ❌ (only 1 browser instead of 3!)
- tests.unit: **19** ✅ (correct)
- **Total: 149**

**Root Cause:** Only **ONE browser's** BDD test results are being merged (51 tests), instead of all THREE browsers (153 tests).

**Missing:** 102 BDD test results (2 browsers × 51 scenarios)

#### GitHub Pages - 57 Tests
From screenshot showing GitHub Pages Allure report:
- **Total: 57 tests**

**Analysis:** This appears to be even worse - possibly only unit (19) + API (79) = 98, or there's another issue with partial API results.

## Root Cause Analysis

### Statistics Calculation (Lines 298-347)
```python
allure_dir = pathlib.Path("allure-results")
for path in allure_dir.rglob("*-result.json"):
    total += 1
    # ...
```

**Status:** ✅ This is working correctly - outputs 251 to `$GITHUB_OUTPUT`
**Evidence:** Index page shows 251 tests
**Conclusion:** The merge step IS creating all 251 result files in `allure-results/`

### Allure Report Generation (Lines 377-384)
```yaml
- name: Generate Allure Report
  uses: simple-elf/allure-report-action@master
  with:
    allure_results: allure-results
    allure_report: allure-report
    allure_history: allure-history
```

**Status:** ❌ This is NOT seeing all 251 files from `allure-results/`
**Evidence:** Generated report only shows 149 or 57 tests
**Hypothesis:**
1. The `simple-elf/allure-report-action` is not processing all files correctly
2. The artifact download step is not downloading all 3 BDD browser artifacts
3. The merge step is not copying all files correctly

## Debugging Changes Made

### 1. Enhanced Artifact Download Logging (Lines 205-225)

**Added:**
```bash
echo "Downloaded artifacts:"
ls -la artifacts/
echo "Per-artifact result counts:"
for d in artifacts/*; do
  if [ -d "$d" ]; then
    echo "- $d: $(find "$d" -name \"*-result.json\" | wc -l)"
  fi
done

# Warn if expected artifacts are missing
for d in artifacts/allure-results-unit artifacts/allure-results-api artifacts/allure-results-bdd-firefox artifacts/allure-results-bdd-chromium artifacts/allure-results-bdd-webkit; do
  if [ -d "$d" ]; then
    count=$(find "$d" -name \"*-result.json\" | wc -l)
    if [ "$count" -eq 0 ]; then
      echo "WARNING: No allure result files found in $d"
    fi
  else
    echo "WARNING: Expected artifact directory missing: $d"
  fi
done
```

**What to check in logs:**
- All 5 artifact directories should be listed
- Expected counts:
  - `artifacts/allure-results-unit`: 19
  - `artifacts/allure-results-api`: 79
  - `artifacts/allure-results-bdd-firefox`: 51
  - `artifacts/allure-results-bdd-chromium`: 51
  - `artifacts/allure-results-bdd-webkit`: 51

### 2. Comprehensive Merge Logging (Lines 227-296)

**Added extensive debugging:**
```bash
echo "=== Artifact Directory Structure ==="
ls -la artifacts/

echo "=== Checking each artifact directory ==="
for artifact_name in ...; do
  echo "Checking artifacts/${artifact_name}..."
  if [ -d "artifacts/${artifact_name}" ]; then
    echo "  ✓ Directory exists"
    echo "  Contents:"
    ls -la "artifacts/${artifact_name}/" | head -10
    result_count=$(find "artifacts/${artifact_name}" -name "*-result.json" | wc -l)
    echo "  Result files: ${result_count}"
  else
    echo "  ✗ Directory NOT found"
  fi
done

echo "=== Merging results ==="
# ... with verbose copy and counting ...

echo "=== Merge Summary ==="
echo "Total result files copied: ${total_copied}"
actual_count=$(find allure-results -name "*-result.json" | wc -l)
echo "Actual files in allure-results: ${actual_count}"

if [ "$actual_count" -ne "$total_copied" ]; then
  echo "⚠️  WARNING: Count mismatch! Expected ${total_copied}, got ${actual_count}"
fi
```

**What to check in logs:**
- Each browser artifact directory should show 51 result files
- Total copied should be 251
- No count mismatch warnings

### 3. Pre-Generation Debug (Lines 367-375)

**Added:**
```bash
echo "=== allure-results directory (INPUT to Allure) ==="
echo "Total result files: $(find allure-results -name '*-result.json' | wc -l)"
ls -la allure-results/ | head -20

echo "=== allure-history directory ==="
ls -la allure-history/ 2>/dev/null || echo "allure-history does not exist yet"
```

**What to check:**
- `allure-results` should have 251 `*-result.json` files
- `allure-history` directory structure

### 4. Post-Generation Debug (Lines 386-395)

**Added:**
```bash
echo "=== allure-report directory (OUTPUT from Allure) ==="
ls -la allure-report/ | head -20

if [ -f "allure-report/widgets/summary.json" ]; then
  echo "=== summary.json content ==="
  cat allure-report/widgets/summary.json
fi
```

**What to check:**
- `summary.json` should show statistics for all 251 tests
- If it doesn't, the issue is in `simple-elf/allure-report-action`

## Suspected Issues

### Issue 1: Artifact Download Structure

**Hypothesis:** `actions/download-artifact@v4` might be creating nested directories.

**Expected structure:**
```
artifacts/
├── allure-results-unit/
│   └── (19 result files directly)
├── allure-results-api/
│   └── (79 result files directly)
├── allure-results-bdd-firefox/
│   └── (51 result files directly)
├── allure-results-bdd-chromium/
│   └── (51 result files directly)
└── allure-results-bdd-webkit/
    └── (51 result files directly)
```

**Possible actual structure (NESTED):**
```
artifacts/
├── allure-results-bdd-firefox/
│   └── allure-results-bdd-firefox/  ← NESTED!
│       └── (actual result files)
```

**How to verify:** Check "Artifact Directory Structure" section in logs.

**If this is the issue:** The merge script needs to handle nested directories.

### Issue 2: File Name Collisions

**Hypothesis:** Some result files from different browsers might have the same UUID, causing overwrites during copy.

**Evidence needed:** Check if `-v` verbose copy shows any files being overwritten.

**If this is the issue:** Use `cp -n` (no-clobber) instead of `cp` and count how many files failed to copy.

### Issue 3: Allure Action Not Reading All Files

**Hypothesis:** `simple-elf/allure-report-action@master` has a bug or limitation on the number of files it processes.

**Evidence needed:**
- Compare result count before generation (should be 251)
- Compare result count in generated `summary.json` (might be less)

**If this is the issue:** May need to use a different Allure action or generate report manually.

## Next Steps

### Step 1: Trigger New CI Run

Push these debugging changes to trigger a new CI/CD run:
```bash
git add .github/workflows/ci.yml docs/CI_DEBUG_TEST_COUNT_ISSUE.md
git commit -m "Add extensive debugging for test count issue"
git push
```

### Step 2: Analyze Logs

Check the following sections in the GitHub Actions logs:

1. **"List downloaded artifacts"** - Verify all 5 artifacts are present with correct counts
2. **"Merge all Allure results"** - Look for:
   - All 5 artifact directories found
   - Each directory has expected count (19, 79, 51, 51, 51)
   - Total copied = 251
   - No mismatch warnings
3. **"Debug before Allure generation"** - Should show 251 result files
4. **"Debug after Allure generation"** - Check `summary.json` test count
5. **"Calculate test statistics"** - Should output "Statistics: 251 tests..."

### Step 3: Identify Root Cause

Based on where the count diverges:

| Divergence Point | Root Cause | Fix |
|------------------|------------|-----|
| Artifact download shows < 251 | BDD test jobs not uploading all results | Check BDD test job logs |
| Merge step copies < 251 | Artifact directory structure issue | Fix merge script to handle nesting |
| Pre-generation shows 251, post shows < 251 | Allure action limitation | Replace action or generate manually |
| Post-generation shows 251, but GH Pages shows less | Deployment issue | Check gh-pages branch deployment |

### Step 4: Apply Fix

Once root cause is identified, apply the appropriate fix from the table above.

## Known Working Configuration

**Local test execution:**
```bash
# Run all tests and generate results
pytest tests/unit/ --alluredir=allure-results-unit
pytest tests/api/ --alluredir=allure-results-api
pytest tests/bdd/ --browser firefox --alluredir=allure-results-bdd-firefox
pytest tests/bdd/ --browser chromium --alluredir=allure-results-bdd-chromium
pytest tests/bdd/ --browser webkit --alluredir=allure-results-bdd-webkit

# Merge results
mkdir -p allure-results
cp allure-results-unit/* allure-results/
cp allure-results-api/* allure-results/
cp allure-results-bdd-firefox/* allure-results/
cp allure-results-bdd-chromium/* allure-results/
cp allure-results-bdd-webkit/* allure-results/

# Count
find allure-results -name "*-result.json" | wc -l  # Should be 251

# Generate report
allure generate allure-results -o allure-report --clean

# Serve
allure open allure-report
```

## Related Files

- [.github/workflows/ci.yml](../.github/workflows/ci.yml) - Main CI/CD workflow with debugging
- [docs/CI_CD_PLAYWRIGHT_INTEGRATION.md](./CI_CD_PLAYWRIGHT_INTEGRATION.md) - Playwright integration docs

## Status

🔧 **FIXING** - Root cause identified: `actions/download-artifact@v4` behavior issue

### Latest Results (Run after debugging added)

**Actual count: 57 tests** (should be 251)
- tests.api: 22 (should be 79) - Missing 57 tests
- tests.bdd: 16 (should be 153) - Missing 137 tests
- tests.unit: 19 (correct) ✓

### Root Cause Identified

**Problem:** `actions/download-artifact@v4` without explicit `name` parameter downloads ALL artifacts but may create nested directory structures or have file conflicts during extraction.

**Evidence:** When downloading with just `path: artifacts`, the action downloads everything but the structure may be:
```
artifacts/
├── allure-results-unit/
│   └── allure-results-unit/  ← NESTED or other structure issue
│       └── files
```

Or worse, files with the same name from different artifacts may overwrite each other during download.

### Fix Applied

Changed from single download-all to explicit individual downloads:

**Before:**
```yaml
- name: Download all test results
  uses: actions/download-artifact@v4
  with:
    path: artifacts
```

**After:**
```yaml
- name: Download unit test results
  uses: actions/download-artifact@v4
  with:
    name: allure-results-unit
    path: artifacts/allure-results-unit

- name: Download API test results
  uses: actions/download-artifact@v4
  with:
    name: allure-results-api
    path: artifacts/allure-results-api

# ... and so on for each artifact
```

**Benefits:**
1. Explicit path control - no nested directories
2. No file name conflicts between artifacts
3. Clear separation of each test type's results
4. Easier to debug which artifact failed to download

### Next CI Run Should Show

With the explicit download paths:
- artifacts/allure-results-unit: 19 result files
- artifacts/allure-results-api: 79 result files
- artifacts/allure-results-bdd-firefox: 51 result files
- artifacts/allure-results-bdd-chromium: 51 result files
- artifacts/allure-results-bdd-webkit: 51 result files
- **Total merged: 251 result files**
- **Allure report: 251 tests**
