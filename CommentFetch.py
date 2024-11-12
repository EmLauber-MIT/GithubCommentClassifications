import requests
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# Configure logging for detailed output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

# Cache the contributors list
contributors_cache = None

# Function to fetch the list of contributors for caching
def fetch_contributors(owner, repo):
    global contributors_cache
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    try:
        response = requests.get(url, headers=headers)
        logging.debug("Fetching contributors list.")

        if response.status_code != 200:
            logging.error(f"Error fetching contributors: Received status code {response.status_code} with message: {response.text}")
            contributors_cache = []
            return

        contributors = response.json()
        # Cache the list of contributor usernames
        contributors_cache = [contributor["login"] for contributor in contributors]
        logging.info(f"Cached {len(contributors_cache)} contributors.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception occurred while fetching contributors: {e}")
        contributors_cache = []

# Function to check if a user is a contributor to the repository
def is_contributor(user):
    # Return False if there was an issue fetching contributors
    if contributors_cache is None:
        fetch_contributors(owner, repo)

    # Check if user is in the cached contributors list
    if user in contributors_cache:
        logging.debug(f"User {user} is a contributor.")
        return True
    else:
        logging.debug(f"User {user} is not a contributor.")
        return False

# Function to fetch issue comments from a repo
def fetch_issue_comments(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments"
    comments = []
    page = 1

    # Fetch and cache contributors before fetching comments
    fetch_contributors(owner, repo)

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
                user_is_contributor = is_contributor(user)  # Use cached contributors

                comments.append({
                    "id": comment["id"],
                    "issue_url": comment["issue_url"],
                    "created_at": comment["created_at"],
                    "updated_at": comment["updated_at"],
                    "body": comment["body"],
                    "user": user,
                    "is_owner": is_owner,
                    "is_contributor": user_is_contributor
                })

            logging.info(f"Fetched page {page} successfully.")
            page += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"Request exception occurred: {e}")
            break

    return comments

# Fetch comments and save them to a JSON file with the repository name in the filename
comments = fetch_issue_comments(owner, repo)

# Only save comments if they were fetched successfully
if comments:
    filename = f"{repo}_github_comments.json"
    with open(filename, "w") as f:
        json.dump(comments, f, indent=4)
    logging.info(f"Comments saved to {filename}")
else:
    logging.warning("No comments were fetched.")
