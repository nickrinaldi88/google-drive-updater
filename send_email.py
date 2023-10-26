import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import datetime
from datetime import datetime



class Emailer:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port  # TLS
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def create_email(self, sender_email, receiver_email, subject, body, attachment):

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment_name}")

        msg.attach(part)
        
        # Create MIME object 

smtp_server = "smtp.gmail.com"
smtp_port = 587  # TLS
smtp_username = "rinaldinick88@gmail.com"
smtp_password = "xpzg zhzn zmla yncj"
body = "This is the email body."
sender_email = smtp_username
receiver_email = sender_email

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