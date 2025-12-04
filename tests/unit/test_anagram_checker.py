"""
Unit tests for AnagramChecker
"""
import pytest
import allure
from src.anagram_checker import (
    CaseInsensitiveNormalizer,
    SortedAnagramValidator,
    AnagramChecker,
    create_anagram_checker
)
from src.config import settings


@allure.feature('Anagram Checker')
@allure.story('String Normalization')
@pytest.mark.unit
class TestCaseInsensitiveNormalizer:
    """Test cases for CaseInsensitiveNormalizer"""

    def setup_method(self):
        """Setup test fixtures"""
        self.normalizer = CaseInsensitiveNormalizer()

    @allure.title("Test lowercase conversion")
    def test_normalize_lowercase(self):
        """Test that uppercase letters are converted to lowercase"""
        assert self.normalizer.normalize("HELLO") == "hello"

    @allure.title("Test space removal")
    def test_normalize_removes_spaces(self):
        """Test that spaces are removed"""
        assert self.normalizer.normalize("hello world") == "helloworld"

    @allure.title("Test combined normalization")
    def test_normalize_combined(self):
        """Test combined case and space normalization"""
        assert self.normalizer.normalize("A Gentleman") == "agentleman"

    @allure.title("Test empty string")
    def test_normalize_empty_string(self):
        """Test normalization of empty string"""
        assert self.normalizer.normalize("") == ""


@allure.feature('Anagram Checker')
@allure.story('Anagram Validation')
@pytest.mark.unit
class TestSortedAnagramValidator:
    """Test cases for SortedAnagramValidator"""

    def setup_method(self):
        """Setup test fixtures"""
        normalizer = CaseInsensitiveNormalizer()
        self.validator = SortedAnagramValidator(normalizer)

    @allure.title("Test valid anagrams: listen and silent")
    def test_validate_anagrams(self):
        """Test that valid anagrams are detected"""
        assert self.validator.validate("listen", "silent") is True

    @allure.title("Test non-anagrams: hello and world")
    def test_validate_non_anagrams(self):
        """Test that non-anagrams are detected"""
        assert self.validator.validate("hello", "world") is False

    @allure.title("Test case insensitive validation")
    def test_validate_case_insensitive(self):
        """Test that validation is case insensitive"""
        assert self.validator.validate("Listen", "Silent") is True

    @allure.title("Test validation with spaces")
    def test_validate_with_spaces(self):
        """Test that spaces are ignored"""
        assert self.validator.validate("A gentleman", "Elegant Man") is True

    @allure.title("Test empty strings")
    def test_validate_empty_strings(self):
        """Test validation of empty strings"""
        assert self.validator.validate("", "") is True


@allure.feature('Anagram Checker')
@allure.story('Main Checker Class')
@pytest.mark.unit
class TestAnagramChecker:
    """Test cases for AnagramChecker"""

    def setup_method(self):
        """Setup test fixtures"""
        self.checker = create_anagram_checker()

    @allure.title("Test check method with valid anagrams")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("listen", "silent", True),
        ("A gentleman", "Elegant Man", True),
        ("school master", "the classroom", True),
        ("conversation", "voices rant on", True),
        ("eleven plus two", "twelve plus one", True),
        ("apple", "paple", True),
    ])
    def test_check_valid_anagrams(self, input1, input2, expected):
        """Test various valid anagram pairs"""
        with allure.step(f"Checking if '{input1}' and '{input2}' are anagrams"):
            result = self.checker.check(input1, input2)
            assert result == expected

    @allure.title("Test check method with non-anagrams")
    @pytest.mark.parametrize("input1,input2,expected", [
        ("hello", "world", False),
        ("rat", "car", False),
    ])
    def test_check_non_anagrams(self, input1, input2, expected):
        """Test various non-anagram pairs"""
        with allure.step(f"Checking if '{input1}' and '{input2}' are anagrams"):
            result = self.checker.check(input1, input2)
            assert result == expected

    @allure.title("Test invalid input type")
    def test_check_invalid_input(self):
        """Test that invalid input raises ValueError"""
        with pytest.raises(ValueError, match="Both inputs must be strings"):
            self.checker.check(123, "test")

    @allure.title("Test factory function")
    def test_create_anagram_checker(self):
        """Test factory function creates valid instance"""
        checker = create_anagram_checker()
        assert isinstance(checker, AnagramChecker)
        assert checker.check("listen", "silent") is True


@allure.feature('Configuration')
@allure.story('Input length limits')
@pytest.mark.unit
class TestConfigValidationBounds:
    """Verify validation bounds are set as expected"""

    def test_min_length_config(self):
        """Minimum input length should be at least 2 characters"""
        assert settings.min_input_length == 2

    def test_max_length_config(self):
        """Maximum input length should be capped to prevent huge payloads"""
        assert settings.max_input_length == 1000
