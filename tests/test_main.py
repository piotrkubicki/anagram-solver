import pytest

from unittest.mock import patch
from main import (
    is_valid_word,
    get_valid_words,
    is_character_count_fine,
    find_combination,
    find_words_lengths,
    find_secret,
)


@pytest.mark.parametrize("valid_chars,min_word_len,word,expected", [
    (["b", "i", "e", "g", "k"], 2, "bike", True),
    (["s", "a", "e", "c"], 2, "space", False),
    (["s", "q", "u", "a", "r", "e"], 2, "square", True),
    (["a", "b", "c"], 2, "good", False),
    (["s", "q", "u", "a", "r", "e"], 9, "square", False),
])
def test_is_valid_word(valid_chars, min_word_len, word, expected):
    assert is_valid_word(valid_chars, min_word_len, word) == expected


@patch("main.read_words", return_value=["test", "bit", "space", "bike", "motorbike"])
def test_get_valid_words(mock_read_words):
    valid_chars = ["b", "r", "o", "t", "k", "i", "e", "s", "a", "p"]
    assert sorted(get_valid_words(valid_chars, 2, "test_path")) == sorted(["bit", "bike"])


@pytest.mark.parametrize("tested,searched,expected", [
    ("trust", "strut", True),
    ("bike", "motorbike", True),
    ("carr", "care", False),
])
def test_is_character_count_fine(tested, searched, expected):
    assert is_character_count_fine(tested, searched) == expected


@pytest.mark.parametrize("words,word_count,expected", [
   (["s", "m", "l", "xl", "xxl"], [1, 2, 3], [("s", "xl", "xxl"), ("m", "xl", "xxl"), ("l", "xl", "xxl")]),
   (["s", "m", "l", "xl", "xxl"], [1, 2, 1], [
            ("s", "xl", "s"), ("s", "xl", "m"), ("s", "xl", "l"),
            ("m", "xl", "s"), ("m", "xl", "m"), ("m", "xl", "l"),
            ("l", "xl", "s"), ("l", "xl", "m"), ("l", "xl", "l"),            
       ]
    ),
   (["s", "m", "xl", "xxl"], [1, 3], [("s", "xxl"), ("m", "xxl")]),
])
def test_find_combination(words, word_count, expected):
    assert set(find_combination(words, word_count)) == set(expected)


@pytest.mark.parametrize("num_words,min_chars,max_chars,limit,expected", [
    (2, 2, 6, 6, [(3, 3)]),
    (3, 2, 10, 10, [(2, 4, 4), (3, 3, 4), (2, 2, 6), (2, 3, 5)]),
    (2, 4, 20, 16, [(4, 12), (7, 9), (8, 8), (5, 11), (6, 10)]),
])
def test_find_words_lengths(num_words, min_chars, max_chars, limit, expected):
    assert set((find_words_lengths(num_words, min_chars, max_chars, limit))) == set(expected)


@patch.dict("main.hashed_secrets", {"easy": "7b751119ca49d2970cba2de2c4e83822"})
def test_find_secret():
    dictionary = ["small", "big", "green", "blue", "cat", "dolphin", "zebra"]
    anagram = "great gin bec"
    results = {}
    find_secret(dictionary, (3, 5, 3), 3, 11, anagram, results, 1)
    assert results["easy"] == "big green cat"
