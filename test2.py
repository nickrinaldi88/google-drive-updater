# file_path = "heartbeat.log"

# try:
#     with open(file_path, 'w') as file:
#         file.truncate(0)
# except Exception as e:
#     print(f"There was an error clearing the context of {file_path}. Here's more info: \n{e}")

import datetime
from datetime import datetime

last_email_time = None

now = datetime.now()
result = (now - last_email_time).total_seconds() >= 24 * 3600
print(result)