#!/bin/bash

# Set the path to your log file
LOG_FILE="/Users/nickrinaldi/dev/google-drive-updater/heartbeat.log"

COUNTER_FILE="/Users/nickrinaldi/dev/google-drive-updater/counter.txt"

# Set the path to the file that stores the last execution timestamp
LAST_EXECUTION_FILE="/Users/nickrinaldi/dev/google-drive-updater/last_ex_time.txt"

# Get SMTP creds

SMTP_USERNAME=$(jq -r '.smtp_username' /Users/nickrinaldi/dev/google-drive-updater/secrets.json)
SMTP_PASSWORD=$(jq -r '.smtp_password' /Users/nickrinaldi/dev/google-drive-updater/secrets.json)

# Get the current timestamp
CURRENT_TIMESTAMP=$(date +%s)

# Read the last execution timestamp
if [ -f "$LAST_EXECUTION_FILE" ]; then
  LAST_EXECUTION_TIMESTAMP=$(cat "$LAST_EXECUTION_FILE")
else
  LAST_EXECUTION_TIMESTAMP=0
fi

# Calculate the time elapsed since the last execution
TIME_ELAPSED=$((CURRENT_TIMESTAMP - LAST_EXECUTION_TIMESTAMP))

# Check if 24 hours (86400 seconds) have passed
if [ "$TIME_ELAPSED" -ge 86400 ]; then
  # Send an email with the log file attached
  # Replace the following placeholders with your email configuration
  TO=$SMTP_USERNAME
  FROM="sender@example.com"
  SUBJECT="GOOGLE DRIVE UPLOADER SCRIPT LOG " + $CURRENT_TIMESTAMP
  SMTP_SERVER="smtp.gmail.com"
  SMTP_PORT="25"
  SMTP_USER=$SMTP_USERNAME
  SMTP_PASS=$SMTP_PASSWORD

  COUNTER=$(cat "$COUNTER_FILE")

   # Send email body 
  EMAIL_BODY="The mixing music uploader ran $COUNTER times today.\n\nSee attached log for more info"


  # Use the 'mail' command to send an email with the log file attachment
  echo -e "$EMAIL_BODY"| mail -s "$SUBJECT" -a "$LOG_FILE" -S smtp="$SMTP_SERVER" -S smtp-use-starttls -S smtp-auth=login -S smtp-auth-user="$SMTP_USER" -S smtp-auth-password="$SMTP_PASS" -S smtp-port="$SMTP_PORT" -r "$FROM" "$TO"

  # open counter
  cat "$COUNTER_FILE"
  # Clear the log file
  > "$LOG_FILE"
  # Clear the counter
  > "$COUNTER_FILE"

  # Update the last execution timestamp to the current timestamp
  echo "$CURRENT_TIMESTAMP" > "$LAST_EXECUTION_FILE"
fi
