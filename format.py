import json

# Path to your JSON file
json_file = "combined_classified_comments.json"

# Load the JSON data
with open(json_file, "r") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)

# Save the reformatted JSON data back to the file
with open(json_file, "w") as f:
    json.dump(data, f, indent=2)

print("JSON file reformatted successfully.")