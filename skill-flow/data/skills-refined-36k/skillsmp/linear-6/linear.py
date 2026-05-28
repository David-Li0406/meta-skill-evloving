#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click",
#     "httpx",
# ]
# ///
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any

import click
import httpx

API_URL = "https://api.linear.app/graphql"


def get_api_key() -> str:
    api_key = os.environ.get("LINEAR_API_KEY")
    if not api_key:
        click.echo("Error: LINEAR_API_KEY environment variable not set", err=True)
        sys.exit(1)
    return api_key


def execute_query(
    query: str, variables: dict[str, Any] | None = None
) -> dict[str, Any]:
    headers = {"Authorization": get_api_key(), "Content-Type": "application/json"}
    payload: dict[str, Any] = {"query": query}
    if variables:
        payload["variables"] = variables

    response = httpx.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()

    if "errors" in result:
        for error in result["errors"]:
            click.echo(f"GraphQL Error: {error.get('message', error)}", err=True)
        sys.exit(1)

    return result["data"]


@click.group()
def cli():
    """Linear CLI - Interact with Linear issues."""


@cli.command("list-issues")
@click.option(
    "--recent",
    "-r",
    type=click.IntRange(1, 60),
    help="Only issues created in last N minutes (max 60)",
)
def list_issues(recent: int | None) -> None:
    """List my assigned issues."""
    filter_clause = ""
    variables: dict[str, Any] | None = None

    if recent:
        created_after = (
            datetime.now(timezone.utc) - timedelta(minutes=recent)
        ).isoformat()
        filter_clause = ", filter: { createdAt: { gte: $createdAfter } }"
        variables = {"createdAfter": created_after}

    # GraphQL requires variable declaration only when variables are used
    var_declaration = "($createdAfter: DateTimeOrDuration!)" if recent else ""
    query = f"""
    query ListMyIssues{var_declaration} {{
        viewer {{
            assignedIssues(first: 50, orderBy: updatedAt{filter_clause}) {{
                nodes {{
                    identifier
                    title
                    state {{ name }}
                }}
            }}
        }}
    }}
    """
    data = execute_query(query, variables)
    issues = data["viewer"]["assignedIssues"]["nodes"]
    if not issues:
        click.echo("No issues found")
        return

    for issue in issues:
        click.echo(f"[{issue['identifier']}] {issue['title']}")


@cli.command("get-issue")
@click.argument("issue_id")
def get_issue(issue_id: str) -> None:
    """Get a specific issue by identifier (e.g., 'ENG-123')."""
    query = """
    query GetIssue($id: String!) {
        issue(id: $id) {
            identifier
            title
            description
            branchName
        }
    }
    """
    data = execute_query(query, {"id": issue_id})

    if not data.get("issue"):
        click.echo(f"Issue '{issue_id}' not found", err=True)
        sys.exit(1)

    issue = data["issue"]
    click.echo(f"DESCRIPTION: {issue.get('description') or 'No description'}")
    click.echo(f"ISSUE_ID: {issue['identifier']} - {issue['title']}")
    click.echo(f"BRANCH_NAME: {issue.get('branchName') or 'N/A'}")


def get_backlog_state_id(team_id: str) -> str:
    query = """
    query TeamStates($teamId: String!) {
        team(id: $teamId) {
            states {
                nodes {
                    id
                    name
                    type
                }
            }
        }
    }
    """
    data = execute_query(query, {"teamId": team_id})
    if not data.get("team"):
        click.echo(f"Team '{team_id}' not found", err=True)
        sys.exit(1)

    states = data["team"]["states"]["nodes"]
    for state in states:
        if state["type"] == "backlog":
            return state["id"]

    click.echo("No Backlog state found for team", err=True)
    sys.exit(1)


@cli.command("create-issue")
@click.option("--team", "-t", required=True, help="Team ID")
@click.option("--project", "-p", help="Project ID (optional)")
@click.option("--title", required=True, help="Issue title")
@click.option("--description", "-d", default="", help="Issue description")
def create_issue(team: str, project: str | None, title: str, description: str) -> None:
    """Create a new issue in backlog."""
    backlog_state_id = get_backlog_state_id(team)

    query = """
    mutation IssueCreate($input: IssueCreateInput!) {
        issueCreate(input: $input) {
            success
            issue {
                identifier
                title
                state { name }
            }
        }
    }
    """
    input_data: dict[str, str] = {
        "title": title,
        "teamId": team,
        "stateId": backlog_state_id,
    }
    if description:
        input_data["description"] = description
    if project:
        input_data["projectId"] = project

    data = execute_query(query, {"input": input_data})

    if not data["issueCreate"]["success"]:
        click.echo("Failed to create issue", err=True)
        sys.exit(1)

    issue = data["issueCreate"]["issue"]
    click.echo(
        f"Created: [{issue['identifier']}] {issue['title']} ({issue['state']['name']})"
    )


@cli.command("list-teams")
def list_teams() -> None:
    """List all teams with their IDs."""
    query = """
    query Teams {
        teams {
            nodes {
                id
                name
                key
            }
        }
    }
    """
    data = execute_query(query)
    teams = data["teams"]["nodes"]

    if not teams:
        click.echo("No teams found")
        return

    for team in teams:
        click.echo(f"{team['name']} ({team['key']}): {team['id']}")


@cli.command("list-projects")
@click.option("--team", "-t", help="Filter by team ID (optional)")
def list_projects(team: str | None) -> None:
    """List all projects with their IDs."""
    if team:
        query = """
        query Projects($teamId: String!) {
            team(id: $teamId) {
                projects {
                    nodes {
                        id
                        name
                    }
                }
            }
        }
        """
        data = execute_query(query, {"teamId": team})
        if not data.get("team"):
            click.echo(f"Team '{team}' not found", err=True)
            sys.exit(1)
        projects = data["team"]["projects"]["nodes"]
    else:
        query = """
        query Projects {
            projects {
                nodes {
                    id
                    name
                }
            }
        }
        """
        data = execute_query(query)
        projects = data["projects"]["nodes"]

    if not projects:
        click.echo("No projects found")
        return

    for proj in projects:
        click.echo(f"{proj['name']}: {proj['id']}")


if __name__ == "__main__":
    cli()
