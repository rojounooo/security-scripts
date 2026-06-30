import getpass
import string
import re
import math
import hashlib
import requests


def get_password():
    """Prompt for a password without echoing it to the terminal."""
    return getpass.getpass("Enter your password: ")


def check_length(password):
    """Print whether the password meets a minimum length requirement."""
    if len(password) >= 8:
        print("Length of password is ok")
    else:
        print("Password is too short")


def check_character_classes(password):
    """Check which character classes are present and return the resulting pool size."""
    pool_size = 0

    has_upper = re.search(r"[A-Z]", password)
    has_lower = re.search(r"[a-z]", password)
    has_digit = re.search(r"\d", password)
    has_symbol = re.search(r"[!@#$%^&*()._+=\-]", password)

    if has_upper:
        print("Has uppercase letter")
        pool_size += 26
    else:
        print("Missing uppercase letter")

    if has_lower:
        print("Has lowercase letter")
        pool_size += 26
    else:
        print("Missing lowercase letter")

    if has_digit:
        print("Has digit")
        pool_size += 10
    else:
        print("Missing digit")

    if has_symbol:
        print("Has symbol")
        pool_size += 13  
    else:
        print("Missing symbol")

    return pool_size


def calculate_entropy(password, pool_size):
    """Calculate password entropy in bits. Returns 0 if pool_size is 0 (empty password)."""
    if pool_size == 0:
        return 0
    return len(password) * math.log2(pool_size)


def rate_entropy(entropy):
    """Map an entropy value (bits) to a human-readable strength rating."""
    if entropy < 28:
        return "Very weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Reasonable"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very strong"


def check_pwned(password):
    """Check the password against the HIBP pwned-passwords API using k-anonymity."""
    encoded_password = password.encode("utf-8")
    hash_object = hashlib.sha1(encoded_password)
    hash_digest = hash_object.hexdigest().upper()

    prefix, suffix = hash_digest[:5], hash_digest[5:]

    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")

    if response.status_code != 200:
        print("Error fetching data from server.")
        return

    hashes = (line.split(":") for line in response.text.splitlines())

    for h, count in hashes:
        if h == suffix:
            print(f"Password found in breaches {count} times")
            return

    print("Password not found in any known breaches")


def main():
    password = get_password()

    check_length(password)
    pool_size = check_character_classes(password)

    entropy = calculate_entropy(password, pool_size)
    rating = rate_entropy(entropy)
    print(f"Entropy: {entropy:.2f} bits ({rating})")

    check_pwned(password)


if __name__ == "__main__":
    main()