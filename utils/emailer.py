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

    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password, last_email_time):

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port  # TLS
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.last_email_time = last_email_time

    def record_email_time(self):

        current_time = datetime.now()
        with open("../last_email_time.txt", 'w+') as file:
            last_email_time = file.read()
            difference = current_time - last_email_time
            if difference >= timedelta(hours=24):
                file.write(str(current_time))
                return True
            return False
    
    def should_send_email(self):
        if not self.last_email_time:
            return True
        now = datetime.now()
        return (now - self.last_email_time).total_seconds() >= 24 * 3600
        

    def create_email(self, sender_email, receiver_email, subject, body, attachment):

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Attach a file
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        attachment_name = f"heartbeat.log - {date_string}"
        part.add_header('Content-Disposition', f"attachment; filename= {attachment_name}")

        msg.attach(part)

        return msg
    
    def send_email(self, sender_email, receiver_email, msg):

        # start server

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_username, self.smtp_password)

        # send email

        server.sendmail(sender_email, receiver_email, msg.as_strong())

        # close server
        server.quit()
        
        # Create MIME object 



current_datetime = datetime.now()
date_string = current_datetime.strftime("%m-%d-%Y %H:%M:%S")

subject = f"GOOGLE DRIVE UPLOADER SCRIPT LOG - {date_string}"
attachment_path = "heartbeat.log"
attachment_name = f"heartbeat.log - {date_string}"
attachment = open(attachment_path, "rb")

# Create an SMTP session
server = smtplib.SMTP(smtp_server, smtp_port)
 
server.starttls()  # Upgrade the connection to a secure TLS connection
server.login(smtp_username, smtp_password)

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f"attachment; filename= {attachment_name}")

msg.attach(part)

email_text = f"Subject: {subject}\n\n{body}"
server.sendmail(sender_email, receiver_email, msg.as_string())

# Close the SMTP session
server.quit()