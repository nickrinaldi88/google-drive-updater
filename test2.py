import os

counter_path = '/Users/nickrinaldi/dev/google-drive-updater/files/counter.txt'

with open(counter_path, 'r+') as file:
    # file.seek(0)
    print("files_moved: ")
    files_moved = file.read()
    print(files_moved)