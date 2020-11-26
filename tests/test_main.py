import pytest

from unittest.mock import patch
from main import (
    is_valid_word,
    get_valid_words,
    find_combination,
)


@pytest.mark.parametrize("valid_chars,word,expected", [
    (["b", "i", "e", "g", "k"], "bike", True),
    (["s", "a", "e", "c"], "space", False),
    (["s", "q", "u", "a", "r", "e"], "square", True),
    (["a", "b", "c"], "good", False),
])
def test_is_valid_word(valid_chars, word, expected):
    assert is_valid_word(valid_chars, word) == expected


@patch("main.read_words", return_value=["test", "bit", "space", "bike", "motorbike"])
def test_get_valid_words(mock_read_words):
    valid_chars = ["b", "r", "o", "t", "k", "i", "e", "s", "a", "p"]
    assert sorted(get_valid_words(valid_chars, "test_path")) == sorted(["bit", "bike", "test"])


def test_find_combination():
    words = sorted(["small", "medium", "big"], key=len)
    expected = "sasdasda asda sd"
    assert " ".join(find_combination([],words, len(expected.replace(" ", "")), "smallbig")) == expected
