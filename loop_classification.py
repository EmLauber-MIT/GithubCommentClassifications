from langchain_ollama import OllamaLLM
import json
import re

# Load comments from JSON file
print("Loading comments from JSON file...")
REPO_NAME = "LightweightFedCM"
json_file = f"{REPO_NAME}_github_comments.json"

with open(json_file) as f:
    comments = json.load(f)
print(f"Loaded {len(comments)} comments.")

# Define the prompt template function
def build_prompt(comment_body):
    prompt = f"""
    Review the following comment and classify it as one of the following: 
    Technical Feedback, Use Case, Feature Request, Administrative, Conclusion / Resolution, Philosophical, or Unknown.
    Provide the classification in the format: "Classification: <Category>" followed by a brief explanation starting with "Reason:".
    '''
    {comment_body}
    '''
    """
    return prompt

# Specify the model to use
model = OllamaLLM(model="llama3.2:1b")
print("Initialized model for classification.")

# Categories for classification standardization
CLASSIFICATIONS = {
    "Technical Feedback": "technical_feedback",
    "Use Case": "use_case",
    "Feature Request": "feature_request",
    "Administrative": "administrative",
    "Conclusion / Resolution": "conclusion_resolution",
    "Philosophical": "philosophical",
    "Unknown": "unknown"
}

# Process each comment
for idx, comment in enumerate(comments, 1):
    # Extract the body and ID of the comment
    comment_body = comment.get("body", "")
    comment_id = comment.get("id", "Unknown ID")
    
    print(f"\nProcessing comment {idx}/{len(comments)} with ID {comment_id}...")

    # Build the prompt and invoke the model
    prompt = build_prompt(comment_body)
    print("Prompt built. Sending to model for classification...")
    result = model.invoke(input=prompt)
    print(f"Model response: {result}")

    # Extract classification and reason
    classification_match = re.search(r'Classification:\s*(\w+(?: \w+)*)', result, re.IGNORECASE)
    reason_match = re.search(r'Reason:\s*(.*)', result, re.IGNORECASE)

    classification_label = classification_match.group(1) if classification_match else "Unknown"
    reason_text = reason_match.group(1).strip() if reason_match else "No reason provided."
    
    # Map to standard classification label
    classification = CLASSIFICATIONS.get(classification_label.strip(), "unknown")
    print(f"Classification for comment ID {comment_id}: {classification} (original label: {classification_label})")
    print(f"Reason for classification: {reason_text}")

    # Append classification and reason to the comment
    comment["classification"] = classification
    comment["reason"] = reason_text

# Save the modified comments back to JSON
output_file = f"combined_classified_comments.json"
print(f"\nSaving classified comments with reasons to {output_file}...")
with open(output_file, "w") as f:
    json.dump(comments, f, indent=2)

print("Comments classified with reasons and saved successfully.")
