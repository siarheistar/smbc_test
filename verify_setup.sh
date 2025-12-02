#!/bin/bash

# Verify project setup and structure

echo "======================================"
echo "Anagram Checker - Setup Verification"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -n "Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found"
    exit 1
fi

# Check pip
echo -n "Checking pip... "
if command -v pip &> /dev/null; then
    PIP_VERSION=$(pip --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} pip $PIP_VERSION"
else
    echo -e "${RED}✗${NC} pip not found"
    exit 1
fi

# Check virtual environment
echo -n "Checking virtual environment... "
if [ -d "venv" ] || [ -d ".venv" ]; then
    echo -e "${GREEN}✓${NC} Found"
else
    echo -e "${YELLOW}⚠${NC} Not found (will create)"
fi

# Check required files
echo ""
echo "Checking project structure:"

files=(
    "src/anagram_checker.py"
    "src/models.py"
    "src/app.py"
    "tests/unit/test_anagram_checker.py"
    "tests/api/test_api.py"
    "tests/bdd/test_anagram_ui.py"
    "features/Anagram_Checker.feature"
    "features/Anagram_Checker_Part1.feature"
    "features/Anagram_Checker_Part2.feature"
    "requirements.txt"
    "pytest.ini"
    "conftest.py"
    "README.md"
    ".github/workflows/ci.yml"
)

for file in "${files[@]}"; do
    echo -n "  $file... "
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
    fi
done

# Check scripts
echo ""
echo "Checking scripts:"
scripts=(
    "start_app.sh"
    "run_tests.sh"
    "run_unit_tests.sh"
    "run_api_tests.sh"
    "run_bdd_tests.sh"
    "run_parallel_tests.sh"
)

for script in "${scripts[@]}"; do
    echo -n "  $script... "
    if [ -f "$script" ] && [ -x "$script" ]; then
        echo -e "${GREEN}✓${NC} (executable)"
    elif [ -f "$script" ]; then
        echo -e "${YELLOW}⚠${NC} (not executable - run: chmod +x $script)"
    else
        echo -e "${RED}✗${NC}"
    fi
done

# Check if dependencies are installed (if venv exists and is activated)
echo ""
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Checking dependencies (venv active):"

    packages=(
        "fastapi"
        "uvicorn"
        "pytest"
        "pytest-bdd"
        "pytest-cov"
        "playwright"
        "allure-pytest"
    )

    for package in "${packages[@]}"; do
        echo -n "  $package... "
        if pip show "$package" &> /dev/null; then
            VERSION=$(pip show "$package" | grep Version | cut -d' ' -f2)
            echo -e "${GREEN}✓${NC} $VERSION"
        else
            echo -e "${RED}✗${NC} Not installed"
        fi
    done

    # Check Playwright browsers
    echo ""
    echo -n "Checking Playwright browsers... "
    if playwright --version &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}⚠${NC} Run: playwright install"
    fi
else
    echo -e "${YELLOW}Virtual environment not activated${NC}"
    echo "Activate with: source venv/bin/activate"
fi

# Summary
echo ""
echo "======================================"
echo "Verification Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. If venv not found: python3 -m venv venv"
echo "2. Activate venv: source venv/bin/activate"
echo "3. Install dependencies: pip install -r requirements.txt"
echo "4. Install Playwright: playwright install"
echo "5. Start app: ./start_app.sh"
echo "6. Run tests: ./run_tests.sh"
echo ""
echo "For detailed setup, see: SETUP.md"
echo "For demo walkthrough, see: DEMO.md"
