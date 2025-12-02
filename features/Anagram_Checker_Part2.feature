Feature: Anagram Checker - Part 2
  As a user
  I want to check if two strings are anagrams
  So that I can verify their relationship

  Scenario Outline: Check if two strings are anagrams - Set 2
    Given the input strings "<input1>" and "<input2>"
    When I check if they are anagrams
    Then the result should be "<output>"

    Examples:
      | input1            | input2          | output |
      | a gentleman       | elegant man     | true   |
      | eleven plus two   | twelve plus one | true   |
      | apple             | paple           | true   |
      | rat               | car             | false  |
