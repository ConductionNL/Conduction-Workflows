import os
import logging
import requests
import yaml
from typing import List, Dict, Any


logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_repositories_from_yaml(config_path: str) -> List[Dict[str, str]]:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file) or {}
    repositories = config.get("repositories", [])
    if not isinstance(repositories, list):
        raise ValueError("Expected 'repositories' to be a list in repo_config.yaml")
    return repositories


def fetch_open_pull_requests(
    owner: str, repo: str, github_token: str | None
) -> List[Dict[str, Any]]:
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {"Accept": "application/vnd.github+json"}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
    params = {"state": "open", "per_page": 50}
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def post_to_slack(webhook_url: str, text: str) -> None:
    try:
        response = requests.post(webhook_url, json={"text": text}, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logging.error(f"Failed to post to Slack: {exc}")


def build_slack_message(owner: str, repo: str, pulls: List[Dict[str, Any]]) -> str:
    if not pulls:
        return ""
    lines: List[str] = [f"*Open PRs for {owner}/{repo}:*"]
    for pr in pulls:
        title = pr.get("title", "Untitled")
        html_url = pr.get("html_url", "")
        user_login = (pr.get("user") or {}).get("login", "unknown")
        lines.append(f"- {title} by `{user_login}` — {html_url}")
    return "\n".join(lines)


def main() -> None:
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        logging.error("SLACK_WEBHOOK_URL environment variable is not set")
        return

    github_token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    repositories = load_repositories_from_yaml("repo_config.yaml")

    for repo_info in repositories:
        owner = repo_info.get("owner")
        repo = repo_info.get("repo")
        if not owner or not repo:
            logging.error(f"Invalid repository entry: {repo_info}")
            continue
        try:
            pulls = fetch_open_pull_requests(owner, repo, github_token)
        except requests.HTTPError as exc:
            logging.error(f"Failed to fetch PRs for {owner}/{repo}: {exc}")
            continue

        message = build_slack_message(owner, repo, pulls)
        if message:
            post_to_slack(webhook_url, message)


if __name__ == "__main__":
    main()
