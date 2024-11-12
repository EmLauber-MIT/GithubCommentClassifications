import requests
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# Configure logging for detailed output
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if the token is loaded
if not token:
    logging.error("GitHub token not found. Make sure the GITHUB_TOKEN variable is set in the .env file.")
    exit(1)

# Define repository details
owner = "fedidcg"
repo = "LightweightFedCM"

# Define headers for authentication
headers = {
    "Authorization": f"token {token}"
}

# Function to fetch issue comments from a repo
def fetch_issue_comments(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments"
    comments = []
    page = 1

    while True:
        try:
            response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
            logging.debug(f"Fetching page {page} from {url}")

            if response.status_code == 403:
                logging.error("Rate limit exceeded. Please try again later or check your API usage.")
                break
            elif response.status_code != 200:
                logging.error(f"Error: Received status code {response.status_code} with message: {response.text}")
                break

            data = response.json()
            if not data:
                logging.info("No more comments to fetch.")
                break

            for comment in data:
                user = comment["user"]["login"]
                is_owner = user == owner
                is_contributor = check_if_contributor(owner, repo, user)
                comments.append({
                    "id": comment["id"],
                    "issue_url": comment["issue_url"],
                    "created_at": comment["created_at"],
                    "updated_at": comment["updated_at"],
                    "body": comment["body"],
                    "user": user,
                    "is_owner": is_owner,
                    "is_contributor": is_contributor
                })

            logging.info(f"Fetched page {page} successfully.")
            page += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception occurred: {e}")
            break

    return comments

# Function to check if a user is a contributor to the repository
def check_if_contributor(owner, repo, user):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    try:
        response = requests.get(url, headers=headers)
        logging.debug("Fetching contributors list.")

        if response.status_code != 200:
            logging.error(f"Error fetching contributors: Received status code {response.status_code} with message: {response.text}")
            return False

        contributors = response.json()
        for contributor in contributors:
            if contributor["login"] == user:
                logging.debug(f"User {user} is a contributor.")
                return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception occurred while fetching contributors: {e}")

    logging.debug(f"User {user} is not a contributor.")
    return False

# Fetch comments and save them to a JSON file
comments = fetch_issue_comments(owner, repo)

# Only save comments if they were fetched successfully
if comments:
    with open("github_comments.json", "w") as f:
        json.dump(comments, f, indent=4)
    logging.info("Comments saved to github_comments.json")
