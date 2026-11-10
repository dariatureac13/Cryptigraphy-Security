import random
import string

PC1 = [
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4,
]

def group(bits, n):
    return " ".join(bits[i:i + n] for i in range(0, len(bits), n))

def get_key():
    choice = input("Enter the 8-character key (Enter = random): ")
    if choice == "":
        alphabet = string.ascii_letters + string.digits
        choice = "".join(random.choice(alphabet) for _ in range(8))
        print(f"Random key generated: {choice}")
    while len(choice) != 8 or any(ord(c) > 127 for c in choice):
        choice = input("Key must be exactly 8 ASCII characters: ")
    return choice

def main():
    key = get_key()
    key_bits = ""
    for ch in key:
        b = format(ord(ch), "08b")
        key_bits += b
        print(ch, ord(ch), f"{ord(ch):02X}", b)
    print("K =", group(key_bits, 8))
    for r in range(8):
        print(" ".join(f"{r*8+c+1:>2}" for c in range(8)), "|",
              " ".join(key_bits[r*8+c] for c in range(8)))
    for r in range(8):
        print(" ".join(f"{x:>2}" for x in PC1[r*7:(r+1)*7]))
    kplus = ""
    for i, p in enumerate(PC1, start=1):
        bit = key_bits[p - 1]
        kplus += bit
        print(f"K+[{i:>2}] = K[{p:>2}] = {bit}")
    print("K+ =", group(kplus, 7))
    print("K+ hex =", f"{int(kplus, 2):014X}")
    print("C0 =", group(kplus[:28], 4))
    print("D0 =", group(kplus[28:], 4))

if __name__ == "__main__":
    main()
