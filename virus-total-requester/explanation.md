# VirusTotal Hash Lookup Tool

Hashes a local file and checks that hash against VirusTotal's database, reporting how many antivirus engines flag it as malicious or suspicious. The file itself is never uploaded, only its SHA-256 hash is sent, so nothing sensitive leaves the machine.

## What it checks

Queries VirusTotal for the file's hash and, if it's a known hash, reports detection counts across four categories: malicious, suspicious, harmless, and undetected.

## How it works

1. File path is entered via `input()` and validated to make sure it exists.
2. The file is read in 64KB chunks and hashed with SHA-256, same approach as the file hash tool, so large files don't get fully loaded into memory.
3. The hash is sent to VirusTotal's `/files/{hash}` endpoint. No file content is uploaded, only the hash.
4. The response is checked by status code and handled accordingly.

## API key

This uses VirusTotal's free tier API, which is rate limited (around 4 requests per minute on the free tier). The key is read from an environment variable, `API`, rather than being hardcoded, so it never ends up committed to the repo.

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

## Status code handling

| Code | Meaning |
|---|---|
| 200 | Hash found, detection stats are printed |
| 404 | Hash not found, VirusTotal has no record of this file |
| 401 | API key missing or invalid |
| 429 | Rate limited by VirusTotal |
| other | Unexpected error, status code is printed |

**Note:** A 404 doesn't mean a file is safe, only that VirusTotal hasn't seen it before. A brand new or custom-built file will always return 404 regardless of whether it's malicious.

## Testing notes

Tested against two cases:

- **A freshly created text file with unique content** returned a 404, as expected, since VirusTotal had no prior record of it.
- **The EICAR test file** (a standard, harmless string used industry-wide to test antivirus detection) returned a 200 with non-zero malicious detections, confirming the response parsing works correctly against a real "known bad" hash. Windows Defender flagged and attempted to remove the EICAR file immediately on creation, which is expected AV behavior, real-time protection was temporarily disabled to allow the file to be written and hashed for this test, then re-enabled afterwards.

## Running it

```
python virus_total_requester.py
```

## Requirements

```
pip install requests
```

## Possible future additions

- CLI flags (argparse) to pass the file path directly instead of prompting, useful for scripting/automation
- Batch mode to check a list of files or hashes in one run, similar to the `--list` option in the file hash tool
- Caching recent lookups locally to avoid re-querying the same hash and burning through the free tier's rate limit
- Handling the case where the JSON response is missing expected fields (e.g. `last_analysis_stats`), rather than assuming it's always present on a 200 response