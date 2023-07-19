import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load your secrets from the secrets.json file
with open('secrets.json', 'r') as f:
    secrets = json.load(f)

# Set the Google Drive API version and credentials
api_version = 'v3'
creds = Credentials.from_service_account_file('credentials.json')

def test_google_credentials(creds):
    """
    Tests if the provided Google credentials work by making a request to the Google Drive API.
    """
    try:
        service = build('drive', api_version, credentials=creds)
        files = service.files().list().execute()
        if 'files' in files:
            print("Credentials are working. You have access to your Google Drive files.")
        else:
            print("Credentials are not working. Please check your credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Perform the test with the provided credentials
test_google_credentials(creds)
