# Password Checker

Checks password strength using length, character variety, entropy, and a breach check against Have I Been Pwned (HIBP). The password is never stored, logged, or written to disk at any point.

## What it checks

| Check | What it does |
|---|---|
| Length | Flags if password is under 8 characters |
| Character classes | Checks for uppercase, lowercase, digits, symbols |
| Entropy | Estimates brute-force difficulty in bits, based on length and character pool size |
| Pwned check | Checks the password against known breaches via the HIBP API |

## How it works

1. Password is entered via `getpass`, so it's not echoed to the terminal or saved in shell history.
2. Character classes are detected using regex. Each class found (upper, lower, digit, symbol) adds its size to the total character pool.
3. Entropy is calculated as `length x log2(pool size)`, then mapped to a rating from Very weak to Very strong.
4. The password is SHA-1 hashed locally, then only the first 5 characters of the hash are sent to the HIBP API (k-anonymity). The full password and full hash never leave the machine. HIBP returns a list of matching hash suffixes, which is checked locally against the rest of the hash.

## Running it

```
python password_checker.py
```

You'll be prompted to enter a password, then a report prints to the terminal.

## Requirements

```
pip install requests
```

**Note:** Entropy is a limited measure. `Tr0ub4dor&3` scores as "Strong" under this formula despite being a well-known weak pattern (dictionary word with leetspeak substitutions), because entropy only measures length and character variety, not predictability. The HIBP check catches passwords that have already leaked, but pattern-based weaknesses like this aren't caught by either check in this version. A pattern detection feature (keyboard walks, repeated characters, common substitutions) is planned as a future addition.

**Note:** SHA-1 is used here only to interact with the HIBP API, which requires it. It has nothing to do with how securely the password itself is handled.
