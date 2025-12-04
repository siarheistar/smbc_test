Feature: Anagram Checker - Part 2
  As a user
  I want to check if two strings are anagrams
  So that I can verify their relationship

  Scenario Outline: Check if two strings are anagrams (Part 2)
    Given the input strings "<input1>" and "<input2>"
    When I check if they are anagrams
    Then the result should be "<output>"

    Examples: Unicode and International Characters
      | input1  | input2  | output |
      | café    | éfac    | true   |
      | naïve   | veïan   | true   |
      | hello   | hëllo   | false  |
      | mañana  | añanam  | true   |
      | Zürich  | hcirüZ  | true   |

    Examples: Numeric Strings
      | input1 | input2 | output |
      | 123    | 321    | true   |
      | abc123 | 321cba | true   |
      | 1000   | 0001   | true   |
      | 123    | 124    | false  |
      | 0      | 0      | error  |

    Examples: Case Sensitivity
      | input1 | input2 | output |
      | ABC    | abc    | true   |
      | AbC    | CbA    | true   |
      | LISTEN | silent | true   |
      | HeLLo  | oLLeH  | true   |

    Examples: Repeated Characters
      | input1 | input2 | output |
      | aaa    | aaa    | true   |
      | aaa    | aab    | false  |
      | aaabbb | bbbaaa | true   |
      | aaaa   | aaaaa  | false  |
      | abcabc | bcabca | true   |

    Examples: Long Strings
      | input1               | input2               | output |
      | abcdefghijklmnopqrst | tsrqponmlkjihgfedcba | true   |
      | The Quick Brown Fox  | xoF nworB kciuQ ehT  | true   |

    Examples: Tricky Cases
      | input1          | input2            | output |
      | Astronomer      | Moon starer       | true   |
      | The Morse Code  | Here come dots    | true   |
      | A decimal point | Im a dot in place | true   |
      | Dormitory       | Dirty room        | true   |
      | The eyes        | They see          | true   |
      | Funeral         | Real fun          | true   |
