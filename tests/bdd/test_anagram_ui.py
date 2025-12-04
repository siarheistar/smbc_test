"""
BDD UI tests using Playwright
"""
import allure
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page
from pathlib import Path
import os
from dotenv import load_dotenv
from src.config import settings

# Load environment variables
load_dotenv()

# Get configuration
TEST_SERVER_URL = os.getenv("TEST_SERVER_URL", "http://localhost:8000")

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
FEATURES_DIR = PROJECT_ROOT / "features"

# Load all scenarios from both feature parts so they can be run in parallel
FEATURE_FILES = [
    FEATURES_DIR / "Anagram_Checker_Part1.feature",
    FEATURES_DIR / "Anagram_Checker_Part2.feature",
]

for feature_file in FEATURE_FILES:
    scenarios(str(feature_file))


@allure.step('Given the input strings "{input1}" and "{input2}"')
@given(parsers.re(r'the input strings "(?P<input1>.*)" and "(?P<input2>.*)"'), target_fixture="inputs")
def given_inputs(page: Page, input1, input2):
    """Enter input strings into the form"""
    # Navigate to the application
    page.goto(TEST_SERVER_URL)
    page.wait_for_load_state("networkidle")

    with allure.step(f"Entering '{input1}' into Input 1 field"):
        input1_field = page.get_by_test_id("input1")
        input1_field.clear()
        input1_field.fill(input1)

    with allure.step(f"Entering '{input2}' into Input 2 field"):
        input2_field = page.get_by_test_id("input2")
        input2_field.clear()
        input2_field.fill(input2)

    # Take screenshot
    screenshot = page.screenshot()
    allure.attach(screenshot, name="Input Form", attachment_type=allure.attachment_type.PNG)

    return {"input1": input1, "input2": input2, "page": page}


@allure.step("When I check if they are anagrams")
@when("I check if they are anagrams")
def when_check_anagrams(inputs):
    """Click the check button"""
    page = inputs["page"]

    with allure.step("Clicking the Check Anagram button"):
        check_button = page.get_by_test_id("check-button")
        check_button.click()

    # If inputs are empty, native HTML validation blocks form submit; capture its message and skip waiting for result.
    if not inputs["input1"].strip() or not inputs["input2"].strip():
        validation_message = page.eval_on_selector(
            '[data-testid="input1"]',
            "el => el.validationMessage"
        ) or page.eval_on_selector(
            '[data-testid="input2"]',
            "el => el.validationMessage"
        )
        inputs["validation_message"] = validation_message
        return

    # Check for validation or API error
    error_div = page.get_by_test_id("error")
    try:
        error_div.wait_for(state="visible", timeout=1000)
        inputs["error_message"] = error_div.text_content()
        return
    except Exception:
        pass

    # Wait for result to appear
    result_div = page.get_by_test_id("result")
    result_div.wait_for(state="visible", timeout=5000)

    # Take screenshot of result
    screenshot = page.screenshot()
    allure.attach(screenshot, name="Result", attachment_type=allure.attachment_type.PNG)

    inputs["result_element"] = result_div


@allure.step('Then the result should be "{output}"')
@then(parsers.re(r'the result should be "(?P<output>.*)"'))
def then_result_should_be(inputs, output):
    """Verify the result"""
    if output.lower() == "error":
        with allure.step("Verifying validation error is shown"):
            error_msg = inputs.get("error_message")
            validation_msg = inputs.get("validation_message")
            msg = error_msg or validation_msg
            assert msg, "Expected validation error message to be displayed"
            if error_msg:
                min_len = settings.min_input_length
                max_len = settings.max_input_length
                assert str(min_len) in error_msg or str(max_len) in error_msg, f"Expected length limits {min_len}-{max_len} in message, got: {error_msg}"
        allure.attach(
            f"Input 1: {inputs['input1']}\nInput 2: {inputs['input2']}\nError: {msg}",
            name="Validation Error Summary",
            attachment_type=allure.attachment_type.TEXT
        )
        return

    # If validation blocked submission, assert a validation message exists and stop.
    if "validation_message" in inputs:
        with allure.step("Verifying native validation is shown for empty input"):
            msg = inputs["validation_message"]
            assert msg, "Expected browser validation message for empty input"
        return

    result_element = inputs["result_element"]
    result_text = result_element.text_content()

    expected_result = output.lower() == "true"

    with allure.step(f"Verifying result is {output}"):
        if expected_result:
            assert "TRUE" in result_text, f"Expected TRUE but got: {result_text}"
            # Verify correct CSS class
            class_name = result_element.get_attribute("class")
            assert "result-true" in class_name, f"Expected 'result-true' class but got: {class_name}"
        else:
            assert "FALSE" in result_text, f"Expected FALSE but got: {result_text}"
            # Verify correct CSS class
            class_name = result_element.get_attribute("class")
            assert "result-false" in class_name, f"Expected 'result-false' class but got: {class_name}"

    allure.attach(
        f"Input 1: {inputs['input1']}\nInput 2: {inputs['input2']}\nResult: {result_text}",
        name="Test Summary",
        attachment_type=allure.attachment_type.TEXT
    )
