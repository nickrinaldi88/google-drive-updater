#!/bin/bash

# Set the path to your log file
LOG_FILE="/Users/nickrinaldi/dev/google-drive-updater/heartbeat.log"

# Set the path to the file that stores the counter
COUNTER_FILE="/Users/nickrinaldi/dev/google-drive-updater/counter.txt"

# Log a timestamp to indicate when the script started
echo "Script started at $(date)" >> "$LOG_FILE"

# Change to the directory where your Python script is located
cd /Users/nickrinaldi/dev/google-drive-updater

# Log a message indicating that the Python script is about to be executed
echo "Executing Python script" >> "$LOG_FILE"

# Execute your Python script
python3 main.py

# Log a message to indicate the Python script execution has completed
echo "Python script execution completed" >> "$LOG_FILE"

# Log a timestamp to indicate when the script finished
echo "Script finished at $(date)" >> "$LOG_FILE"

echo "***********************************" >> "$LOG_FILE"

# Read the current counter value
if [ -f "$COUNTER_FILE" ]; then
  COUNTER=$(cat "$COUNTER_FILE")
else
  COUNTER=0
fi

# Increment the counter
((COUNTER++))

# Save the updated counter value
echo "$COUNTER" > "$COUNTER_FILE"

echo "$COUNTER"

