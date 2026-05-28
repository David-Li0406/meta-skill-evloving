#!/usr/bin/env python3
"""Generate work-items from unresolved PR conversations.

This script fetches unresolved PR review conversations and automatically creates
work-items (GitHub issues or Azure DevOps work-items) for each conversation.

The workflow pattern is:
1. Claude fetches unresolved PR conversations
2. Claude creates one work-item per conversation in the tracker
3. User approves PR in web portal (conversations remain as work-items)
4. Claude creates feature worktrees to fix each work-item
5. Repeat until no unresolved conversations

Constants:
- GITHUB_GRAPHQL_TEMPLATE: GraphQL query for fetching GitHub review threads
  Rationale: GitHub requires GraphQL for isResolved status (not available in REST API)
- WORK_ITEM_SLUG_PATTERN: pr-<pr-number>-issue-<sequence>
  Rationale: Sequential numbering, PR-scoped, sortable, compatible with worktree naming
"""

import json
import subprocess
import sys
from pathlib import Path

# Add VCS module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"))
from vcs import get_vcs_adapter
from vcs.azure_adapter import AzureDevOpsAdapter
from vcs.github_adapter import GitHubAdapter

# Constants with documented rationale
GITHUB_GRAPHQL_TEMPLATE = """
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      url
      title
      reviewDecision
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          isCollapsed
          comments(first: 100) {
            nodes {
              id
              author {
                login
              }
              body
              url
              createdAt
              path
              line
            }
          }
        }
      }
    }
  }
}
"""

WORK_ITEM_SLUG_PATTERN = "pr-{pr_number}-issue-{sequence}"  # e.g., pr-94-issue-1


class PRFeedbackWorkItemGenerator:
    """Generate work-items from unresolved PR conversations."""

    def __init__(self, adapter):
        """Initialize generator with VCS adapter.

        Args:
            adapter: VCS adapter instance (GitHub or Azure DevOps)
        """
        self.adapter = adapter
        self.provider_name = adapter.get_provider_name()

    def fetch_unresolved_conversations(self, pr_number: int) -> list[dict]:
        """Fetch unresolved PR conversations.

        Args:
            pr_number: Pull request number

        Returns:
            List of conversation dictionaries with keys:
                - id: Conversation ID (str for GitHub, int for Azure)
                - url: Direct link to conversation
                - file: File path (if file comment, None otherwise)
                - line: Line number (if line comment, None otherwise)
                - author: Comment author username/display name
                - body: First comment body text
                - created_at: Timestamp string

        Raises:
            RuntimeError: If fetching conversations fails
        """
        if isinstance(self.adapter, GitHubAdapter):
            return self._fetch_github_conversations(pr_number)
        elif isinstance(self.adapter, AzureDevOpsAdapter):
            return self._fetch_azure_conversations(pr_number)
        else:
            raise RuntimeError(f"Unsupported VCS adapter: {type(self.adapter)}")

    def _fetch_github_conversations(self, pr_number: int) -> list[dict]:
        """Fetch unresolved GitHub PR review threads.

        Uses GitHub GraphQL API to fetch reviewThreads with isResolved status.

        Args:
            pr_number: Pull request number

        Returns:
            List of conversation dictionaries

        Raises:
            RuntimeError: If GraphQL query fails
        """
        # Get repository owner and name from git remote
        try:
            remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], text=True, stderr=subprocess.PIPE).strip()

            # Parse GitHub URL (supports both HTTPS and SSH formats)
            # HTTPS: https://github.com/owner/repo.git
            # SSH: git@github.com:owner/repo.git
            if remote_url.startswith("https://"):
                parts = remote_url.replace("https://github.com/", "").replace(".git", "").split("/")
            elif remote_url.startswith("git@"):
                parts = remote_url.replace("git@github.com:", "").replace(".git", "").split("/")
            else:
                raise ValueError(f"Unsupported remote URL format: {remote_url}")

            owner, repo = parts[0], parts[1]

        except (subprocess.CalledProcessError, IndexError, ValueError) as e:
            raise RuntimeError(f"Failed to parse GitHub repository from git remote: {e}")

        # Execute GraphQL query
        try:
            result = subprocess.check_output(
                ["gh", "api", "graphql", "-f", f"query={GITHUB_GRAPHQL_TEMPLATE}", "-f", f"owner={owner}", "-f", f"repo={repo}", "-F", f"pr={pr_number}"],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            data = json.loads(result)

        except FileNotFoundError:
            raise RuntimeError("'gh' CLI not found. Install from https://cli.github.com/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to fetch GitHub PR conversations.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while fetching GitHub PR conversations")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse GitHub GraphQL response: {e}")

        # Parse response and extract unresolved threads
        try:
            pr_data = data["data"]["repository"]["pullRequest"]
            review_threads = pr_data["reviewThreads"]["nodes"]

            conversations = []
            for thread in review_threads:
                # Filter: only unresolved threads
                if thread["isResolved"]:
                    continue

                # Get first comment in thread
                if not thread["comments"]["nodes"]:
                    continue  # Skip empty threads

                first_comment = thread["comments"]["nodes"][0]

                conversations.append(
                    {
                        "id": thread["id"],
                        "url": first_comment.get("url", f"{pr_data['url']}#discussion_{thread['id']}"),
                        "file": first_comment.get("path"),
                        "line": first_comment.get("line"),
                        "author": first_comment["author"]["login"] if first_comment.get("author") else "Unknown",
                        "body": first_comment["body"],
                        "created_at": first_comment["createdAt"],
                    }
                )

            return conversations

        except (KeyError, TypeError) as e:
            raise RuntimeError(f"Failed to parse GitHub review threads: {e}")

    def _fetch_azure_conversations(self, pr_number: int) -> list[dict]:
        """Fetch unresolved Azure DevOps PR threads.

        Uses Azure CLI to fetch PR threads with status "active" or "pending".

        Args:
            pr_number: Pull request ID

        Returns:
            List of conversation dictionaries

        Raises:
            RuntimeError: If Azure CLI query fails
        """
        try:
            result = subprocess.check_output(
                ["az", "repos", "pr", "show", "--id", str(pr_number), "--organization", self.adapter.organization, "--query", "threads", "--output", "json"],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30,
            )
            threads = json.loads(result)

        except FileNotFoundError:
            raise RuntimeError("'az' CLI not found. Install from https://learn.microsoft.com/cli/azure/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to fetch Azure DevOps PR threads.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while fetching Azure DevOps PR threads")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse Azure DevOps response: {e}")

        # Parse threads and extract unresolved ones
        conversations = []
        for thread in threads:
            # Filter: only active or pending status (unresolved)
            status = thread.get("status", "unknown").lower()
            if status not in ["active", "pending"]:
                continue

            # Get first comment in thread
            if not thread.get("comments"):
                continue  # Skip empty threads

            first_comment = thread["comments"][0]

            # Extract file path and line number from threadContext
            file_path = None
            line_number = None
            if thread.get("threadContext"):
                file_path = thread["threadContext"].get("filePath")
                if thread["threadContext"].get("rightFileStart"):
                    line_number = thread["threadContext"]["rightFileStart"].get("line")

            conversations.append(
                {
                    "id": thread["id"],
                    "url": f"https://dev.azure.com/{self.adapter.organization}/{self.adapter.project}/_git/{self.adapter.repository}/pullrequest/{pr_number}?_a=files&discussionId={thread['id']}",
                    "file": file_path,
                    "line": line_number,
                    "author": first_comment["author"]["displayName"] if first_comment.get("author") else "Unknown",
                    "body": first_comment.get("content", ""),
                    "created_at": first_comment.get("publishedDate", ""),
                }
            )

        return conversations

    def create_work_item_from_conversation(self, pr_number: int, conversation: dict, sequence: int) -> tuple[str, str]:
        """Create work-item from conversation.

        Args:
            pr_number: Pull request number
            conversation: Conversation dictionary from fetch_unresolved_conversations
            sequence: Work-item sequence number (1, 2, 3, ...)

        Returns:
            Tuple of (work_item_url, work_item_slug)

        Raises:
            RuntimeError: If work-item creation fails
        """
        if isinstance(self.adapter, GitHubAdapter):
            return self._create_github_issue(pr_number, conversation, sequence)
        elif isinstance(self.adapter, AzureDevOpsAdapter):
            return self._create_azure_work_item(pr_number, conversation, sequence)
        else:
            raise RuntimeError(f"Unsupported VCS adapter: {type(self.adapter)}")

    def _create_github_issue(self, pr_number: int, conversation: dict, sequence: int) -> tuple[str, str]:
        """Create GitHub issue from conversation.

        Args:
            pr_number: Pull request number
            conversation: Conversation dictionary
            sequence: Work-item sequence number

        Returns:
            Tuple of (issue_url, issue_slug)

        Raises:
            RuntimeError: If issue creation fails
        """
        # Generate slug
        slug = WORK_ITEM_SLUG_PATTERN.format(pr_number=pr_number, sequence=sequence)

        # Generate title (first 50 chars of comment body)
        comment_preview = conversation["body"][:50]
        if len(conversation["body"]) > 50:
            comment_preview += "..."
        title = f"PR #{pr_number} feedback: {comment_preview}"

        # Generate body with conversation context
        body_parts = [
            f"**From PR:** #{pr_number}",
            f"**Conversation:** {conversation['url']}",
        ]

        if conversation.get("file"):
            location = conversation["file"]
            if conversation.get("line"):
                location += f":{conversation['line']}"
            body_parts.append(f"**Location:** {location}")

        body_parts.append(f"**Author:** {conversation['author']}")
        body_parts.append("")  # Blank line
        body_parts.append(conversation["body"])
        body_parts.append("")  # Blank line
        body_parts.append("---")
        body_parts.append(f"Related to PR #{pr_number}")

        body = "\n".join(body_parts)

        # Create issue (try with labels first, fall back to no labels if they don't exist)
        pr_label = f"pr-{pr_number}"
        try:
            issue_url = subprocess.check_output(
                ["gh", "issue", "create", "--title", title, "--body", body, "--label", "pr-feedback", "--label", pr_label, "--assignee", "@me"],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30,
            ).strip()

            return (issue_url, slug)

        except FileNotFoundError:
            raise RuntimeError("'gh' CLI not found. Install from https://cli.github.com/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)

            # If labels don't exist, retry without labels
            if "not found" in error_msg.lower() and "label" in error_msg.lower():
                print("    ⚠️  Labels not found, creating issue without labels...")
                try:
                    issue_url = subprocess.check_output(
                        ["gh", "issue", "create", "--title", title, "--body", body, "--assignee", "@me"], text=True, stderr=subprocess.PIPE, timeout=30
                    ).strip()

                    return (issue_url, slug)
                except subprocess.CalledProcessError as retry_error:
                    retry_msg = retry_error.stderr.strip() if retry_error.stderr else str(retry_error)
                    raise RuntimeError(f"Failed to create GitHub issue.\nError: {retry_msg}")
            else:
                raise RuntimeError(f"Failed to create GitHub issue.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while creating GitHub issue")

    def _create_azure_work_item(self, pr_number: int, conversation: dict, sequence: int) -> tuple[str, str]:
        """Create Azure DevOps work-item from conversation.

        Args:
            pr_number: Pull request ID
            conversation: Conversation dictionary
            sequence: Work-item sequence number

        Returns:
            Tuple of (work_item_url, work_item_slug)

        Raises:
            RuntimeError: If work-item creation fails
        """
        # Generate slug
        slug = WORK_ITEM_SLUG_PATTERN.format(pr_number=pr_number, sequence=sequence)

        # Generate title (first 50 chars of comment body)
        comment_preview = conversation["body"][:50]
        if len(conversation["body"]) > 50:
            comment_preview += "..."
        title = f"PR #{pr_number} feedback: {comment_preview}"

        # Generate description with conversation context
        description_parts = [
            f"<b>From PR:</b> #{pr_number}<br/>",
            f"<b>Thread ID:</b> {conversation['id']}<br/>",
        ]

        if conversation.get("file"):
            location = conversation["file"]
            if conversation.get("line"):
                location += f":{conversation['line']}"
            description_parts.append(f"<b>Location:</b> {location}<br/>")

        description_parts.append(f"<b>Author:</b> {conversation['author']}<br/>")
        description_parts.append("<br/>")  # Blank line
        description_parts.append(conversation["body"].replace("\n", "<br/>"))

        description = "".join(description_parts)

        # Create work-item
        try:
            result = subprocess.check_output(
                [
                    "az",
                    "boards",
                    "work-item",
                    "create",
                    "--title",
                    title,
                    "--type",
                    "Task",
                    "--description",
                    description,
                    "--assigned-to",
                    "@me",
                    "--organization",
                    self.adapter.organization,
                    "--project",
                    self.adapter.project,
                    "--fields",
                    "System.Tags=pr-feedback",
                    "--output",
                    "json",
                ],
                text=True,
                stderr=subprocess.PIPE,
                timeout=30,
            )

            work_item = json.loads(result)
            work_item_url = work_item["url"]

            return (work_item_url, slug)

        except FileNotFoundError:
            raise RuntimeError("'az' CLI not found. Install from https://learn.microsoft.com/cli/azure/")
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.strip() if e.stderr else str(e)
            raise RuntimeError(f"Failed to create Azure DevOps work-item.\nError: {error_msg}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout while creating Azure DevOps work-item")
        except (json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Failed to parse Azure DevOps work-item response: {e}")

    def display_conversations(self, conversations: list[dict]) -> None:
        """Display unresolved conversations grouped by file.

        Args:
            conversations: List of conversation dictionaries
        """
        if not conversations:
            print("\n✓ No unresolved conversations found!")
            return

        print("\n" + "=" * 80)
        print(f"UNRESOLVED PR CONVERSATIONS ({len(conversations)} total)")
        print("=" * 80)

        # Group by file
        file_groups = {}
        general_conversations = []

        for conv in conversations:
            if conv.get("file"):
                file_path = conv["file"]
                if file_path not in file_groups:
                    file_groups[file_path] = []
                file_groups[file_path].append(conv)
            else:
                general_conversations.append(conv)

        # Display general conversations
        if general_conversations:
            print("\n📌 GENERAL COMMENTS")
            print("-" * 80)
            for i, conv in enumerate(general_conversations, 1):
                print(f"\n[{i}] {conv['author']} wrote:")
                print(f"    {conv['body'][:100]}{'...' if len(conv['body']) > 100 else ''}")
                print(f"    🔗 {conv['url']}")

        # Display file-specific conversations
        if file_groups:
            print("\n📄 FILE-SPECIFIC COMMENTS")
            print("-" * 80)
            for file_path, file_convs in sorted(file_groups.items()):
                print(f"\n  {file_path}")
                for conv in file_convs:
                    line_info = f" (line {conv['line']})" if conv.get("line") else ""
                    print(f"    • {conv['author']}{line_info}:")
                    print(f"      {conv['body'][:100]}{'...' if len(conv['body']) > 100 else ''}")
                    print(f"      🔗 {conv['url']}")

        print("\n" + "=" * 80 + "\n")


def generate_work_items_from_pr(pr_number: int, dry_run: bool = False) -> int:
    """Generate work-items from unresolved PR conversations.

    Args:
        pr_number: Pull request number
        dry_run: If True, only display conversations without creating work-items

    Returns:
        0 on success, 1 on failure

    Raises:
        ValueError: If pr_number is invalid
    """
    # Input validation
    if not isinstance(pr_number, int) or pr_number <= 0:
        raise ValueError(f"Invalid PR number: {pr_number}. Must be a positive integer.")

    # Get VCS adapter
    try:
        adapter = get_vcs_adapter()
    except Exception as e:
        print(f"ERROR: Failed to get VCS adapter: {e}", file=sys.stderr)
        print("Make sure you're in a git repository with a configured remote.")
        return 1

    generator = PRFeedbackWorkItemGenerator(adapter)
    print(f"\n🔧 Using {generator.provider_name} adapter\n")

    # Fetch unresolved conversations
    print(f"🔍 Fetching unresolved conversations from PR #{pr_number}...")
    try:
        conversations = generator.fetch_unresolved_conversations(pr_number)
    except RuntimeError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        return 1

    # Display conversations
    generator.display_conversations(conversations)

    if not conversations:
        return 0  # Success - no work-items to create

    if dry_run:
        print("ℹ️  Dry run mode - no work-items created")
        print(f"Would create {len(conversations)} work-items with slugs:")
        for i in range(len(conversations)):
            slug = WORK_ITEM_SLUG_PATTERN.format(pr_number=pr_number, sequence=i + 1)
            print(f"  - {slug}")
        return 0

    # Create work-items
    print("🔨 Creating work-items...")
    created_work_items = []

    for i, conversation in enumerate(conversations, 1):
        try:
            work_item_url, work_item_slug = generator.create_work_item_from_conversation(pr_number, conversation, i)
            created_work_items.append((work_item_url, work_item_slug))
            print(f"  ✓ Created {work_item_slug}: {work_item_url}")

        except RuntimeError as e:
            print(f"\n  ✗ Failed to create work-item {i}: {e}", file=sys.stderr)
            print(f"    Stopping after {len(created_work_items)} successful work-items.")
            break

    # Summary
    print("\n" + "=" * 80)
    print("✅ WORK-ITEM GENERATION COMPLETE")
    print("=" * 80)
    print(f"\nCreated {len(created_work_items)} work-items from {len(conversations)} conversations:")
    for url, slug in created_work_items:
        print(f"  • {slug}")
        print(f"    {url}")

    print("\n📋 Next steps:")
    print(f"  1. Review and approve PR #{pr_number} in web portal")
    print("  2. For each work-item, create feature worktree:")
    for _, slug in created_work_items:
        print(f"     python .claude/skills/git-workflow-manager/scripts/create_worktree.py feature {slug} contrib/<user>")
    print("  3. Implement fixes and create PRs for each work-item")
    print("  4. Repeat until no unresolved conversations\n")

    return 0


def main():
    """Main entry point for script."""
    if len(sys.argv) < 2:
        print("Usage: python generate_work_items_from_pr.py <pr-number> [--dry-run]", file=sys.stderr)
        print("\nExamples:")
        print("  python generate_work_items_from_pr.py 94")
        print("  python generate_work_items_from_pr.py 94 --dry-run")
        sys.exit(1)

    try:
        pr_number = int(sys.argv[1])
    except ValueError:
        print(f"ERROR: Invalid PR number '{sys.argv[1]}'. Must be an integer.", file=sys.stderr)
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv

    try:
        exit_code = generate_work_items_from_pr(pr_number, dry_run)
        sys.exit(exit_code)
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
