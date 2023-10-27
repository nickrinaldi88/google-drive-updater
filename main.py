import os
import json
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build, MediaFileUpload
from google.oauth2 import service_account
import mimetypes
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import emailer
from utils import emailer
from emailer import Emailer

################################# EMAIL CONFIGURATION #################################
# get current datetime
current_datetime = datetime.now()
date_string = current_datetime.strftime("%m-%d-%Y %H:%M:%S")

smtp_port = 587 # TLS port
smtp_server = "smtp.gmail.com"
total_file_count = 0

subject = f"GOOGLE DRIVE UPLOADER SCRIPT LOG - {date_string}"
body = "The script ran 48 times today, and uploaded a total of {total_file_count} files."
attachment_path = "heartbeat.log"
attachment = open(attachment_path, "rb")

# get smtp user + pass
try:
    with open('secrets.json', 'r') as file:
        data = json.load(file)
        smtp_username, sender_email, receiver_email = data['smtp_username']
        smtp_password = data['smtp_password']
except (FileNotFoundError, json.JSONDecodeError) as e:
    print("Error: ", e)
    logging.info("Error: ", e)
    

logging.basicConfig(filename='heartbeat.log', level=logging.INFO, format='%(asctime)s - %(message)s')


# scope
scopes = ['https://www.googleapis.com/auth/drive']

#paths
source_path = '/Users/nickrinaldi/Desktop/Dubstep-Uploader/staging'
destination_path = '/Users/nickrinaldi/Desktop/Dubstep-Uploader/uploaded'
credentials_path = 'service_account_key.json'
dash = "-"

# build heartbeat 
def log_heartbeat():

    # print(f"Heartbeat: Script is still running at: {date_string}")
    logging.info(f"INTERNAL LOG: Script run executed at: {date_string}")
    logging.info(dash * 25)

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
        for item in os.listdir(source_path):
            item_path = os.path.join(source_path, item)
            items.append(item_path)
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
    logging.info(dash * 25)
    
def remove_path(source_path):

    substring = "Dubstep-Uploader/staging/"
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

    counter = 0

    with open('secrets.json') as secrets_file:
        secrets = json.load(secrets_file)

    # folder id
    folder_id = secrets['folder_id']

    # build the drive service
    drive_service = build_drive_service(credentials_path, scopes=scopes)

    items = parse_folder(source_path)
    item_len = len(items)

    if item_len > 0:
        for item in items:
            counter += 1
            item_dict = remove_path(item)
            upload_to_folder(item_dict['raw_path'], item_dict['file_name'], folder_id, drive_service)
            destination_path = destination_path + "/" + item_dict['file_name']
            move_file(item_dict['raw_path'], destination_path=destination_path)
    else:
        logging.info("No files to upload")

    
# execution
if __name__ == "__main__":
    
    log_heartbeat()
    upload_and_move(source_path=source_path, destination_path=destination_path)
    attachment_path = "files/heartbeat.log"
    emailer = Emailer(smtp_server, smtp_username, smtp_password, smtp_port)
    # if 24 hours have passed, send email
    if emailer.record_email_time():
        email = emailer.create_email(sender_email, receiver_email, subject, body, attachment_path)
        emailer.send_email(sender_email, receiver_email, email)



