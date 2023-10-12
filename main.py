import os
import json
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build, MediaFileUpload
from google.oauth2 import service_account
import mimetypes
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# configure logger

logging.basicConfig(filename='heartbeat.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# get current datetime
current_datetime = datetime.now()
date_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

# scope
scopes = ['https://www.googleapis.com/auth/drive']

#paths
source_path = '/Users/nickrinaldi/Desktop/Dubstep-Test/staging'
destination_path = '/Users/nickrinaldi/Desktop/Dubstep-Test/uploaded'
credentials_path = 'service_account_key.json'

# build event handler
class MyHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:  # Ignore directory creation events
            print(f"New file created: {event.src_path}")
            upload_and_move(event.src_path, destination_path=destination_path)

# build heartbeat 
def log_heartbeat():
    
    logging.info(f"Heartbeat: Script is still running at: {date_string}")
    time.sleep(3 * 36000)

# build drive service

def build_drive_service(credentials_path, scopes):

    creds = None

    try:
        creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
    except Exception as e:
        print(f"Error intializing service account creds. Exception: {e}")
        logging.error(f"Error intializing service account creds. Exception: {e}")

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def parse_folder(source_path):

    items = []

    if os.path.exists(source_path):
        # for item in os.listdir(source_path):
        # item_path = os.path.join(source_path, item)
        items.append(source_path)
    else:
        print(f"The folder '{source_path}' does not exist")
        logging.error(f"The folder '{source_path}' does not exist")

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
    logging.info(f"Uploaded file {file_metadata['name']} complete")
    
def remove_path(source_path):

    substring = "Dubstep-Test/staging/"
    index = source_path.find(substring)
    path_new_name = {}

    if index != -1:

    # Remove everything before "Dubstep-Test/" including "Dubstep-Test/"
        new_file_name = source_path[index + len(substring):]
        path_new_name['raw_path'] = source_path
        path_new_name['file_name'] = new_file_name

        return path_new_name
    
def move_file(source_path, destination_path):

    try:
        # Copy the file to the destination path
        with open(source_path, 'rb') as source_file:
            with open(destination_path, 'wb') as destination_file:
                destination_file.write(source_file.read())

        # Remove the file from the source path
        os.remove(source_path)

        print(f"File moved from '{source_path}' to '{destination_path}' successfully.")
    except Exception as e:
        print(f"Error moving the file: {str(e)}")


def upload_and_move(source_path, destination_path):

    with open('secrets.json') as secrets_file:
        secrets = json.load(secrets_file)

    # folder id
    folder_id = secrets['folder_id']

    # build the drive service
    drive_service = build_drive_service(credentials_path, scopes=scopes)

    items = parse_folder(source_path)

    for item in items:
        item_dict = remove_path(item)
        upload_to_folder(item_dict['raw_path'], item_dict['file_name'], folder_id, drive_service)
        destination_path = destination_path + "/" + item_dict['file_name']
        move_file(item_dict['raw_path'], destination_path=destination_path)

# execution
if __name__ == "__main__":

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=source_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
        log_heartbeat()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()