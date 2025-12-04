Feature: Anagram Checker - Part 1
  As a user
  I want to check if two strings are anagrams
  So that I can verify their relationship

  Scenario Outline: Check if two strings are anagrams (Part 1)
    Given the input strings "<input1>" and "<input2>"
    When I check if they are anagrams
    Then the result should be "<output>"

    Examples: Basic Anagram Tests
      | input1           | input2          | output |
      | listen           | silent          | true   |
      | hello            | world           | false  |
      | conversation     | voices rant on  | true   |
      | school master    | the classroom   | true   |
      | a gentleman      | elegant man     | true   |
      | eleven plus two  | twelve plus one | true   |
      | apple            | paple           | true   |
      | rat              | car             | false  |

    Examples: Edge Cases - Short Strings
      | input1 | input2 | output |
      | aa     | aa     | true   |
      | ab     | ba     | true   |
      | Aa     | aA     | true   |
      | 11     | 11     | true   |
      | !!     | !!     | true   |
      | a      | a      | error  |
      | a      | b      | error  |
      | A      | a      | error  |
      | 1      | 1      | error  |
      | !      | !      | error  |

    Examples: Edge Cases - Empty and Whitespace
      | input1    | input2   | output |
      |           |          | error  |
      | abc       | abc      | true   |
      |   hello   | olleh    | true   |
      | a b c     | cba      | true   |

    Examples: Special Characters
      | input1      | input2      | output |
      | hello!      | !olleh      | true   |
      | test@123    | 123@test    | true   |
      | a-b-c       | c-b-a       | true   |
      | hello_world | world_hello | true   |
      | test#tag    | gat#test    | true   |
      | 100%        | %001        | true   |
