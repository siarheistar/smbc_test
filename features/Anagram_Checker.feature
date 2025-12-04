Feature: Anagram Checker
  As a user
  I want to check if two strings are anagrams
  So that I can verify their relationship

  Scenario Outline: Check if two strings are anagrams
    Given the input strings "<input1>" and "<input2>"
    When I check if they are anagrams
    Then the result should be "<output>"

    Examples: Basic Anagram Tests
      | input1            | input2          | output |
      | listen            | silent          | true   |
      | hello             | world           | false  |
      | conversation      | voices rant on  | true   |
      | school master     | the classroom   | true   |
      | a gentleman       | elegant man     | true   |
      | eleven plus two   | twelve plus one | true   |
      | apple             | paple           | true   |
      | rat               | car             | false  |



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
      | input1       | input2       | output |
      | hello!       | !olleh       | true   |
      | test@123     | 123@test     | true   |
      | a-b-c        | c-b-a        | true   |
      | hello_world  | world_hello  | true   |
      | test#tag     | gat#test     | true   |
      | 100%         | %001         | true   |

    Examples: Unicode and International Characters
      | input1  | input2  | output |
      | café    | éfac    | true   |
      | naïve   | veïan   | true   |
      | hello   | hëllo   | false  |
      | mañana  | añanam  | true   |
      | Zürich  | hcirüZ  | true   |

    Examples: Numeric Strings
      | input1    | input2    | output |
      | 123       | 321       | true   |
      | abc123    | 321cba    | true   |
      | 1000      | 0001      | true   |
      | 123       | 124       | false  |
      | 0         | 0         | error  |

    Examples: Case Sensitivity
      | input1  | input2  | output |
      | ABC     | abc     | true   |
      | AbC     | CbA     | true   |
      | LISTEN  | silent  | true   |
      | HeLLo   | oLLeH   | true   |

    Examples: Repeated Characters
      | input1     | input2     | output |
      | aaa        | aaa        | true   |
      | aaa        | aab        | false  |
      | aaabbb     | bbbaaa     | true   |
      | aaaa       | aaaaa      | false  |
      | abcabc     | bcabca     | true   |

    Examples: Long Strings
      | input1                | input2                | output |
      | abcdefghijklmnopqrst  | tsrqponmlkjihgfedcba  | true   |
      | The Quick Brown Fox   | xoF nworB kciuQ ehT   | true   |

    Examples: Tricky Cases
      | input1           | input2            | output |
      | Astronomer       | Moon starer       | true   |
      | The Morse Code   | Here come dots    | true   |
      | A decimal point  | Im a dot in place | true   |
      | Dormitory        | Dirty room        | true   |
      | The eyes         | They see          | true   |
      | Funeral          | Real fun          | true   |
