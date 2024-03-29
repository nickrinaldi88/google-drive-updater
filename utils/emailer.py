import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import datetime
from datetime import datetime, timedelta
import os

class Emailer:

    def __init__(self, smtp_server, smtp_username, smtp_password, smtp_port):

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port  # TLS
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def record_email_time(self):

        date_format = "%Y-%m-%d %H:%M:%S.%f"

        current_time = datetime.now()
        with open("files/last_email_time.txt", 'r') as file:
            # read last email times
            last_email_time_str = file.read()
            print(last_email_time_str)
            # get difference
            if last_email_time_str != '':
                last_email_time = datetime.strptime(last_email_time_str, date_format)
                difference = current_time - last_email_time
                if difference >= timedelta(hours=24):
                    with open("files/last_email_time.txt", 'w') as file: 
                        # write a new time
                        file.write(str(current_time))
                    # return True
                    return True
            return False
        return False

    def create_email(self, sender_email, receiver_email, subject, body, attachment_path, date_string):

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach a file
        part = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as file:
                part.set_payload(file.read())
        encoders.encode_base64(part)
        attachment = os.path.basename(attachment_path)
        attachment_name = f"{attachment} - {date_string}"
        part.add_header('Content-Disposition', f"attachment; filename= {attachment_name}")

        msg.attach(part)

        return msg
    
    def send_email(self, sender_email, receiver_email, msg):

        # Start server
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_username, self.smtp_password)

        # Send email

        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close server
        server.quit()
