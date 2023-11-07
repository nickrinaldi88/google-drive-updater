# Google Drive Uploader Script

This Python script is designed to upload files from a source directory to a Google Drive folder and move them to a destination directory while keeping track of the number of files uploaded. It also includes a feature to send email notifications with an attachment of the script's log file after a specified time interval.

Version
-------

- ```0.0.1```


Prerequisites
-------------

Before using the script, ensure that you have the following prerequisites in place:

- **Python:** You need to have Python installed on your system.

- **Google Drive API Access:** You must have access to the Google Drive API. You can set up a Google Cloud project, create credentials, and enable the Google Drive API.

- **Google Drive Service Account Key:** You should have a service account key JSON file that grants the script access to your Google Drive. Save this file as `service_account_key.json` in the script's directory.

- **Secrets Configuration:** Create a `secrets.json` file with the following content:
   ```json
   {
       "folder_id": "YOUR_FOLDER_ID",
       "smtp_username": "YOUR_SMTP_USERNAME",
       "smtp_password": "YOUR_SMTP_PASSWORD"
   }

- Replace `YOUR_FOLDER_ID` with the Google Drive folder ID where you want to upload files.

- Replace `YOUR_SMTP_USERNAME` and `YOUR_SMTP_PASSWORD` with your SMTP server credentials for sending email notifications.

- **Source and Destination Directories:** Configure the `source_path` and `destination_path` variables in the script to specify the source and destination directories.

Usage
-----

- Run the script by executing it using Python.

- ``` python main.py```

- The script will upload files from the source_path to the specified Google Drive folder, and then move them to the destination_path.

- The script will keep track of the number of files uploaded and store it in the files/counter.txt file.

- After a specified time interval, the script will send an email notification with the script's log file attached to the specified email addresses. You can configure the time interval in the script.

Setting up as a Cron Job
------------------------

To schedule the script to run periodically as a cron job, follow these steps:

1. Open your terminal or SSH into the server where you want to set up the cron job.

2. Edit your crontab file by running the following command:

- Add a new line to specify when and how often you want the script to run. For example, to run the script every day at 2:00 AM, you can use the following line:

    shellCopy code

    `0 2 * * * /usr/bin/python /path/to/your_script.py`

    Replace `/usr/bin/python` with the correct path to your Python interpreter and `/path/to/your_script.py` with the actual path to your script.

- Save and exit the crontab editor.

The script will now run as a cron job at the specified time and frequency. Make sure to adjust the timing and frequency to match your specific requirements.

Logging
-------

The script logs its activities to the `logs/heartbeat.log` file. You can review this log file to track the script's execution and any potential issues.

Email Notifications
-------------------

The script sends email notifications using the provided SMTP server credentials. The email content includes information about the number of files uploaded and a log file attachment for reference.

Error Handling
--------------

The script handles errors and logs them for easy debugging. If any issues occur during execution, you can check the log file for error details.


Important Note
--------------

Make sure to keep your service_account_key.json and secrets.json files secure, as they contain sensitive information.

For any questions or issues with the script, please contact the script owner or maintainer (rinaldinick88@gmail.com).

Future Improvements
-------------------

v2 will set to release Winter 2024. It will include improvements such as:

- **Unit Tests:** A comprehensive set of unit tests to ensure the script's functionality is reliable and free of errors.

- **Code Refactoring:** The code will be refactored to improve readability, maintainability, and adherence to coding best practices.

- **Enhanced Error Handling:** The new version will include enhanced error handling and more detailed error messages for easier debugging.

- **Additional Features:** Depending on user feedback and requirements, we may add new features and enhancements to further improve the script's functionality.

Stay tuned for updates and enhancements in the upcoming v2 release!