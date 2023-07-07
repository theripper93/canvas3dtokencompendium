import os
import json
import datetime
import math
from PIL import Image

def merge_images(images, output_path):
    total_images = len(images)
    thumbnail_size = (400, 400)  # Adjust the size of each thumbnail as per your needs

    # Calculate the number of rows and columns for a square aspect ratio
    sqrt_total = math.sqrt(total_images)
    rows = math.ceil(sqrt_total)
    cols = math.ceil(total_images / rows)

    album_width = thumbnail_size[0] * cols
    album_height = thumbnail_size[1] * rows
    album_image = Image.new('RGB', (album_width, album_height))

    for i, image_path in enumerate(images):
        image = Image.open(image_path)
        image.thumbnail(thumbnail_size)
        row = i // cols
        col = i % cols
        x = col * thumbnail_size[0]
        y = row * thumbnail_size[1]
        album_image.paste(image, (x, y))

    album_image.save(output_path)

image_paths = []

def get_latest_files(folder_path):
    file_dict = {}

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('.webp'):  # Check for files with the .webp extension
                # If the file includes "topdown" in its name, ignore it
                if 'topdown' in file_name.lower():
                    continue
                
                file_path = os.path.join(root, file_name)
                file_stat = os.stat(file_path)
                creation_time = file_stat.st_ctime

                # Calculate the datetime of two weeks ago
                two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)

                # Ignore files created more than 2 weeks ago
                if datetime.datetime.fromtimestamp(creation_time) >= two_weeks_ago:
                    image_paths.append(file_path)
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

output_path = 'latest.jpg'

merge_images(image_paths, output_path)