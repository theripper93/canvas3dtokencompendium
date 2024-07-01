import os
import json

# Define the extensions to include in the crawl
included_extensions = ['glb', 'gltf']  # Add more extensions as needed

# Function to crawl directory and collect file paths
def crawl_directory(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in included_extensions):
                file_paths.append(os.path.relpath(os.path.join(root, file), directory).replace("\\", "/"))
    return file_paths

# Get the directory of the current script file
script_directory = os.path.dirname(os.path.abspath(__file__))

# Crawl the script directory and subdirectories
file_paths = crawl_directory(script_directory)

# Save file paths as JSON
output_file = os.path.join(script_directory, 'index.json')
with open(output_file, 'w') as f:
    json.dump(file_paths, f, indent=4)

print(f"File paths saved to {output_file}")
