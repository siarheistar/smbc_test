#!/usr/bin/env python3
"""
Script to customize Allure report with purple gradient theme and custom header.
This adds a beautiful header with test statistics and navigation links.
"""

import json
import pathlib
import sys
from datetime import datetime

def calculate_test_stats(allure_results_dir: str = "allure-results") -> dict:
    """Calculate test statistics from Allure results."""
    allure_dir = pathlib.Path(allure_results_dir)
    total = passed = failed = broken = skipped = 0

    for path in allure_dir.rglob("*-result.json"):
        try:
            data = json.loads(path.read_text())
            status = str(data.get("status", "")).lower()
            total += 1
            if status == "passed":
                passed += 1
            elif status == "failed":
                failed += 1
            elif status == "broken":
                broken += 1
            elif status in ["skipped", "pending"]:
                skipped += 1
        except Exception as e:
            print(f"Warning: Could not read {path}: {e}")
            continue

    pass_rate = round((passed * 100 / total), 1) if total > 0 else 0.0

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "broken": broken,
        "skipped": skipped,
        "passRate": pass_rate,
        "timestamp": datetime.now().isoformat()
    }

def create_custom_css(output_path: str = "allure-report/custom-style.css"):
    """Create custom CSS file with purple gradient theme."""
    css_content = """/* Custom Purple Gradient Theme for Allure Report */

/* Add purple gradient background to body */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    min-height: 100vh;
}

/* Custom header banner */
.custom-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px 30px;
    margin: 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    position: relative;
    z-index: 1000;
}

.custom-header h1 {
    margin: 0 0 10px 0;
    font-size: 28px;
    font-weight: 600;
    color: white;
}

.custom-header .run-info {
    display: flex;
    gap: 30px;
    align-items: center;
    flex-wrap: wrap;
    margin-top: 10px;
}

.custom-header .info-item {
    display: flex;
    align-items: center;
    gap: 8px;
}

.custom-header .info-label {
    opacity: 0.9;
    font-size: 14px;
}

.custom-header .info-value {
    font-weight: 600;
    font-size: 16px;
    background: rgba(255, 255, 255, 0.2);
    padding: 4px 12px;
    border-radius: 6px;
}

.custom-header .nav-links {
    margin-top: 15px;
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}

.custom-header .nav-link {
    color: white;
    text-decoration: none;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    font-size: 14px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.custom-header .nav-link:hover {
    background: rgba(255, 255, 255, 0.25);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Style the main content area */
#content {
    background: white;
    margin: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

/* Enhance the sidebar */
.side-nav {
    background: #f8f9fa !important;
}

/* Style badges with purple theme */
.badge--passed {
    background: #10b981 !important;
}

.badge--failed {
    background: #ef4444 !important;
}

.badge--broken {
    background: #f59e0b !important;
}

.badge--skipped {
    background: #6b7280 !important;
}

/* Enhanced statistics cards */
.statistic__row {
    transition: all 0.3s ease;
}

.statistic__row:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

/* Purple accent for links */
a {
    color: #667eea !important;
}

a:hover {
    color: #5568d3 !important;
}

/* Enhanced buttons */
.button, .btn {
    background: #667eea !important;
    transition: all 0.3s ease;
}

.button:hover, .btn:hover {
    background: #5568d3 !important;
    transform: translateY(-2px);
}

/* Status badges with better styling */
.status-toggle {
    border-radius: 8px !important;
}

/* Severity badges */
.severity--critical {
    background: #ef4444 !important;
}

.severity--high {
    background: #f59e0b !important;
}

.severity--normal {
    background: #667eea !important;
}

.severity--low {
    background: #6b7280 !important;
}

/* Enhanced pane styling */
.pane {
    background: white;
    border-radius: 8px;
}

/* Table enhancements */
.table {
    border-radius: 8px;
    overflow: hidden;
}

.table__row:hover {
    background: rgba(102, 126, 234, 0.05) !important;
}

/* Widget enhancements */
.widget {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.widget:hover {
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.15);
}
"""

    pathlib.Path(output_path).write_text(css_content)
    print(f"✓ Created custom CSS at {output_path}")

def create_custom_header(stats: dict) -> str:
    """Generate custom header HTML with test statistics."""
    return f"""    <!-- Custom Header with Purple Gradient -->
    <div class="custom-header">
        <h1>🧪 Anagram Checker - Test Automation Report</h1>
        <div class="run-info">
            <div class="info-item">
                <span class="info-label">Total Tests:</span>
                <span class="info-value">{stats['total']}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Passed:</span>
                <span class="info-value" style="background: rgba(16, 185, 129, 0.3);">✅ {stats['passed']}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Failed:</span>
                <span class="info-value" style="background: rgba(239, 68, 68, 0.3);">❌ {stats['failed']}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Broken:</span>
                <span class="info-value" style="background: rgba(245, 158, 11, 0.3);">⚠️ {stats['broken']}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Pass Rate:</span>
                <span class="info-value" style="background: rgba(16, 185, 129, 0.3);">{stats['passRate']}%</span>
            </div>
        </div>
        <div class="nav-links">
            <a href="#" class="nav-link">📊 Overview</a>
            <a href="#categories" class="nav-link">📁 Categories</a>
            <a href="#suites" class="nav-link">📋 Suites</a>
            <a href="#graphs" class="nav-link">📈 Graphs</a>
            <a href="../htmlcov/index.html" class="nav-link" target="_blank">📉 Coverage Report</a>
            <a href="../newman-report.html" class="nav-link" target="_blank">🔌 Newman API Tests</a>
        </div>
    </div>"""

def customize_allure_report(
    report_dir: str = "allure-report",
    results_dir: str = "allure-results"
):
    """Main function to customize Allure report."""
    print("🎨 Customizing Allure Report...")
    print("=" * 60)

    # Calculate statistics
    print("\n📊 Calculating test statistics...")
    stats = calculate_test_stats(results_dir)
    print(f"  Total Tests: {stats['total']}")
    print(f"  Passed: {stats['passed']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Broken: {stats['broken']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Pass Rate: {stats['passRate']}%")

    # Save statistics
    stats_path = pathlib.Path(report_dir) / "test-stats.json"
    stats_path.write_text(json.dumps(stats, indent=2))
    print(f"\n✓ Saved statistics to {stats_path}")

    # Create custom CSS
    print("\n🎨 Creating custom CSS...")
    css_path = pathlib.Path(report_dir) / "custom-style.css"
    create_custom_css(str(css_path))

    # Inject custom header and CSS into index.html
    print("\n📝 Injecting custom header into index.html...")
    index_path = pathlib.Path(report_dir) / "index.html"

    if not index_path.exists():
        print(f"❌ Error: {index_path} not found!")
        print("   Please generate Allure report first using: allure generate")
        sys.exit(1)

    html_content = index_path.read_text()

    # Add custom CSS link if not already present
    if "custom-style.css" not in html_content:
        html_content = html_content.replace(
            '<link rel="stylesheet" type="text/css" href="plugin/screen-diff/styles.css">',
            '<link rel="stylesheet" type="text/css" href="plugin/screen-diff/styles.css">\n    <link rel="stylesheet" type="text/css" href="custom-style.css">'
        )

    # Add custom header if not already present
    if "custom-header" not in html_content:
        custom_header = create_custom_header(stats)
        html_content = html_content.replace(
            '<body>\n    <div id="alert"></div>',
            f'<body>\n{custom_header}\n    <div id="alert"></div>'
        )

    # Write updated HTML
    index_path.write_text(html_content)
    print(f"✓ Updated {index_path}")

    print("\n" + "=" * 60)
    print("✅ Allure report customization complete!")
    print(f"🌐 Open the report: file://{index_path.absolute()}")
    print("=" * 60)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Customize Allure report with purple gradient theme"
    )
    parser.add_argument(
        "--report-dir",
        default="allure-report",
        help="Path to Allure report directory (default: allure-report)"
    )
    parser.add_argument(
        "--results-dir",
        default="allure-results",
        help="Path to Allure results directory (default: allure-results)"
    )

    args = parser.parse_args()

    try:
        customize_allure_report(args.report_dir, args.results_dir)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
