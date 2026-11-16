

from dataclasses import dataclass

MAX_LENGTH = 1000

MESSAGE_YES = "является палиндромом"
MESSAGE_NO = "не является палиндромом"


class PalindromeInputError(ValueError):
    """Строка не подходит для проверки (пустая, слишком длинная, без букв и цифр)."""


@dataclass(frozen=True)
class PalindromeResult:
    text: str
    normalized: str
    is_palindrome: bool
    message: str


def normalize(text: str) -> str:
    """Оставляет только буквы и цифры в нижнем регистре, «ё» заменяет на «е»."""
    lowered = text.lower().replace("ё", "е")
    return "".join(ch for ch in lowered if ch.isalnum())


def is_palindrome(chars: str) -> bool:
    """Сравнивает символы попарно с двух концов строки."""
    left, right = 0, len(chars) - 1
    while left < right:
        if chars[left] != chars[right]:
            return False
        left += 1
        right -= 1
    return True


def check_palindrome(text: str) -> PalindromeResult:
    if len(text) > MAX_LENGTH:
        raise PalindromeInputError(f"Строка длиннее {MAX_LENGTH} символов")
    if not text.strip():
        raise PalindromeInputError("Строка пустая")

    normalized = normalize(text)
    if not normalized:
        raise PalindromeInputError("В строке нет ни одной буквы или цифры")

    result = is_palindrome(normalized)
    return PalindromeResult(
        text=text,
        normalized=normalized,
        is_palindrome=result,
        message=MESSAGE_YES if result else MESSAGE_NO,
    )
