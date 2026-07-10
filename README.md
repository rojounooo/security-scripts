# security-scripts

A collection of defensive security tools written in Python. Each script targets a specific blue-team or hygiene-focused task: password strength, file integrity, OSINT lookups for compromised credentials, and SSH configuration security.

This repo is a working toolbox rather than a single project, scripts are added here as they're built and documented.

## Topics covered

- **Passwords** - strength checking and related hygiene tools
- **Hashing** - file hash generation and verification, useful for integrity checks and automation via cron
- **OSINT API integrations** - tools that query external threat intel and breach-data services (VirusTotal, Have I Been Pwned) without storing sensitive input locally

More categories will be added as the repo grows.

## Repo structure

Each script lives in its own folder containing:

- `script_name.py` - the script itself
- `explanation.md` - what it does, how to run it, and any design notes or lessons learned

```
security-scripts/
├── README.md
├── LICENSE
├── password-strength-checker/
│   ├── password_strength_checker.py
│   └── explanation.md
├── file-hash-tool/
│   ├── file_hash_tool.py
│   └── explanation.md
└── ...
```

## Disclaimer

These scripts are for educational and personal lab use. None of the tools in this repo store, log, or transmit credentials or sensitive data beyond what's required to make a given API call (e.g. password range lookups use k-anonymity, full passwords are never sent or saved).
