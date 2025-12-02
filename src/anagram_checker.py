"""
Anagram Checker - Core Logic
Implements SOLID principles with OOP design
"""
from abc import ABC, abstractmethod
from typing import Protocol


class StringNormalizer(Protocol):
    """Interface for string normalization (Interface Segregation Principle)"""
    def normalize(self, text: str) -> str:
        """Normalize a string for comparison"""
        ...


class CaseInsensitiveNormalizer:
    """Concrete implementation of StringNormalizer (Single Responsibility Principle)"""

    def normalize(self, text: str) -> str:
        """
        Normalize string by converting to lowercase and removing spaces

        Args:
            text: Input string to normalize

        Returns:
            Normalized string
        """
        return ''.join(text.lower().split())


class AnagramValidator(ABC):
    """Abstract base class for anagram validation (Open/Closed Principle)"""

    @abstractmethod
    def validate(self, str1: str, str2: str) -> bool:
        """Validate if two strings are anagrams"""
        pass


class SortedAnagramValidator(AnagramValidator):
    """
    Validates anagrams by sorting characters
    (Single Responsibility Principle)
    """

    def __init__(self, normalizer: StringNormalizer):
        """
        Initialize validator with a normalizer
        (Dependency Inversion Principle - depends on abstraction)
        """
        self._normalizer = normalizer

    def validate(self, str1: str, str2: str) -> bool:
        """
        Check if two strings are anagrams by sorting their characters

        Args:
            str1: First string
            str2: Second string

        Returns:
            True if strings are anagrams, False otherwise
        """
        normalized1 = self._normalizer.normalize(str1)
        normalized2 = self._normalizer.normalize(str2)

        return sorted(normalized1) == sorted(normalized2)


class AnagramChecker:
    """
    Main class for checking anagrams
    (Single Responsibility Principle - orchestrates the checking process)
    """

    def __init__(self, validator: AnagramValidator):
        """
        Initialize checker with a validator
        (Dependency Inversion Principle)

        Args:
            validator: AnagramValidator implementation
        """
        self._validator = validator

    def check(self, input1: str, input2: str) -> bool:
        """
        Check if two inputs are anagrams

        Args:
            input1: First string
            input2: Second string

        Returns:
            True if anagrams, False otherwise
        """
        if not isinstance(input1, str) or not isinstance(input2, str):
            raise ValueError("Both inputs must be strings")

        return self._validator.validate(input1, input2)


def create_anagram_checker() -> AnagramChecker:
    """
    Factory function to create AnagramChecker instance
    (Dependency Injection)

    Returns:
        Configured AnagramChecker instance
    """
    normalizer = CaseInsensitiveNormalizer()
    validator = SortedAnagramValidator(normalizer)
    return AnagramChecker(validator)
