
"""
Laboratory work no. 3, Task 3.1 - Playfair cipher for the Romanian alphabet
(31 letters).

The 31-letter Romanian alphabet is placed in a 6x6 matrix (36 cells);
the 5 remaining cells are filled with the service symbols 0-4, which can
never occur in the text.
"""
import re

ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"   # 31 letters
FILLERS = "01234"                               # 36 - 31 = 5 free cells
SIZE = 6
MIN_KEY_LEN = 7
PAD = "X"          # inserted between double letters / at the end
PAD_ALT = "Q"      # used when the double letter itself is X

VALID_RE = re.compile(r"^[A-Za-z]+$")
HINT = "Allowed characters: Latin letters 'A'-'Z' and 'a'-'z' only."


# input
def clean_input(text, what):
    """Remove spaces, validate characters, convert to upper case."""
    text = text.replace(" ", "")
    if not text:
        raise ValueError(f"The {what} is empty.")
    if not VALID_RE.match(text):
        bad = sorted({c for c in text if not re.match(r"[A-Za-z]", c)})
        raise ValueError(f"Invalid character(s) in the {what}: {bad}. {HINT}")
    return text.upper()


def validate_key(key):
    if len(key.replace(" ", "")) < MIN_KEY_LEN:
        raise ValueError(f"The key must contain at least {MIN_KEY_LEN} letters.")
    return clean_input(key, "key")


#matrix
def build_matrix(key):
    """Key letters (without repeats) + rest of alphabet + filler symbols."""
    seen, cells = set(), []
    for ch in key + ALPHABET + FILLERS:
        if ch not in seen:
            seen.add(ch)
            cells.append(ch)
    return [cells[i * SIZE:(i + 1) * SIZE] for i in range(SIZE)]


def positions(matrix):
    return {ch: (r, c) for r, row in enumerate(matrix) for c, ch in enumerate(row)}


def print_matrix(matrix):
    for row in matrix:
        print("  " + " ".join(row))


#text preparing
def prepare(text):
    """Split into digraphs; insert PAD between equal letters; pad odd end."""
    pairs, i = [], 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:                       # double letter -> insert filler
                pairs.append(a + (PAD if a != PAD else PAD_ALT))
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:                                # odd number of letters
            pairs.append(a + (PAD if a != PAD else PAD_ALT))
            i += 1
    return pairs


#cipher
def _transform(pair, matrix, pos, shift):
    """shift = +1 for encryption, -1 for decryption."""
    (r1, c1), (r2, c2) = pos[pair[0]], pos[pair[1]]
    if r1 == r2:                                         # same row
        return matrix[r1][(c1 + shift) % SIZE] + matrix[r2][(c2 + shift) % SIZE]
    if c1 == c2:                                         # same column
        return matrix[(r1 + shift) % SIZE][c1] + matrix[(r2 + shift) % SIZE][c2]
    return matrix[r1][c2] + matrix[r2][c1]               # rectangle


def encrypt(message, key):
    key = validate_key(key)
    msg = clean_input(message, "message")
    matrix = build_matrix(key)
    pos = positions(matrix)
    return "".join(_transform(p, matrix, pos, +1) for p in prepare(msg))


def decrypt(cryptogram, key):
    key = validate_key(key)
    # The cryptogram may contain any symbol of the 6x6 matrix (31 Romanian
    # letters + 5 service symbols), because plaintext letters can be
    # replaced by diacritic letters.
    ct = cryptogram.replace(" ", "").upper()
    if not ct:
        raise ValueError("The cryptogram is empty.")
    allowed = set(ALPHABET + FILLERS)
    bad = sorted({c for c in ct if c not in allowed})
    if bad:
        raise ValueError(f"Invalid character(s) in the cryptogram: {bad}. "
                         "Allowed: letters of the Romanian alphabet (A-Z, Ă, Â, Î, Ș, Ț) "
                         "and the service symbols 0-4.")
    if len(ct) % 2:
        raise ValueError("The cryptogram must have an even number of letters.")
    matrix = build_matrix(key)
    pos = positions(matrix)
    pairs = [ct[i:i + 2] for i in range(0, len(ct), 2)]
    if any(p[0] == p[1] for p in pairs):
        raise ValueError("A Playfair cryptogram cannot contain a pair of equal letters.")
    return "".join(_transform(p, matrix, pos, -1) for p in pairs)


#UI
def main():
    print("Playfair cipher (Romanian alphabet, 31 letters)")
    while True:
        op = input("\nChoose operation: [E]ncrypt / [D]ecrypt / [Q]uit: ").strip().lower()
        if op in ("q", "quit"):
            break
        if op not in ("e", "d"):
            print("Please type E, D or Q.")
            continue
        try:
            key = validate_key(input(f"Key (min {MIN_KEY_LEN} letters): "))
            print("Encryption matrix:")
            print_matrix(build_matrix(key))
            if op == "e":
                text = input("Message: ")
                print("Cryptogram:", encrypt(text, key))
            else:
                text = input("Cryptogram: ")
                print("Decrypted message (add spaces manually):", decrypt(text, key))
        except ValueError as err:
            print("Error:", err)


if __name__ == "__main__":
    main()