#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "gql[all]>=3.5.0",
#     "snakemd>=2.0.0",
# ]
# ///
"""
Summarize a GitHub PR with file changes and unresolved comments.

Usage:
    ./summarize-pr.py OWNER REPO PR_NUMBER

Example:
    ./summarize-pr.py ansible handbook 744
"""

import json
import os
import subprocess
import sys
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from snakemd import new_doc, Paragraph, Inline


GRAPHQL_QUERY = gql(
    """
query($owner: String!, $repo: String!, $number: Int!, $filesCursor: String, $threadsCursor: String, $commentsCursor: String, $reviewsCursor: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      title
      number
      url
      author {
        login
      }
      baseRefName
      headRefName
      state
      additions
      deletions
      changedFiles
      body
      files(first: 100, after: $filesCursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          path
          additions
          deletions
        }
      }
      comments(first: 100, after: $commentsCursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          author {
            login
          }
          body
          createdAt
        }
      }
      reviews(first: 100, after: $reviewsCursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          author {
            login
          }
          state
          body
          submittedAt
        }
      }
      reviewThreads(first: 100, after: $threadsCursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          isResolved
          isOutdated
          resolvedBy {
            login
          }
          comments(first: 100) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              id
              databaseId
              author {
                login
              }
              body
              diffHunk
              path
              line
              createdAt
            }
          }
        }
      }
    }
  }
}
"""
)

COMMENTS_PAGINATION_QUERY = gql(
    """
query($owner: String!, $repo: String!, $number: Int!, $threadsCursor: String!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $threadsCursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        nodes {
          id
          comments(first: 100) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              id
              databaseId
              author {
                login
              }
              body
              diffHunk
              path
              line
              createdAt
            }
          }
        }
      }
    }
  }
}
"""
)


def get_github_token() -> str:
    """Get GitHub token from environment or gh CLI config."""
    # Try environment variable first
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token

    # Fall back to gh CLI config
    try:
        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        raise ValueError(
            "No GitHub token found. Please set GITHUB_TOKEN or GH_TOKEN environment variable, "
            "or authenticate with 'gh auth login'"
        )


def paginate_comments(
    client: Client,
    owner: str,
    repo: str,
    pr_number: int,
    thread_id: str,
    initial_comments: dict,
) -> list[dict]:
    """Paginate through all comments in a review thread if needed."""
    all_comments = list(initial_comments["nodes"])
    page_info = initial_comments["pageInfo"]

    # Note: GitHub GraphQL API doesn't support paginating comments within a thread directly
    # The first: 100 limit should be sufficient for most threads
    # If a thread has >100 comments, we'd need a different query structure
    if page_info.get("hasNextPage"):
        print(
            f"Warning: Thread has >100 comments, some may be truncated", file=sys.stderr
        )

    return all_comments


def get_pr_data(owner: str, repo: str, pr_number: int) -> dict:
    """Fetch PR data from GitHub GraphQL API with pagination."""
    token = get_github_token()

    transport = RequestsHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"bearer {token}"},
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    # Initial query
    variables = {
        "owner": owner,
        "repo": repo,
        "number": pr_number,
        "filesCursor": None,
        "threadsCursor": None,
        "commentsCursor": None,
        "reviewsCursor": None,
    }

    result = client.execute(GRAPHQL_QUERY, variable_values=variables)
    pr_data = result["repository"]["pullRequest"]

    # Paginate files if needed
    all_files = list(pr_data["files"]["nodes"])
    files_page_info = pr_data["files"]["pageInfo"]

    while files_page_info["hasNextPage"]:
        variables["filesCursor"] = files_page_info["endCursor"]
        result = client.execute(GRAPHQL_QUERY, variable_values=variables)
        page_data = result["repository"]["pullRequest"]["files"]
        all_files.extend(page_data["nodes"])
        files_page_info = page_data["pageInfo"]

    pr_data["files"]["nodes"] = all_files

    # Paginate general comments if needed
    all_comments = list(pr_data["comments"]["nodes"])
    comments_page_info = pr_data["comments"]["pageInfo"]

    while comments_page_info["hasNextPage"]:
        variables["commentsCursor"] = comments_page_info["endCursor"]
        variables["filesCursor"] = None  # Don't re-fetch files
        result = client.execute(GRAPHQL_QUERY, variable_values=variables)
        page_data = result["repository"]["pullRequest"]["comments"]
        all_comments.extend(page_data["nodes"])
        comments_page_info = page_data["pageInfo"]

    pr_data["comments"]["nodes"] = all_comments

    # Paginate reviews if needed
    all_reviews = list(pr_data["reviews"]["nodes"])
    reviews_page_info = pr_data["reviews"]["pageInfo"]

    while reviews_page_info["hasNextPage"]:
        variables["reviewsCursor"] = reviews_page_info["endCursor"]
        variables["filesCursor"] = None  # Don't re-fetch files
        variables["commentsCursor"] = None  # Don't re-fetch comments
        result = client.execute(GRAPHQL_QUERY, variable_values=variables)
        page_data = result["repository"]["pullRequest"]["reviews"]
        all_reviews.extend(page_data["nodes"])
        reviews_page_info = page_data["pageInfo"]

    pr_data["reviews"]["nodes"] = all_reviews

    # Paginate review threads if needed
    all_threads = list(pr_data["reviewThreads"]["nodes"])
    threads_page_info = pr_data["reviewThreads"]["pageInfo"]

    while threads_page_info["hasNextPage"]:
        variables["threadsCursor"] = threads_page_info["endCursor"]
        variables["filesCursor"] = None  # Don't re-fetch files
        variables["commentsCursor"] = None  # Don't re-fetch comments
        variables["reviewsCursor"] = None  # Don't re-fetch reviews
        result = client.execute(GRAPHQL_QUERY, variable_values=variables)
        page_data = result["repository"]["pullRequest"]["reviewThreads"]
        all_threads.extend(page_data["nodes"])
        threads_page_info = page_data["pageInfo"]

    pr_data["reviewThreads"]["nodes"] = all_threads

    return pr_data


def extract_unresolved_threads(pr_data: dict) -> list[dict]:
    """Extract unresolved review threads."""
    threads = pr_data["reviewThreads"]["nodes"]
    unresolved = []

    for thread in threads:
        if not thread["isResolved"]:
            first_comment = thread["comments"]["nodes"][0]
            preview = first_comment["body"].split("\n")[0][:120]

            unresolved.append(
                {
                    "threadId": thread["id"],
                    "isResolved": thread["isResolved"],
                    "isOutdated": thread["isOutdated"],
                    "author": first_comment["author"]["login"],
                    "line": first_comment["line"],
                    "path": first_comment["path"],
                    "preview": preview,
                    "commentCount": len(thread["comments"]["nodes"]),
                    "allComments": thread["comments"]["nodes"],
                }
            )

    return unresolved


def generate_markdown_summary(pr_data: dict, unresolved_threads: list[dict]) -> str:
    """Generate markdown summary of the PR using SnakeMD."""
    doc = new_doc()

    # Header
    doc.add_heading(f"PR #{pr_data['number']}: {pr_data['title']}", level=1)

    # URL
    p = Paragraph([Inline("URL", bold=True), f": {pr_data['url']}"])
    doc.add_block(p)

    # Author
    p = Paragraph([Inline("Author", bold=True), f": @{pr_data['author']['login']}"])
    doc.add_block(p)

    # Status
    p = Paragraph([Inline("Status", bold=True), f": {pr_data['state']}"])
    doc.add_block(p)

    # Branch
    p = Paragraph(
        [
            Inline("Branch", bold=True),
            ": ",
            Inline(pr_data["headRefName"], code=True),
            " → ",
            Inline(pr_data["baseRefName"], code=True),
        ]
    )
    doc.add_block(p)

    # Stats
    doc.add_heading("Summary", level=2)

    p1 = Paragraph([Inline("Files changed", bold=True), f": {pr_data['changedFiles']}"])
    p2 = Paragraph([Inline("Additions", bold=True), f": +{pr_data['additions']}"])
    p3 = Paragraph([Inline("Deletions", bold=True), f": -{pr_data['deletions']}"])
    p4 = Paragraph(
        [
            Inline("General comments", bold=True),
            f": {len(pr_data['comments']['nodes'])}",
        ]
    )
    p5 = Paragraph(
        [
            Inline("Unresolved review comments", bold=True),
            f": {len(unresolved_threads)}",
        ]
    )
    doc.add_unordered_list([p1, p2, p3, p4, p5])

    # Description
    if pr_data.get("body"):
        doc.add_heading("Description", level=2)
        # Use raw to preserve formatting from the PR body
        doc.add_raw(pr_data["body"])

    # File changes
    doc.add_heading("Files Changed", level=2)
    if pr_data["files"]["nodes"]:
        file_list = [
            Paragraph(
                [
                    Inline(file["path"], code=True),
                    f" (+{file['additions']} -{file['deletions']})",
                ]
            )
            for file in pr_data["files"]["nodes"]
        ]
        doc.add_unordered_list(file_list)
    else:
        doc.add_paragraph("*No file changes found*")

    # Combine all comments chronologically
    all_timeline_items = []

    # Add general comments
    for comment in pr_data["comments"]["nodes"]:
        all_timeline_items.append(
            {
                "type": "comment",
                "timestamp": comment["createdAt"],
                "author": comment["author"]["login"],
                "body": comment["body"],
            }
        )

    # Add reviews with top-level comments
    for review in pr_data["reviews"]["nodes"]:
        if review.get("body"):
            all_timeline_items.append(
                {
                    "type": "review",
                    "timestamp": review["submittedAt"],
                    "author": review["author"]["login"],
                    "body": review["body"],
                    "state": review["state"],
                }
            )

    # Sort chronologically
    all_timeline_items.sort(key=lambda x: x["timestamp"])

    # Display all comments chronologically
    if all_timeline_items:
        doc.add_heading("Discussion & Reviews", level=2)
        for item in all_timeline_items:
            if item["type"] == "comment":
                p = Paragraph(
                    [
                        Inline(f"@{item['author']}", bold=True),
                        f" ({item['timestamp']}):",
                    ]
                )
                doc.add_block(p)
            else:  # review
                # Map state to emoji/label
                state_label = {
                    "APPROVED": "✅ APPROVED",
                    "CHANGES_REQUESTED": "🔴 CHANGES REQUESTED",
                    "COMMENTED": "💬 COMMENTED",
                    "DISMISSED": "❌ DISMISSED",
                    "PENDING": "⏳ PENDING",
                }.get(item["state"], item["state"])

                p = Paragraph(
                    [
                        Inline(f"@{item['author']}", bold=True),
                        f" ({item['timestamp']}) - {state_label}:",
                    ]
                )
                doc.add_block(p)

            doc.add_raw(item["body"])
            doc.add_horizontal_rule()

    # Unresolved comments
    doc.add_heading("Unresolved Review Comments", level=2)

    if unresolved_threads:
        for i, thread in enumerate(unresolved_threads, 1):
            doc.add_heading(f"{i}. Comment by @{thread['author']}", level=3)

            # Location and status
            if thread["path"]:
                location_parts = [
                    Inline("Location", bold=True),
                    ": ",
                    Inline(thread["path"], code=True),
                ]
                if thread["line"]:
                    location_parts.append(f" (line {thread['line']})")
                p = Paragraph(location_parts)
                doc.add_block(p)

            p = Paragraph(
                [
                    Inline("Status", bold=True),
                    f": {'Outdated' if thread['isOutdated'] else 'Current'}",
                ]
            )
            doc.add_block(p)

            # All comments in thread
            for idx, comment in enumerate(thread["allComments"]):
                p = Paragraph(
                    [
                        Inline(f"@{comment['author']['login']}", bold=True),
                        f" ({comment['createdAt']}):",
                    ]
                )
                doc.add_block(p)

                # Show diff hunk for the first comment if available
                if idx == 0 and comment.get("diffHunk"):
                    p = Paragraph([Inline("Code context:", bold=True)])
                    doc.add_block(p)
                    doc.add_code(comment["diffHunk"], lang="diff")

                doc.add_raw(comment["body"])
                doc.add_horizontal_rule()
    else:
        doc.add_paragraph("*No unresolved comments*")

    return str(doc)


def main():
    if len(sys.argv) != 4:
        print("Usage: summarize-pr.py OWNER REPO PR_NUMBER", file=sys.stderr)
        sys.exit(1)

    owner = sys.argv[1]
    repo = sys.argv[2]
    pr_number = int(sys.argv[3])

    try:
        pr_data = get_pr_data(owner, repo, pr_number)
        unresolved_threads = extract_unresolved_threads(pr_data)

        markdown = generate_markdown_summary(pr_data, unresolved_threads)
        print(markdown)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
