---
name: qdrant-sync
description: Update the account's searchable description in Qdrant after state changes. Keeps search results accurate.
---

# Qdrant Sync

## When to use this skill

- After any state.md update
- After account creation
- When description should reflect new status

## What gets indexed

Two collections are maintained:

### 1. Name Collection

For `lookup_account` searches:

```json
{
  "account_id": "29041",
  "name": "Sunny Days Childcare Center",
  "directory_path": "mem/accounts/29041"
}
```

### 2. Description Collection

For `search_descriptions` searches:

```json
{
  "account_id": "29041",
  "name": "Sunny Days Childcare Center",
  "description": "Sunny Days Childcare Center, a childcare facility in Austin, TX. Stage: Quote Pitched. Seeking General Liability and Workers Comp coverage. Waiting for loss runs.",
  "directory_path": "mem/accounts/29041"
}
```

## Description generation

Generate a searchable description including:

1. Company name and what they do
2. Location (city, state)
3. Current stage
4. Insurance types sought
5. Key status (waiting for docs, quote pending, etc.)

Keep under 100 words. Focus on searchable attributes.

## Sync process

1. Read current `state.md`
2. Generate new description from state
3. Call `upsert_description` with:
   - account_id
   - name
   - description
   - directory_path

## When to skip

- Read-only operations (no state change)
- Failed updates (state not modified)
