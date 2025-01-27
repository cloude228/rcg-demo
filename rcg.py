import os
import subprocess
import requests
from git import Repo

# Config
BITBUCKET_USERNAME = "rcg-demo-cloude"
BITBUCKET_APP_PASSWORD = ""
GITHUB_USERNAME = "cloude228"
GITHUB_TOKEN = ""
BITBUCKET_WORKSPACE = "rcg-demo-cloudesingh"
BITBUCKET_REPOS = ["repo1", "repo2", "repo3"]
GITHUB_REPOS = ["Migration-repo1", "Migration-repo2", "Migration-repo3"]

# Helper Functions
def create_github_repo(repo_name):
    # Create a new GitHub repository
    url = f"https://api.github.com/user/repos"
    payload = {"name": repo_name, "private": False}
    response = requests.post(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN), json=payload)
    response.raise_for_status()

def mirror_repo(bitbucket_repo, github_repo):
    # Define the local directory for the Bitbucket repository
    repo_dir = os.path.join(os.getcwd(), bitbucket_repo)

    # Clone the Bitbucket repository if it doesn't already exist locally
    if not os.path.exists(repo_dir):
        Repo.clone_from(
            f"https://{BITBUCKET_USERNAME}:{BITBUCKET_APP_PASSWORD}@bitbucket.org/{BITBUCKET_WORKSPACE}/{bitbucket_repo}.git",
            repo_dir,
            mirror=False  # Clone the full repository with working tree
        )

    repo = Repo(repo_dir)

    # Fetch all branches from the Bitbucket repository
    origin = repo.remote(name="origin")
    origin.fetch(prune=True)

    # Add GitHub as a new remote
    if "github" not in repo.remotes:
        repo.create_remote(
            "github",
            url=f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{github_repo}.git",
        )

    github_remote = repo.remote(name="github")

    # Push each branch from Bitbucket to GitHub
    for ref in origin.refs:
        branch_name = ref.remote_head
        if branch_name == "HEAD":  # Skip the symbolic HEAD reference
            continue
        print(f"Pushing branch: {branch_name} from {bitbucket_repo} to {github_repo}")
        github_remote.push(f"refs/remotes/origin/{branch_name}:refs/heads/{branch_name}")

    # Push all tags to GitHub
    repo.git.push("github", "--tags")

    print(f"Completed mirroring {bitbucket_repo} to {github_repo}")

# Main Script
if __name__ == "__main__":
    # Step 1: Create corresponding GitHub repositories
    for github_repo in GITHUB_REPOS:
        create_github_repo(github_repo)

    # Step 2: Mirror each Bitbucket repository to its GitHub counterpart
    for bitbucket_repo, github_repo in zip(BITBUCKET_REPOS, GITHUB_REPOS):
        mirror_repo(bitbucket_repo, github_repo)

    print("Migration completed successfully!")
