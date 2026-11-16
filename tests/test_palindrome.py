import pytest

from app.palindrome import PalindromeInputError, check_palindrome


@pytest.mark.parametrize(
    "text, expected",
    [
        ("А роза упала на лапу Азора", True),
        ("Шалаш", True),
        ("Madam, I'm Adam", True),
        ("12321", True),
        ("Аргентина манит негра", True),
        ("Ёж ежё", True),
        ("а", True),
        ("Привет", False),
        ("Сервер", False),
        ("12345", False),
    ],
)
def test_palindrome(text, expected):
    assert check_palindrome(text).is_palindrome is expected


def test_normalized_and_message():
    r = check_palindrome("А роза упала на лапу Азора")
    assert r.normalized == "арозаупаланалапуазора"
    assert r.message == "является палиндромом"
    assert check_palindrome("Привет").message == "не является палиндромом"


@pytest.mark.parametrize("text", ["", "   ", "!!! ,,, ---", "x" * 1001])
def test_bad_input(text):
    with pytest.raises(PalindromeInputError):
        check_palindrome(text)


def test_max_length_allowed():
    assert check_palindrome("a" * 1000).is_palindrome
