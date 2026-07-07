import argparse
from pathlib import Path
import hashlib
import json
import datetime

# Create Parser
parser = argparse.ArgumentParser()

# Create filename group
file_name_group = parser.add_mutually_exclusive_group(required=True)

# Create flag for new hashes
file_name_group.add_argument(
    "-c",
    "--create",
    type=str,
    nargs="?",
    const=True,
    metavar="FILE",
    help="Path to file you want a hash of. Omit the file when using --list."
)

# Update flag to rehash a file
file_name_group.add_argument(
    "-u",
    "--update",
    type=str,
    nargs="?",
    const=True,
    metavar="FILE",
    help="Path to file you want to rehash. Omit the file when using --list."
)

# Compare hash flag to rehash and compare to stored hash
file_name_group.add_argument(
    "-ch",
    "--check-hash",
    type=str,
    nargs="?",
    const=True,
    metavar="FILE",
    help="Path to file you want to compare the hash of. Omit the file when using --list."
)

# List flag for a file containing a list of filepaths
parser.add_argument(
    "-l",
    "--list",
    type=str,
    metavar="FILE",
    help="Path to file containing a list of file paths"
)

# Parse arguments
args = parser.parse_args()


# File validation function
def check_file_exists(path: str) -> bool:
    return Path(path).is_file()


# Pick mode
if args.create:
    mode = "create"
    target = args.create

elif args.update:
    mode = "update"
    target = args.update

elif args.check_hash:
    mode = "check"
    target = args.check_hash

# target is True (not a path) when the mode flag was used with no file, e.g. "-c --list files.txt"
using_list_only = target is True

if not args.list and using_list_only:
    parser.error("A file path is required unless --list is used")

# Validate target file, skipped when running in list-only mode
if not using_list_only and not check_file_exists(target):
    parser.error(f"{target} does not exist")

# Create valid and invalid file lists
valid_files = []
invalid_files = []

# Validate list file and process contents
if args.list:

    if not check_file_exists(args.list):
        parser.error(f"{args.list} does not exist")

    with open(args.list) as f:
        for line in f:

            line = line.strip()

            # Skip blank lines
            if not line:
                continue

            if check_file_exists(line):
                valid_files.append(line)
            else:
                invalid_files.append(line)


# Hash creation function
def create_hash(target):
    hash_obj = hashlib.sha256()
    buffer_size = 65536
    with open(target, "rb") as file:
        while True:
            content = file.read(buffer_size)
            if not content:
                break
            hash_obj.update(content)
    return hash_obj.hexdigest()


# JSON file to store hashes
hashfile = "hashes.json"

if check_file_exists(hashfile):
    pass
else:
    with open(hashfile, 'w') as f:
        json.dump({}, f)


# JSON write function
def write_to_json(entry, hashfile):
    with open(hashfile, "r+") as file:
        data = json.load(file)
        data.update(entry)
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)


# JSON read function, returns the stored entry for a file, or None if it has no entry yet
def get_existing_entry(hashfile, target):
    with open(hashfile, "r") as file:
        data = json.load(file)
    return data.get(target)


# Shared helper, hashes the target and writes a fresh entry with a current timestamp
def _write_entry(target):
    hash_value = create_hash(target)
    entry = {
        target: {
            "hash": hash_value,
            "algorithm": "sha256",
            "last_updated": datetime.datetime.now().strftime("%d/%m/%y %H:%M"),
        }
    }
    write_to_json(entry, hashfile)
    print(f"[CREATED] {target} -> {hash_value}")


# Create handler, refuses to run if an entry already exists
def handle_create(target):
    existing = get_existing_entry(hashfile, target)
    if existing:
        print(f"[SKIPPED] {target} already has a stored hash, use --update to rehash it")
        return
    _write_entry(target)


# Update handler, refuses to run if there is no existing entry to update
def handle_update(target):
    existing = get_existing_entry(hashfile, target)
    if not existing:
        print(f"[SKIPPED] {target} has no stored hash yet, use --create first")
        return
    _write_entry(target)


# Check handler, rehashes the file now and compares against the stored hash
def handle_check(target):
    existing = get_existing_entry(hashfile, target)
    if not existing:
        print(f"[SKIPPED] {target} has no stored hash to check against, use --create first")
        return

    current_hash = create_hash(target)
    stored_hash = existing["hash"]

    if current_hash == stored_hash:
        print(f"[MATCH] {target} is unchanged")
    else:
        print(f"[MISMATCH] {target} has changed since it was last hashed")


# Dispatch table, maps mode to its handler function
handlers = {
    "create": handle_create,
    "update": handle_update,
    "check": handle_check,
}

# Run the chosen handler against every valid file in the list, and/or the single target
if args.list:
    for file_path in valid_files:
        handlers[mode](file_path)

    if invalid_files:
        print("\nThe following files were skipped as they do not exist:")
        for file_path in invalid_files:
            print(f"  {file_path}")

if not using_list_only:
    handlers[mode](target)