import argparse
from pathlib import Path

# Create Parser
parser = argparse.ArgumentParser()

# Create filename group
file_name_group = parser.add_mutually_exclusive_group(required=True)

# Create flag for new hashes
file_name_group.add_argument(
    "-c",
    "--create",
    type=str,
    metavar="FILE",
    help="Path to file you want a hash of"
)

# Note: Adding a long name e.g. --create means args.create can be used later for readability

# Update flag to rehash a file
file_name_group.add_argument(
    "-u",
    "--update",
    type=str,
    metavar="FILE",
    help="Path to file you want to rehash"
)

# Compare hash flag to rehash and compare to stored hash
file_name_group.add_argument(
    "-ch",
    "--check-hash",
    type=str,
    metavar="FILE",
    help="Path to file you want to compare the hash of"
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

# Validate target file
if not check_file_exists(target):
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