import requests 
import os

# Function to get users email
def get_email():
    email = input("Email: ")

    return email

# Function to get API key
def get_api_key():
    api_key = os.environ.get("API")

    return api_key

# Function to query api 
def check_email(email, api_key):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"hibp-api-key": api_key}
    response = requests.get(url, headers=headers)

    return response

# Function to process response
def process_response(response):
    if response.status_code == 200:
        breaches = response.json()
        print(f"Found {len(breaches)} breach(es):\n")
        for breach in breaches:
            name = breach["Name"]
            date = breach["BreachDate"]
            data_classes = ", ".join(breach["DataClasses"])
            print(f"- {name} ({date})")
            print(f"  Exposed data: {data_classes}\n")

    elif response.status_code == 404:
        print("No breaches found for this email.")

    elif response.status_code == 429:
        print("Rate limited by HIBP, wait before trying again.")

    elif response.status_code == 401:
        print("API key rejected, check that it's valid.")

    else:
        print(f"Unexpected error: {response.status_code}")

def main():
    api_key = get_api_key()
 
    if not api_key:
        print("Error: API environment variable not set.")
        return
 
    email = get_email()
    response = check_email(email, api_key)
    process_response(response)
 
 
if __name__ == "__main__":
    main()




