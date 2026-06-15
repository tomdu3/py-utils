#!/usr/bin/env python3
"""
GitHub Stats Utility
Retrieves and displays statistics for a GitHub user and their repositories.
Can be run as a standalone script or imported as a module.
"""

import argparse
import os
import sys
from typing import Any
import requests


def fetch_github_user(username: str, token: str | None = None) -> dict[str, Any] | None:
    """
    Fetches profile information for a specified GitHub user.
    """
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Python-GitHub-Stats-Retriever",
    }

    if token:
        headers["Authorization"] = f"token {token}"

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(
                f"Error: User '{username}' not found. (Status Code: 404)",
                file=sys.stderr,
            )
        elif response.status_code == 403:
            print(
                "Error: Access forbidden or Rate limit exceeded. (Status Code: 403)",
                file=sys.stderr,
            )
            if not token:
                print(
                    "Tip: Provide a GITHUB_TOKEN environment variable or use the --token option to increase rate limits.",
                    file=sys.stderr,
                )
        else:
            print(
                f"Error: Failed to retrieve user data. Status Code: {response.status_code}",
                file=sys.stderr,
            )

    except requests.exceptions.RequestException as e:
        print(f"Network error occurred while fetching user: {e}", file=sys.stderr)

    return None


def fetch_github_repos(username: str, token: str | None = None) -> list[dict[str, Any]]:
    """
    Fetches the list of public repositories for a specified GitHub user, sorted by recent activity.
    """
    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Python-GitHub-Stats-Retriever",
    }

    if token:
        headers["Authorization"] = f"token {token}"

    params: dict[str, Any] = {"sort": "updated", "per_page": 100}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()
        elif (
            response.status_code != 404
        ):  # Avoid double 404 error messages if already handled
            print(
                f"Error: Failed to retrieve repositories. Status Code: {response.status_code}",
                file=sys.stderr,
            )

    except requests.exceptions.RequestException as e:
        print(
            f"Network error occurred while fetching repositories: {e}", file=sys.stderr
        )

    return []


def print_user_stats(user_data: dict):
    """
    Prints GitHub user profile details.
    """
    name = user_data.get("name", "N/A")
    login = user_data.get("login", "N/A")
    company = user_data.get("company", "N/A")
    bio = user_data.get("bio", "N/A")
    location = user_data.get("location", "N/A")
    public_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    following = user_data.get("following", 0)
    html_url = user_data.get("html_url", "N/A")

    print("\n" + "=" * 50)
    print(f" GITHUB PROFILE: {login} ({name})")
    print("=" * 50)
    print(f"Profile URL:  {html_url}")
    print(f"Location:     {location}")
    print(f"Company:      {company}")
    print(f"Bio:          {bio}")
    print(f"Followers:    {followers} | Following: {following}")
    print(f"Public Repos: {public_repos}")
    print("=" * 50)


def print_repo_stats(repos: list, limit: int = 5):
    """
    Prints a table of top repositories.
    """
    if not repos:
        print("\nNo repositories found or retrieved.")
        return

    print(f"\nTop {min(limit, len(repos))} Repositories (sorted by recent activity):")
    print(
        f"{'Repository Name':<30} | {'Stars':<6} | {'Language':<12} | {'Description'}"
    )
    print("-" * 80)

    for repo in repos[:limit]:
        repo_name = repo.get("name", "N/A")
        stars = repo.get("stargazers_count", 0)
        lang = repo.get("language") or "N/A"
        desc = repo.get("description") or "No description"

        # Truncate description if too long
        if len(desc) > 30:
            desc = desc[:27] + "..."

        print(f"{repo_name:<30} | {stars:<6} | {lang:<12} | {desc}")
    print("-" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub stats for a user.")
    parser.add_argument(
        "username",
        nargs="?",
        default="octocat",
        help="GitHub username to query (default: octocat)",
    )
    parser.add_argument(
        "-t",
        "--token",
        help="GitHub Personal Access Token (defaults to GITHUB_TOKEN environment variable)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=5,
        help="Number of repositories to display (default: 5)",
    )

    args = parser.parse_args()

    # Use token from argument or environment variable
    token = args.token or os.environ.get("GITHUB_TOKEN")

    user_data = fetch_github_user(args.username, token)
    if not user_data:
        sys.exit(1)

    print_user_stats(user_data)

    repos = fetch_github_repos(args.username, token)
    print_repo_stats(repos, args.limit)


if __name__ == "__main__":
    main()
