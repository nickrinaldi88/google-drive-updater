import time
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import platform

# import secrets file
with open('secrets.json', 'r') as f:
    secrets = json.load(f)

# Set the time interval for uploading files (in seconds)
time_interval = 3600  # upload a file every hour

# check os, based on result, select folder path
if platform.system() == 'Windows':
    desktop_folder = 'C:\\Users\\Nick\\Desktop\\Mixing_Music'
else:
    desktop_folder = '/Users/nickrinaldi/Desktop/Mixing-Music/'

# Set the ID of the folder in your Google Drive account to upload files to
folder_id = secrets['folder_id']

print(folder_id)

# Set the MIME type to for mp3
mime_type = 'audio/mpeg' 

# Set the Google Drive API version and credentials
api_version = 'v3'
creds = Credentials.from_service_account_file('credentials.json')
print("hi")

def build_drive_service(credentials_path, scopes):

    # check for token 

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes=scopes)

    # generate token if not exist
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
      
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # build drive service

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def count_items_in_folder(folder_id):

    """
    Returns count of items in a folder
    """

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name)"
    ).execute()

    items = results.get('files', [])
    return len(items)


def upload_file_to_drive(file_path, folder_id, mime_type):
    """
    Uploads a file to a folder in Google Drive using the Google Drive API.
    """

    # builds a file 
    service = build('drive', api_version, credentials=creds)
    

    file_metadata = {'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype=mime_type)
    print(dir(media))
    print(media.mimetype)

    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f'File ID: {file.get("id")} uploaded successfully.')
    except HttpError as error:
        print(f'An error occurred: {error}')
        file = None

    return file


while True:
    for file_name in os.listdir(desktop_folder):
        file_path = os.path.join(desktop_folder, file_name)
        if os.path.isfile(file_path):
            upload_file_to_drive(file_path, folder_id, mime_type)

    time.sleep(time_interval)


# TODO:
    # try a file id instead of a folder id - it may be looking for that
    # -confirm creds.json works

