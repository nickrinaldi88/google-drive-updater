import os.path
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build



# build drive service

def build_drive_service(credentials_path, refresh_token):
    creds = Credentials.from_authorized_user_file(credentials_path, refresh_token=refresh_token)
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def add_token_to_creds(refresh_token):

    with open('credentials.json', 'r') as creds_file:
        credentials = json.load(creds_file)

    credentials['installed']['refresh_token'] = refresh_token

    with open('credentials.json', 'w') as creds_file:
        json.dump(credentials, creds_file, indent=4)
# scope
scopes = ['https://www.googleapis.com/auth/drive']

# instansiate creds
if os.path.exists('credentials.json'):
    creds = Credentials.from_authorized_user_file('credentials.json')

# count items
def count_items_in_folder(folder_id):

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name)"
    ).execute()

    items = results.get('files', [])
    return len(items)


# execution
if __name__ == "__main__":

    # Load your secrets and credentials
    with open('secrets.json') as secrets_file:
        secrets = json.load(secrets_file)

    client_creds_path = 'credential.json'

    with open('refresh_token.txt', 'r') as f:
        token = f.read()

    add_token_to_creds(token)

    # build the drive service
    drive_service = build_drive_service(client_creds_path, token)

    # folder -id
    folder_id = secrets['folder_id']

    count_items_in_folder(folder_id)

