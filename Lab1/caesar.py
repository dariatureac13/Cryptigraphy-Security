"Caesar cipher (one and two keys) for the Romanian alphabet."


# Table 2 of the lab: Romanian alphabet, n = 31
ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I", "Î",
            "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "Ș", "T",
            "Ț", "U", "V", "W", "X", "Y", "Z"]
N = len(ALPHABET)  # 31
MIN_KEYWORD_LEN = 7

# Cedilla variants (ş, ţ) are treated as the comma-below letters (ș, ț)
CEDILLA_FIX = {"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"}


class InvalidInput(ValueError):
    """Raised when a key or a text does not satisfy the lab requirements."""


# encoding
def build_codes(alphabet):
    """Letter -> numeric code (position in the alphabet, starting from 0)."""
    return {letter: i for i, letter in enumerate(alphabet)}


def normalize(text):
    """Fix cedilla variants, convert to uppercase (spaces are kept here)."""
    fixed = "".join(CEDILLA_FIX.get(ch, ch) for ch in text)
    return fixed.upper()


# validation
def validate_shift(value, n=N):
    """Key 1: integer from 1 to n-1 (1..30 for Romanian)."""
    try:
        k = int(str(value).strip())
    except ValueError:
        raise InvalidInput(
            f"Invalid key '{value}': the key must be an integer "
            f"between 1 and {n - 1} inclusive.")
    if not 1 <= k <= n - 1:
        raise InvalidInput(
            f"Invalid key {k}: the key must be between 1 and {n - 1} inclusive.")
    return k


def clean_text(text, alphabet=ALPHABET):
    """Uppercase the text and remove spaces; reject anything that is not a letter."""
    codes = build_codes(alphabet)
    result = []
    for ch in normalize(text):
        if ch == " ":
            continue
        if ch not in codes:
            raise InvalidInput(
                f"Invalid character '{ch}': only letters of the Romanian alphabet "
                f"(A-Z, Ă, Â, Î, Ș, Ț) and spaces are allowed.")
        result.append(ch)
    if not result:
        raise InvalidInput("The text is empty: enter at least one letter.")
    return "".join(result)


def validate_keyword(word, alphabet=ALPHABET, min_len=MIN_KEYWORD_LEN):
    """Key 2: only letters of the alphabet, at least min_len characters."""
    word = normalize(word.strip())
    codes = build_codes(alphabet)
    for ch in word:
        if ch not in codes:
            shown = "space" if ch == " " else f"'{ch}'"
            raise InvalidInput(
                f"Invalid character {shown} in the keyword: only letters of the "
                f"Romanian alphabet are allowed (no spaces, digits or symbols).")
    if len(word) < min_len:
        raise InvalidInput(
            f"Keyword too short ({len(word)} characters): it must contain "
            f"at least {min_len} letters.")
    return word


#permuted alphabet
def permuted_alphabet(keyword, alphabet=ALPHABET):
    """Distinct keyword letters first, then the remaining letters in natural order."""
    result = []
    for ch in list(keyword) + list(alphabet):
        if ch not in result:
            result.append(ch)
    return result


# encryption / decryption
def _shift(text, k, alphabet, sign):
    codes = build_codes(alphabet)
    n = len(alphabet)
    # (x +/- k) mod n; Python's % is already non-negative, "+ n" kept for clarity
    return "".join(alphabet[(codes[ch] + sign * k + n) % n] for ch in text)


def encrypt(text, k, alphabet=ALPHABET):
    """c = (x + k) mod n"""
    return _shift(text, k, alphabet, +1)


def decrypt(text, k, alphabet=ALPHABET):
    """m = (y - k) mod n"""
    return _shift(text, k, alphabet, -1)
