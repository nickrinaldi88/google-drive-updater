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
from utils.emailer import Emailer

################################# EMAIL CONFIGURATION #################################
# get current datetime
current_datetime = datetime.now()
date_string = current_datetime.strftime("%m-%d-%Y %H:%M:%S")
total_file_count = 0

# get smtp user + pass
try:
    with open('secrets.json', 'r') as file:
        data = json.load(file)
        smtp_username = sender_email = receiver_email = data['smtp_username']
        smtp_password = data['smtp_password']
except (FileNotFoundError, json.JSONDecodeError) as e:
    print("Error: ", e)
    logging.info("Error: ", e)

try:
    with open('files/counter.txt', 'r') as file:
        total_file_count = file.read()
except (FileNotFoundError) as e:
    print("Error:", e)
    logging.info("Error: ", e)


smtp_port = 587 # TLS port
smtp_server = "smtp.gmail.com"

subject = f"GOOGLE-DRIVE-UPLOADER SCRIPT LOG - {date_string}"
body = f"The script and uploaded a total of {total_file_count} files today."

 ################################# LOGGING + MISC CONFIG #################################   

logging.basicConfig(filename='logs/heartbeat.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# scope
scopes = ['https://www.googleapis.com/auth/drive']

#paths
source_path = '/Users/nickrinaldi/Desktop/Dubstep-Uploader/staging'
destination_path = '/Users/nickrinaldi/Desktop/Dubstep-Uploader/uploaded'
counter_path = 'files/counter.txt'
credentials_path = 'service_account_key.json'
dash = "-"

# build heartbeat 
def log_heartbeat():

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

    logging.info(f"*** Uploaded File: {file_metadata['name']} complete ***")
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


    with open('secrets.json', 'r+') as secrets_file:
        secrets_file = secrets_file.read()
        # print(secrets)
        secrets = json.loads(secrets_file)

    # folder id
    folder_id = secrets['folder_id']

    # build the drive service
    drive_service = build_drive_service(credentials_path, scopes=scopes)

    # initialize counter

    items = parse_folder(source_path)
    item_len = len(items)

    counter = 0
    if item_len > 0:
        counter = 0
        for item in items:
            item_dict = remove_path(item)
            if item_dict['file_name'] != ".DS_Store":
                counter += 1
                upload_to_folder(item_dict['raw_path'], item_dict['file_name'], folder_id, drive_service)
                destination_path = destination_path + "/" + item_dict['file_name']
                move_file(item_dict['raw_path'], destination_path=destination_path)
    else:
        logging.info("No files to upload")

    # add to counter

    # read file
    try:
        with open(counter_path, 'r') as file:
            print("files_moved: ")
            files_moved = file.read()
    except FileNotFoundError as e:
        logging.info(e)
        previous_value = 0

    try: 
        with open(counter_path, 'w') as file:
            print("files_moved: ")
            previous_value = int(files_moved) if files_moved else 0
            print("previous", previous_value)
            new_value = previous_value + counter
            print("new", new_value)
            file.write(str(new_value))
    except FileNotFoundError as e:
        logging.info(e)
        previous_value = 0
    
    return new_value

# execution
if __name__ == "__main__":
    
    log_heartbeat()
    new_value = upload_and_move(source_path=source_path, destination_path=destination_path)
    attachment_path = "logs/heartbeat.log"
    emailer = Emailer(smtp_server, smtp_username, smtp_password, smtp_port)
    last_email_time = emailer.record_email_time()

    # if 24 hours have passed, send email
    if last_email_time: # if true, create + send email 
    # if new_value > 4:


        # reset counter
        with open('files/counter.txt', 'w+') as file:
            file.write("")

        # write email

        email = emailer.create_email(sender_email, receiver_email, subject, body, attachment_path, date_string)

        # send email 

        emailer.send_email(sender_email, receiver_email, email)
        
        # clear logs

        with open('logs/heartbeat.log', 'w+') as file:
            file.write("")




