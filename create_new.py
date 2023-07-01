import os
import json
import datetime

def get_latest_files(folder_path):
    file_dict = {}

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('.webp'):  # Check for files with the .webp extension
                file_path = os.path.join(root, file_name)
                file_stat = os.stat(file_path)
                creation_time = file_stat.st_ctime

                # Calculate the datetime of two weeks ago
                two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)

                # Ignore files created more than 2 weeks ago
                if datetime.datetime.fromtimestamp(creation_time) >= two_weeks_ago:
                    file_dict[creation_time] = os.path.splitext(file_name)[0]  # Store only the filename without extension

    return file_dict.values()

def save_files_to_json(file_list, json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump(list(file_list), json_file, indent=4)

# Specify the folder path
folder_path = './miniatures/_Colorized'

# Get the list of files with the latest creation dates
latest_files = get_latest_files(folder_path)

# Specify the JSON file path to save the results
json_file_path = './miniatures/_Colorized/new.json'

# Save the file list to a JSON file
save_files_to_json(latest_files, json_file_path)