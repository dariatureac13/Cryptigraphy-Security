"""Interactive console program: Caesar cipher with one key (Task 1.1)
and with two keys / permuted alphabet (Task 1.2) for the Romanian alphabet."""

import caesar as cz


def ask(prompt, validator):
    """Ask again until the validator accepts the value."""
    while True:
        try:
            return validator(input(prompt))
        except cz.InvalidInput as err:
            print(f"  [!] {err}\n")


def choose_operation(value):
    value = value.strip().upper()
    if value not in ("E", "D"):
        raise cz.InvalidInput("Choose E (encrypt) or D (decrypt).")
    return value


def run_operation(alphabet, two_keys):
    op = ask("Operation - (E)ncrypt or (D)ecrypt: ", choose_operation)
    k = ask(f"Key 1 (shift, 1-{cz.N - 1}): ", cz.validate_shift)
    if two_keys:
        word = ask(f"Key 2 (keyword, min {cz.MIN_KEYWORD_LEN} letters): ",
                   cz.validate_keyword)
        alphabet = cz.permuted_alphabet(word)
        print("Permuted alphabet:", " ".join(alphabet))
    label = "message" if op == "E" else "ciphertext"
    text = ask(f"Enter the {label}: ", cz.clean_text)
    print("Processed input :", text)
    if op == "E":
        print("Ciphertext      :", cz.encrypt(text, k, alphabet))
    else:
        print("Decrypted text  :", cz.decrypt(text, k, alphabet))


def main():
    while True:
        print("\n=== Caesar cipher - Romanian alphabet (n = 31) ===")
        print("1. Caesar cipher (one key)")
        print("2. Caesar cipher with a permutation (two keys)")
        print("0. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            run_operation(cz.ALPHABET, two_keys=False)
        elif choice == "2":
            run_operation(cz.ALPHABET, two_keys=True)
        elif choice == "0":
            break
        else:
            print("  [!] Choose 1, 2 or 0.")


if __name__ == "__main__":
    main()
