from langchain_ollama import OllamaLLM
import json
import re

# List of JSON files to be combined
json_files = [
    "classified_comments_with_reasons.json",
    "Proposals_classified_comments.json"
]

# Load comments from JSON files
all_comments = []
for json_file in json_files:
    print(f"Loading comments from {json_file}...")
    with open(json_file) as f:
        comments = json.load(f)
        all_comments.extend(comments)
    print(f"Loaded {len(comments)} comments from {json_file}.")

print(f"Total comments loaded: {len(all_comments)}")

# Save the modified comments back to a single JSON file
output_file = "combined_classified_comments.json"
print(f"\nSaving classified comments with reasons to {output_file}...")
with open(output_file, "w") as f:
    json.dump(all_comments, f, indent=2)

print("Comments classified with reasons and saved successfully.")