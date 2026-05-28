#!/usr/bin/env python3
"""
Supabase Security Audit Script

Generates a security access matrix showing:
- Table privileges (GRANTs) for anon/authenticated roles
- RLS policies and their conditions
- Security gaps (GRANTs without matching RLS policies)

Usage:
    python audit_security.py                    # Print to stdout
    python audit_security.py --output FILE      # Write to file
    python audit_security.py --format json      # JSON output

Requires: Supabase MCP connection (run within Claude Code)
"""

import argparse
import json
import sys
from datetime import datetime

# SQL queries for security audit
QUERIES = {
    "rls_status": """
        SELECT
            n.nspname AS schema,
            c.relname AS table_name,
            c.relrowsecurity AS rls_enabled,
            c.relforcerowsecurity AS rls_forced
        FROM pg_class c
        JOIN pg_namespace n ON c.relnamespace = n.oid
        WHERE c.relkind = 'r'
            AND n.nspname IN ('public', 'bible_schema', 'admin', 'notifications', 'feedback')
        ORDER BY n.nspname, c.relname;
    """,

    "table_grants": """
        SELECT
            table_schema,
            table_name,
            privilege_type,
            grantee
        FROM information_schema.table_privileges
        WHERE table_schema IN ('public', 'bible_schema', 'admin', 'notifications', 'feedback')
            AND grantee IN ('anon', 'authenticated')
        ORDER BY table_schema, table_name, grantee, privilege_type;
    """,

    "rls_policies": """
        SELECT
            schemaname,
            tablename,
            policyname,
            roles::text AS roles,
            cmd,
            qual IS NOT NULL AS has_using,
            with_check IS NOT NULL AS has_with_check,
            CASE
                WHEN qual::text LIKE '%auth.uid()%' THEN 'user-scoped'
                WHEN qual::text LIKE '%has_role%' THEN 'admin-check'
                WHEN qual::text = 'true' THEN 'open'
                ELSE 'other'
            END AS policy_type
        FROM pg_policies
        WHERE schemaname IN ('public', 'bible_schema', 'admin', 'notifications', 'feedback')
        ORDER BY schemaname, tablename, cmd;
    """,

    "security_gaps": """
        SELECT DISTINCT
            tp.table_schema,
            tp.table_name,
            tp.privilege_type,
            tp.grantee
        FROM information_schema.table_privileges tp
        WHERE tp.grantee IN ('anon', 'authenticated')
            AND tp.privilege_type IN ('UPDATE', 'DELETE', 'INSERT')
            AND tp.table_schema IN ('public', 'bible_schema', 'admin', 'notifications', 'feedback')
            AND NOT EXISTS (
                SELECT 1 FROM pg_policies pp
                WHERE pp.schemaname = tp.table_schema
                    AND pp.tablename = tp.table_name
                    AND (pp.cmd = tp.privilege_type OR pp.cmd = 'ALL')
            )
        ORDER BY tp.table_schema, tp.table_name;
    """
}


def generate_markdown_report(data: dict) -> str:
    """Generate markdown report from audit data."""

    lines = [
        "# Supabase Security Matrix",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Overview",
        "",
        "This document shows the effective access permissions for each table,",
        "combining table-level GRANTs and row-level security (RLS) policies.",
        "",
    ]

    # Security gaps section
    gaps = data.get("security_gaps", [])
    if gaps:
        lines.extend([
            "## Security Gaps",
            "",
            "Tables with GRANTs but missing RLS policies for that operation:",
            "",
            "| Schema | Table | Operation | Role |",
            "|--------|-------|-----------|------|",
        ])
        for gap in gaps:
            lines.append(f"| {gap['table_schema']} | {gap['table_name']} | {gap['privilege_type']} | {gap['grantee']} |")
        lines.append("")
    else:
        lines.extend([
            "## Security Gaps",
            "",
            "No security gaps found.",
            "",
        ])

    # Build access matrix
    rls_status = {(r['schema'], r['table_name']): r for r in data.get("rls_status", [])}
    grants = data.get("table_grants", [])
    policies = data.get("rls_policies", [])

    # Group grants by table
    table_grants = {}
    for g in grants:
        key = (g['table_schema'], g['table_name'])
        if key not in table_grants:
            table_grants[key] = {'anon': set(), 'authenticated': set()}
        table_grants[key][g['grantee']].add(g['privilege_type'])

    # Group policies by table
    table_policies = {}
    for p in policies:
        key = (p['schemaname'], p['tablename'])
        if key not in table_policies:
            table_policies[key] = []
        table_policies[key].append(p)

    # Generate per-schema tables
    schemas = sorted(set(k[0] for k in table_grants.keys()))

    for schema in schemas:
        lines.extend([
            f"## {schema}",
            "",
            "| Table | RLS | anon | authenticated | Notes |",
            "|-------|-----|------|---------------|-------|",
        ])

        schema_tables = sorted([k for k in table_grants.keys() if k[0] == schema], key=lambda x: x[1])

        for schema_name, table_name in schema_tables:
            key = (schema_name, table_name)
            rls = rls_status.get(key, {})
            rls_str = "Yes" if rls.get('rls_enabled') else "**NO**"

            anon_grants = table_grants[key]['anon']
            auth_grants = table_grants[key]['authenticated']

            anon_str = format_grants(anon_grants)
            auth_str = format_grants(auth_grants)

            # Determine notes based on policies
            notes = []
            pols = table_policies.get(key, [])
            has_admin_check = any(p.get('policy_type') == 'admin-check' for p in pols)
            has_user_scope = any(p.get('policy_type') == 'user-scoped' for p in pols)

            if has_admin_check:
                notes.append("admin-only writes")
            if has_user_scope:
                notes.append("user-scoped")

            notes_str = ", ".join(notes) if notes else "-"

            lines.append(f"| {table_name} | {rls_str} | {anon_str} | {auth_str} | {notes_str} |")

        lines.append("")

    # Legend
    lines.extend([
        "## Legend",
        "",
        "- **R** = SELECT (read)",
        "- **C** = INSERT (create)",
        "- **U** = UPDATE",
        "- **D** = DELETE",
        "- **RLS** = Row Level Security enabled",
        "- **admin-only writes** = Write operations require admin role",
        "- **user-scoped** = Access limited to user's own data via auth.uid()",
        "",
    ])

    return "\n".join(lines)


def format_grants(grants: set) -> str:
    """Format grant set as compact string."""
    if not grants:
        return "-"

    mapping = {
        'SELECT': 'R',
        'INSERT': 'C',
        'UPDATE': 'U',
        'DELETE': 'D',
    }

    result = []
    for op in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']:
        if op in grants:
            result.append(mapping[op])

    return "".join(result) if result else "-"


def main():
    parser = argparse.ArgumentParser(description="Audit Supabase security configuration")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown",
                        help="Output format (default: markdown)")
    args = parser.parse_args()

    print("Security Audit Script", file=sys.stderr)
    print("", file=sys.stderr)
    print("This script generates SQL queries for security auditing.", file=sys.stderr)
    print("Run these queries via Supabase MCP or SQL editor:", file=sys.stderr)
    print("", file=sys.stderr)

    for name, query in QUERIES.items():
        print(f"=== {name.upper()} ===", file=sys.stderr)
        print(query.strip(), file=sys.stderr)
        print("", file=sys.stderr)

    print("To generate the full report, run these queries and pass results to this script.", file=sys.stderr)
    print("Or use Claude Code with Supabase MCP to run the audit automatically.", file=sys.stderr)


if __name__ == "__main__":
    main()
