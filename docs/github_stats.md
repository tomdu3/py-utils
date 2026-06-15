# GitHub Stats Retriever Guide

This guide describes how to construct a Python script to retrieve user profiles and repository statistics from the **GitHub REST API** using Python's **`requests` library**. It outlines the core concepts, a step-by-step implementation plan, key API endpoints, and important considerations.

---

## Core Concepts

Understanding these basic concepts is essential before starting your implementation:

### 1. The GitHub REST API
GitHub exposes a public API that allows developers to access data programmatically. Information is retrieved by sending standard HTTP requests to specific URLs called **endpoints**.
*   **Base API URL:** `https://api.github.com`
*   **Authentication:** Public data can be fetched without authentication, but GitHub imposes low rate limits. To increase limits or read private metadata, you must authenticate using a **Personal Access Token (PAT)**.

### 2. HTTP GET Requests
A **GET** request is the standard HTTP method used to retrieve resources from a server. In Python, you initiate this using:
```python
import requests
response = requests.get(url, headers=headers)
```

### 3. Header Fields
GitHub expects specific request headers to ensure compatibility and identify your application:
*   **`Accept`**: Set to `application/vnd.github+json` to tell GitHub you want the standard v3 JSON response.
*   **`User-Agent`**: GitHub's API rules require a unique `User-Agent` header (e.g., your script name or username). Requests without one may be rejected with a `403 Forbidden` response.
*   **`Authorization`**: If authenticated, set this header to `token <YOUR_TOKEN>`.

### 4. JSON Format
The response body is returned as a JSON-formatted string. Calling `response.json()` parses this string into native Python data structures (dictionaries and lists), which can be queried using standard dictionary lookup methods.

---

## Step-by-Step Implementation Workflow

When writing your script, build and test your code incrementally using these steps:

### Step 1: Send the Request
Construct your target URL, set up the headers, and call `requests.get()`. Always specify a `timeout` value in seconds to prevent your script from hanging indefinitely if GitHub's servers are slow.

```python
import requests

url = "https://api.github.com/users/octocat"
headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "GitHubStatsRetriever/1.0"
}

# Use a 10-second timeout to handle slow networks gracefully
response = requests.get(url, headers=headers, timeout=10)
```

### Step 2: Verify the Status Code
Do not assume the request succeeded. Check the response status code before attempting to read the data:
*   `200 OK`: The request succeeded; data is available.
*   `404 Not Found`: The specified user or repository does not exist.
*   `403 Forbidden`: You exceeded the API rate limit or have invalid credentials.
*   `401 Unauthorized`: Bad credentials/expired token.

```python
if response.status_code == 200:
    # Proceed to extract data
    pass
else:
    # Print error diagnostics
    print(f"Error: Received status code {response.status_code}")
```

### Step 3: Extract and Verify JSON Fields
Start by printing a single field (such as a `name` or `login` key) to verify you have parsed the JSON correctly. Once confirmed, you can extract more complex stats:

```python
data = response.json()

# Use .get() to avoid KeyError if a field is missing from the API response
display_name = data.get("name", "No name provided")
public_repos = data.get("public_repos", 0)

print(f"User: {display_name} has {public_repos} public repositories.")
```

### Step 4: Handle Exceptions
Network requests can fail due to DNS resolution issues, timeout limits, or broken connections. Wrap your API call inside a `try-except` block targeting `requests.exceptions.RequestException`.

```python
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status() # Raises an HTTPError for bad responses (4xx/5xx)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
```

---

## Key API Endpoints Reference

To query different resources, target these endpoint patterns (appended to `https://api.github.com`):

| Target Resource | Endpoint Pattern | Key Fields to Extract |
| :--- | :--- | :--- |
| **User Profile Details** | `/users/{username}` | `login`, `name`, `bio`, `followers`, `public_repos` |
| **User's Repositories** | `/users/{username}/repos` | Array of objects with: `name`, `stargazers_count`, `language`, `description` |
| **Repository Details** | `/repos/{owner}/{repo}` | `name`, `description`, `stargazers_count`, `forks_count`, `license` |
| **Repo Contributors** | `/repos/{owner}/{repo}/contributors` | Array of user objects including: `login`, `contributions` |

---

## Architectural & Design Considerations

When designing your script for modularity and reliability, keep the following considerations in mind:

### 1. Modular Functions vs. Inline Scripts
Instead of putting all request logic in a main function, separate the concerns:
*   Write utility functions like `fetch_user_data(username)` and `fetch_user_repos(username)` that return parsed Python dictionaries/lists.
*   Write formatting functions like `display_results(data)` to handle console output presentation.
*   This structure allows you to reuse the logic elsewhere or import the utility into other scripts.

### 2. Environment Variables for Sensitive Configuration
Avoid hardcoding authentication tokens in your source code. Instead, design your script to read from environment variables:
```python
import os
token = os.environ.get("GITHUB_TOKEN")
```
This keeps your credentials secure and allows you to easily switch tokens between development and production environments.

### 3. Pagination Support
If a user has more than 30 repositories, GitHub will paginate the list. To fetch more repositories, use the `params` option to specify page limits:
*   `per_page`: Number of results to return per page (max 100).
*   `page`: The page number to fetch.
```python
params = {"per_page": 100, "page": 1}
response = requests.get(url, headers=headers, params=params)
```

### 4. Handling Missing Data (Defensive Design)
Not all GitHub users have filled out their biographies or company fields. Use the dict `.get()` method's fallback values (e.g., `data.get("bio") or "N/A"`) to prevent print statements from outputting literal `None` values or throwing formatting errors.
