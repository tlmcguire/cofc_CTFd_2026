import sys

KEY = "cyberclub"
TARGET = [26, 74, 25, 13, 12, 33, 228, 15, 232, 237, 250, 231, 230, 233, 241, 254, 250, 253, 5, 11, 199, 199]


def transform(text):
    encoded = []
    for i, c in enumerate(text):
        shifted = (ord(c) + i * 3) % 256
        encoded.append(shifted ^ ord(KEY[i % len(KEY)]))
    return encoded


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 keygen.py <password>")
        sys.exit(1)

    password = sys.argv[1]

    if len(password) != len(TARGET):
        print("Access denied.")
        return

    if transform(password) == TARGET:
        print(f"Access granted! cofc{{{password}}}")
    else:
        print("Access denied.")


if __name__ == "__main__":
    main()
