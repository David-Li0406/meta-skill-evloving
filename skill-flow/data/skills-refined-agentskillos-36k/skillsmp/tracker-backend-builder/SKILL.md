---
name: tracker-backend-builder
description: Sets up the backend structure for tracking pill ingestion. Use this when defining data models.
---

# Goal
Build a reliable log system.

# Instructions
1. Run `python scripts/db_gen.py` to get the Firestore Schema definition.
2. Apply this schema to the project's codebase (Data Models).
3. Ensure the `confidence_score` field is included to track if the user "thinks" they took it or "knows" they did.

## Firestore Architecture
Since this app uses Cloud Firestore (NoSQL), the "Schema" is enforced via application-side data models (`.dart` classes) and logic.
