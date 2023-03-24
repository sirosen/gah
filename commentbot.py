#!/usr/bin/env python
import os
import sys

import requests


def get_pr_url():
    repo = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PR_NUMBER"]
    return f"https://api.github.com/repos/{repo}/pulls/{pr_number}"


def get_token():
    return os.environ["GITHUB_TOKEN"]


def get_pr_body(pr_url, token):
    r = requests.get(
        pr_url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    return r.json()["body"]


def update_pr(pr_url, token, new_body):
    requests.patch(
        pr_url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        json={"body": new_body},
    )


def updated_body_or_none(old_body, message):
    if old_body is None:
        return message
    if message in old_body:
        return None
    return f"""\
{old_body}

---

{message}"""


def main():
    message = sys.argv[1]
    token = get_token()
    pr_url = get_pr_url()
    old_pr_body = get_pr_body(pr_url, token)

    updated_body = updated_body_or_none(old_pr_body, message)
    if updated_body is not None:
        update_pr(pr_url, token, updated_body)


if __name__ == "__main__":
    main()
