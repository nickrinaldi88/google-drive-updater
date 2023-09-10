import os
import json
import time
# from google.oauth2.credentials import Credentials
from google.oauth2._credentials_async import Credentials
from googleapiclient.discovery import build, MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow


# scope
scopes = ['https://www.googleapis.com/auth/drive']

file_name = 'flava.mp3'

token_file = 'token.json'

# build drive service

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

def remove_token(token_file):

    if os.path.exists(token_file):
        os.remove(token_file)
    else:
        print("token does not exist. Generating new service and rebuilding token")
        time.sleep(.5)

    return None
# def add_token_to_creds(refresh_token):

#     with open('credentials.json', 'r') as creds_file:
#         credentials = json.load(creds_file)

#     credentials['installed']['refresh_token'] = refresh_token

#     with open('credentials.json', 'w') as creds_file:
#         json.dump(credentials, creds_file, indent=4)

# count items
def count_items_in_folder(folder_id):

    results = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name)"
    ).execute()

    print("results")
    print(results)

    items = results.get('files', [])
    return len(items)

# upload folder function
def upload_to_folder(file_name, drive_service):

    file_metadata = {
        'name': file_name
    }
    media = MediaFileUpload('flava.mp3', mimetype=None, resumable=True)
    request = drive_service.files().create(
        body=file_metadata,
        media_body = media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f'Uploaded {int(status.progress())}%')
    
    print("Upload complete")
    

    # look up docs for drive_services.files() methods
    # results = drive_service.files().list(q=f"'{folder_id}' in parents",fields="files(id, name)").execute()



# execution
if __name__ == "__main__":

    # remove file if exists
    remove_token(token_file)
    

    # Load your secrets and credentials
    with open('secrets.json') as secrets_file:
        secrets = json.load(secrets_file)

    client_creds_path = 'credentials.json'

    # build the drive service
    drive_service = build_drive_service(client_creds_path, scopes=scopes)

    # # folder -id
    folder_id = secrets['folder_id']

    val = count_items_in_folder(folder_id)

    upload_to_folder(file_name, drive_service)

  

