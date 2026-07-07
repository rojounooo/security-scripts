# File Hash Tool

Generates and verifies SHA-256 hashes for files, storing them in a JSON baseline file (`hashes.json`). Useful for detecting whether a file has changed, and can be automated with cron.

## Flags

| Flag | Long name | What it does |
|---|---|---|
| `-c` | `--create` | Hash a file and store it as a new baseline entry |
| `-u` | `--update` | Rehash a file and overwrite its existing baseline entry |
| `-ch` | `--check-hash` | Rehash a file now and compare it against the stored baseline |
| `-l` | `--list` | Path to a text file containing a list of file paths, one per line |

`-c`, `-u`, and `-ch` are mutually exclusive, only one mode can be chosen per run.

Adding a long name (e.g. `--create` alongside `-c`) means `args.create` can be used in code later, which is more readable than referring back to `args.c`.

## Single file vs list mode

Each mode flag can be used two ways:

- **With a file path**, e.g. `-c test1.txt` — runs against that one file
- **With `--list` and no path**, e.g. `-c --list files.txt` — runs against every valid file in the list

To allow the second case, `-c`/`-u`/`-ch` use `nargs="?"` with `const=True`. This makes the file path optional: if no path follows the flag, `args.create` becomes `True` instead of a string.

`using_list_only = target is True` checks for this exact case. Since `target` can now be either a real path (a string) or `True` (flag used with no path), the script needs to know which one it's dealing with before trying to validate it as a file. `is True` matches only the literal boolean, so a filename string is never mistaken for it. This flag is then used to skip single-file validation when running in list-only mode, since there's no single path to check, the file-by-file validation instead happens later when the list file is read.

## Handlers

Each mode has its own handler function (`handle_create`, `handle_update`, `handle_check`), mapped through a dispatch dictionary (`handlers = {"create": handle_create, ...}`) rather than a chain of if/elif statements. This means the same handler function can be called once for a single target, or repeatedly in a loop for list mode, without the mode logic needing to know or care how many files it's being run against.

- **`handle_create`** — checks if the file already has a stored entry. If it does, the create is skipped (use `--update` instead) to avoid silently overwriting a baseline.
- **`handle_update`** — checks if the file has an existing entry. If it doesn't, the update is skipped (use `--create` first), since there's nothing to update.
- **`handle_check`** — checks if the file has an existing entry to compare against. If it does, the file is rehashed right now and compared to the stored hash, reporting a match or mismatch.

`handle_create` and `handle_update` both end up doing the same work (hash the file, build an entry, write it to JSON), just with opposite existence checks beforehand. That shared work lives in one helper, `_write_entry()`, so the hashing and writing logic only exists in one place.

## Why SHA-256 instead of SHA-1

SHA-1 is broken for collision resistance, meaning it's possible to deliberately craft two different files that produce the same hash. For pure accidental-change detection this weakness barely matters, but SHA-256 has no such practical collision weakness and is the current standard for file integrity hashing, so it was used here instead to avoid the need to justify SHA-1 as a deliberate exception.

## Running it

```
# Create a baseline hash for a single file
python file_hash_tool.py -c important_file.txt

# Update an existing baseline
python file_hash_tool.py -u important_file.txt

# Check a file against its stored baseline
python file_hash_tool.py -ch important_file.txt

# Run any mode against a list of files instead of a single file
python file_hash_tool.py -c --list files.txt
```

`files.txt` should contain one file path per line. Any paths that don't exist are skipped and reported at the end of the run rather than stopping the whole batch.

**Note:** Files are hashed in 64KB chunks rather than read into memory all at once, so large files don't get fully loaded into RAM.