import os
import json
import time
from datetime import datetime, timedelta
# from google.oauth2.credentials import Credentials
import google.auth
from google.oauth2._credentials_async import Credentials
from googleapiclient.discovery import build, MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import mimetypes

# scope
scopes = ['https://www.googleapis.com/auth/drive']

folder_path = '/Users/nickrinaldi/Desktop/Dubstep-Test'

token_file = 'token.json'
# build drive service

def build_drive_service(credentials_path, scopes):

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # creds = service_account.Credentials.from_service_account_file('service_account_key.json', scopes=scopes)

    # creds, _ = google.auth.default()

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def remove_token(token_file):

    if os.path.exists(token_file):
        os.remove(token_file)
    else:
        print("token does not exist. Generating new service and rebuilding token")
        time.sleep(.5)

    return None

def parse_folder(folder_path):

    # get current time
    current_datetime = datetime.now()
    one_day_ago = current_datetime - timedelta(days=1)

    items = []

    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            create_time = datetime.fromtimestamp(os.path.getctime(item_path)) # check if create time is greater than now
            items.append(item_path)
    else:
        print(f"The folder '{folder_path}' does not exist")

    return items


# upload folder function
def upload_to_folder(raw_path, file_name, folder_id, drive_service):

    file_metadata = {
        'raw_path':  raw_path,
        'name': file_name,
        'parents': [folder_id]
    }

    mime_type, _ = mimetypes.guess_type(file_metadata['raw_path'])
    media = MediaFileUpload(file_metadata['raw_path'], mimetype=mime_type, resumable=True)
    request = drive_service.files().create(
        body=file_metadata,
        media_body = media,
        fields='id'
    )

    response = None

    while response is None:
        status, response = request.next_chunk()
        print(status, response)
        if status:
            print(f'Uploaded {int(status.progress())}%')

    print(f"Uploaded file {file_metadata['name']} complete")
    
def remove_path(folder_path):

    substring = "Dubstep-Test/"
    index = folder_path.find(substring)
    path_new_name = {}

    if index != -1:

    # Remove everything before "Dubstep-Test/" including "Dubstep-Test/"
        new_file_name = folder_path[index + len(substring):]
        path_new_name['raw_path'] = folder_path
        path_new_name['file_name'] = new_file_name

        return path_new_name
    
# execution
if __name__ == "__main__":

    credentials_path = 'credentials.json'

    # Load your secrets and credentials
    with open('secrets.json') as secrets_file:
        secrets = json.load(secrets_file)

    # build the drive service
    drive_service = build_drive_service(credentials_path, scopes=scopes)

    # # folder -id
    folder_id = secrets['folder_id']

    val = count_items_in_folder(folder_id)

    items = parse_folder(folder_path)
    # print(items)

    for item in items:
        item_dict = remove_path(item)
        upload_to_folder(item_dict['raw_path'], item_dict['file_name'], folder_id, drive_service)

  

