"""Jira skill for read-only Jira integration.

This skill provides tools for querying Jira issues, sprints, projects, and users
via the REST API. All operations are READ-ONLY - no create, update, delete,
or transition operations are available.

Environment Variables:
    JIRA_URL: Jira instance URL (e.g., https://your-instance.atlassian.net)
    JIRA_USERNAME: Username or email
    JIRA_API_TOKEN: API token (Cloud) or password (Server)
    JIRA_API_VERSION: "2" (default) or "3"
"""
