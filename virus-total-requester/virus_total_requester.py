from pathlib import Path
import requests
import hashlib
import os

# Function to get file path
def get_path() -> str:
    filepath = input("File path: ")

    return filepath

# File validation function
def check_file_exists(path: str) -> bool:
    return Path(path).is_file()

# Hash creation function
def create_hash(target) -> str:
    hash_obj = hashlib.sha256()
    buffer_size = 65536
    with open(target, "rb") as file:
        while True:
            content = file.read(buffer_size)
            if not content:
                break
            hash_obj.update(content)
    return hash_obj.hexdigest()

# Function to get API key
def get_api_key():
    api_key = os.environ.get("API")

    return api_key

# Function to query api
def check_hash(file_hash, api_key):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": api_key}
    response = requests.get(url, headers=headers)

    return response


# Function to process response
def process_response(response):
    if response.status_code == 200:
        data = response.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]

        malicious = stats["malicious"]
        suspicious = stats["suspicious"]
        harmless = stats["harmless"]
        undetected = stats["undetected"]

        print("Hash found on VirusTotal")
        print(f"Malicious: {malicious}")
        print(f"Suspicious: {suspicious}")
        print(f"Harmless: {harmless}")
        print(f"Undetected: {undetected}")

    elif response.status_code == 404:
        print("Hash not found on VirusTotal, this file has not been seen before.")

    elif response.status_code == 401:
        print("API key rejected, check that it's valid.")

    elif response.status_code == 429:
        print("Rate limited by VirusTotal, wait before trying again.")

    else:
        print(f"Unexpected error: {response.status_code}")


def main():
    api_key = get_api_key()

    if not api_key:
        print("Error: API environment variable not set.")
        return

    filepath = get_path()

    if not check_file_exists(filepath):
        print(f"Error: {filepath} does not exist.")
        return

    file_hash = create_hash(filepath)
    response = check_hash(file_hash, api_key)
    process_response(response)


if __name__ == "__main__":
    main()