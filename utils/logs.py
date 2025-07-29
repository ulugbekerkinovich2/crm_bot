import json
import os
from datetime import datetime

def log_to_json(log_data):
    log_file='bot_logs.json'
    """Append log data to a JSON file."""
    if not os.path.isfile(log_file):
        # Create the file if it does not exist
        with open(log_file, 'w') as file:
            json.dump([], file)  # Initialize with an empty list
    
    with open(log_file, 'r+') as file:
        logs = json.load(file)  # Load existing logs
        logs.append(log_data)   # Append new log data
        file.seek(0)            # Move file cursor to the beginning
        json.dump(logs, file, indent=4)  # Write updated logs back to file
