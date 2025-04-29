import json
import csv
from pathlib import Path

def convert_json_to_csv(json_file, csv_file):
    """
    Convert JSON data to CSV format.
    
    Args:
        json_file (str): Path to the input JSON file
        csv_file (str): Path to the output CSV file
    """
    # Read JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Define CSV headers based on the JSON structure
    headers = ['id', 'title', 'author', 'created_utc', 'score', 'url', 'selftext', 'num_comments']
    
    # Write to CSV
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for post in data:
            # Create a new dict with only the fields we want
            row = {header: post.get(header, '') for header in headers}
            writer.writerow(row)

if __name__ == "__main__":
    # Define input and output file paths
    json_file = "lets_talk_music_data/LetsTalkMusic_new.json"
    csv_file = "lets_talk_music_data/LetsTalkMusic_new.csv"
    
    # Create output directory if it doesn't exist
    Path(csv_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Convert the file
    convert_json_to_csv(json_file, csv_file)
    print(f"Successfully converted {json_file} to {csv_file}") 