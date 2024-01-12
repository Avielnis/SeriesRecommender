import time

import pytest
from word_tools import count_anagrams


def test_empty_text():
    assert count_anagrams("", "abc") == 0


@pytest.mark.parametrize("text, word, expected", [
    ("kjgwhefjkw", "", 0),
    ("forxxorfxdofr", "for", 3),
    ("hello world", "who", 0),
    ("aBcDeF", "fed", 0),
    ("ababab", "ab", 5),
    ("this is a longer piece of text to test the function", "test", 1),
    ("this is a longer piece of text to test the function", " ", 10),
    ("this is a longer piece of text to test the function", " t", 6),
    ("repeated repeated repeated", "te", 3),
    ("x", "x", 1),
    ("abcabcabc", "cba", 7),
    ("normaltext", "xyz", 0),
    ("abcdbacbacbacdbcdabcdbacbacbacdbcdabcdbacbacbacdbcd", "abcd", 21)
])
def test_count_anagrams(text, word, expected):
    assert count_anagrams(text, word) == expected


def test_count_anagrams_performance():
    text = "abcdbacbacbacdbcdabcdbacbacbacdbcdabcdbacbacbacdbcd"
    word = "abcd"
    start = time.time()
    for _ in range(1000):
        count_anagrams(text, word)
    end = time.time()
    time_took_ms = (end - start) * 1000
    assert time_took_ms < 50, "to slow"

