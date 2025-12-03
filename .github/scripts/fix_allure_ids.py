#!/usr/bin/env python3
"""
Fix Allure result files to have unique historyId values per browser.
This prevents Allure from deduplicating tests from different browser runs.
"""
import json
import sys
from pathlib import Path


def fix_browser_results(results_dir: Path, browser: str):
    """Add browser suffix to historyId and add browser parameter to all result files."""
    modified_count = 0

    for result_file in results_dir.glob("*-result.json"):
        try:
            # Read the result file
            with open(result_file, 'r') as f:
                data = json.load(f)

            # Modify historyId to be unique per browser
            if "historyId" in data:
                data["historyId"] = f"{data['historyId']}-{browser}"

            # Add browser as a parameter
            if "parameters" not in data:
                data["parameters"] = []
            data["parameters"].append({"name": "browser", "value": browser})

            # Add browser as a label
            if "labels" not in data:
                data["labels"] = []
            data["labels"].append({"name": "browser", "value": browser})

            # Modify fullName to include browser
            if "fullName" in data:
                data["fullName"] = f"{data['fullName']}[{browser}]"

            # Write back to file
            with open(result_file, 'w') as f:
                json.dump(data, f, indent=2)

            modified_count += 1

        except Exception as e:
            print(f"Error processing {result_file}: {e}", file=sys.stderr)
            continue

    return modified_count


def main():
    if len(sys.argv) != 3:
        print("Usage: fix_allure_ids.py <results_directory> <browser_name>")
        sys.exit(1)

    results_dir = Path(sys.argv[1])
    browser = sys.argv[2]

    if not results_dir.exists():
        print(f"Error: Directory {results_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    count = fix_browser_results(results_dir, browser)
    print(f"Modified {count} result files with browser={browser}")


if __name__ == "__main__":
    main()
