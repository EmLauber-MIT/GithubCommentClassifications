# GithubCommentClassifications
Repo to work on 1.125 class project on using LLM to classify Github engagement comments

# Final Video

<iframe src="https://mitprod-my.sharepoint.com/personal/emlauber_mit_edu/_layouts/15/embed.aspx?UniqueId=7afbdc63-fc67-47bc-83b9-7d23c6ba7f4f&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="1125 Final Cut_W3C.mp4"></iframe>

# Code Structure 
- Public
    - Index.html: webpage to display visualizations 
    - combined_classified_comments.json: storage of classified comments 
- CommentFetch.py: script to fetch comments from a specified repo
- loop_classification.py: script to classify the comments using my defined classification types
- server.js: backend for form submission on webpage 
- analysis_request.json: collection of requested repos for analysis 
- raw comments 
    - various Github repository JSON files 

# How To Run
## For Visualizations 
The best user experience is to navigate the webpage yourself for the visualizations.

**Prerequisites**
- Node 

This can be run locally or in a Github CodeSpace environment. 

1) Download the repository 
2) Run *npm start* in the terminal to start the server.js file  
3) Open index.html on the local port 
4) Navigate the webpage by selecting from the available respositories for visualizations or submit a request for a new respository to analyze 

# For Classifications
If you'd like to run the classifications yourself, you can do so in the following steps. 

**Prerequisites**
- Ollama 
- Python

1) Download the repository 
2) Start by fetching comments from a repository
    a) Run CommentFetch.py with changed constants for your preferred repository: owner = "" & repo = ""
3) The JSON file will save as "RepoName_github_comments.json"
4) Run "loop_classification.py" with the updated constant REPO_NAME = ""
    a) Note: this requires a local copy of Ollama, version llama3.2:1b
    b) Note: this could take a long time if there are a large amount of comments.
5) The comments will append to the existing "combined_classified_comments.json" file. You can then run the instructions above for visualizations of the repo. 




