---
name: verify-pr
description: Analyze PR implementation and provide verification instructions
---

Analyze PR implementation and provide verification instructions for $ARGUMENTS

## Prerequisites
- $ARGUMENTS: PR number
- Run from repository root

## Process

1. Fetch PR diff: `gh pr diff $ARGUMENTS`
2. Search changed files (parallel Grep calls) for:
   - Route definitions: `router\.(GET|POST|PUT|DELETE)|HandleFunc|http\.Handle`
   - Auth patterns: `JWT|Authorization|Bearer|API.*Key`
   - Env vars: `os\.Getenv|viper\.|config\.|ENV`
   - DB ops: `migrate|seed|CREATE TABLE|ALTER TABLE`
   - External deps: `Redis|S3|AWS|GCP`
3. Generate verification instructions with:
   - Prerequisites (server startup, env vars, DB setup, test data)
   - curl examples for each endpoint (method, URL, headers, body)
   - Authentication details (token acquisition, header format)
   - Expected responses (status codes, response body examples)
4. Output structured verification guide

## Output Format

Structure: 前提条件 (server start, env vars, DB setup) → APIエンドポイント確認 (each endpoint with curl example, expected status/body)

## Analysis Guidelines

- Focus on user-facing changes (new/modified endpoints)
- Extract authentication requirements from middleware/handlers
- Identify environment-dependent configuration
- Include realistic request/response examples
- Note any breaking changes or migration requirements

## Notes

- If no API changes detected, report: "このPRにはAPI変更が含まれていません"
- For non-API changes (refactoring, internal), suggest relevant verification method
- Include warnings for breaking changes or required migrations
