# HIBP Email Breach Checker

Checks whether an email address appears in any known data breaches, using the Have I Been Pwned (HIBP) breached account API. The email is never stored or logged.

## What it checks

Queries HIBP for the given email and, if breaches are found, reports the breach name, date, and what type of data was exposed (passwords, usernames, phone numbers, etc.) for each one.

## How it works

1. Email is entered via a plain `input()` prompt.
2. The email is sent directly to HIBP's breached account endpoint as part of the URL. No hashing is used here, unlike the password checker.
3. The response is checked by status code and handled accordingly.

## Why no hashing here

The password checker hashes the password locally and only sends a small piece of the hash to HIBP (k-anonymity), so the actual password never leaves the machine. This script doesn't do that for the email, because the HIBP breached account API works by looking up the email directly, it has no k-anonymity equivalent for this endpoint. This is a reasonable tradeoff since an email address is far less sensitive than a password: it's usually already public in some form (used to sign up for accounts, sent in plain text over email, etc.), so sending it directly to a trusted API isn't the same risk as sending a password in plain text would be.

## API key

This endpoint requires a paid HIBP API key (unlike the free k-anonymity password range API used in the password checker). The key is read from an environment variable, `API`, rather than being hardcoded or prompted for, so it never ends up committed to the repo.

Set it before running:

**Linux / macOS:**
```
export API=your_api_key_here
```

**Windows (PowerShell):**
```
$env:API = "your_api_key_here"
```

**Windows (Command Prompt):**
```
set API=your_api_key_here
```

If the environment variable isn't set, the script prints an error and exits without making a request.

**Note:** This script has not been tested against a live key, since a paid HIBP subscription wasn't used during development. All logic up to and including the request has been verified, but response handling should be double checked against a real response once a key is available.

## Status code handling

| Code | Meaning |
|---|---|
| 200 | Breaches found, details are printed |
| 404 | No breaches found (HIBP uses 404 for "clean", not an error) |
| 401 | API key missing or invalid |
| 429 | Rate limited by HIBP |
| other | Unexpected error, status code is printed |

## Running it

```
python email_breach_checker.py
```

## Requirements

```
pip install requests
```