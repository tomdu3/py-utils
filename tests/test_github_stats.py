from unittest.mock import patch
import requests
from utils.github_stats import fetch_github_user, fetch_github_repos


@patch("utils.github_stats.requests.get")
def test_fetch_github_user_success(mock_get):
    # Mock successful response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "login": "octocat",
        "name": "The Octocat",
        "public_repos": 8,
    }

    result = fetch_github_user("octocat")
    assert result is not None
    assert result["login"] == "octocat"
    assert result["name"] == "The Octocat"
    assert result["public_repos"] == 8
    mock_get.assert_called_once()


@patch("utils.github_stats.requests.get")
def test_fetch_github_user_not_found(mock_get):
    # Mock 404 response
    mock_get.return_value.status_code = 404

    result = fetch_github_user("nonexistent-user")
    assert result is None


@patch("utils.github_stats.requests.get")
def test_fetch_github_user_network_error(mock_get):
    # Mock connection error
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection timed out")

    result = fetch_github_user("octocat")
    assert result is None


@patch("utils.github_stats.requests.get")
def test_fetch_github_repos_success(mock_get):
    # Mock successful repo list response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "repo1", "stargazers_count": 10},
        {"name": "repo2", "stargazers_count": 5},
    ]

    result = fetch_github_repos("octocat")
    assert len(result) == 2
    assert result[0]["name"] == "repo1"
    assert result[1]["stargazers_count"] == 5
