file_path = "heartbeat.log"

try:
    with open(file_path, 'w') as file:
        file.truncate(0)
except Exception as e:
    print(f"There was an error clearing the context of {file_path}. Here's more info: \n{e}")
