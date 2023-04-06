import time
import os
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# import secrets file


# Set the time interval for uploading files (in seconds)
time_interval = 3600  # upload a file every hour

# Set the path to the folder on your desktop
desktop_folder = '/Users/Nick/Desktop/DJstuff'

# Set the ID of the folder in your Google Drive account to upload files to
folder_id = 'your_folder_id'

# Set the MIME type of the file to upload
mime_type = 'application/pdf'  # replace with the desired MIME type

# Set the Google Drive API version and credentials
api_version = 'v3'
creds = Credentials.from_authorized_user_file('path/to/your/credentials.json')


def upload_file_to_drive(file_path, folder_id, mime_type):
    """
    Uploads a file to a folder in Google Drive using the Google Drive API.
    """
    service = build('drive', api_version, credentials=creds)

    file_metadata = {'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype=mime_type)

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

