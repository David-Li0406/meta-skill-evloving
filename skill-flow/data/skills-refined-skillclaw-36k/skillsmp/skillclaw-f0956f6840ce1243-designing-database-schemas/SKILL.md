---
name: designing-database-schemas
description: Use this skill when you need to design, visualize, or normalize a database schema, generate an ERD, or create SQL statements for a relational database.
---

# Skill body

## Overview

This skill assists in designing robust and normalized database schemas. It provides guidance on normalization principles, helps map relationships between entities, generates ERD diagrams for visualization, and ultimately produces SQL CREATE statements.

## How It Works

1. **Schema Definition**: Analyze the user's request to understand the application's data requirements.
2. **Normalization & Relationship Mapping**: Apply normalization principles (1NF to BCNF) and define relationships between entities (one-to-one, one-to-many, many-to-many).
3. **ERD Generation**: Generate a Mermaid diagram representing the Entity-Relationship Diagram.
4. **SQL Generation**: Create SQL CREATE statements for the tables, columns, indexes, and constraints.

## When to Use This Skill

This skill activates when you need to:
- Design a new database schema from scratch.
- Normalize an existing database schema.
- Generate an ERD diagram for a database.
- Create SQL CREATE statements for a database.

## Examples

### Example 1: Designing a Social Media Database

User request: "Design a database schema for a social media application with users, posts, and comments."

The skill will:
1. Design tables for users, posts, and comments, including relevant attributes (e.g., user_id, username, post_id, content, timestamp).
2. Define relationships between the tables (e.g., one user can have many posts, one post can have many comments).
3. Generate an ERD diagram visualizing the relationships.
4. Create SQL CREATE TABLE statements for the tables, including primary keys, foreign keys, and indexes.

### Example 2: Normalizing an E-commerce Database

User request: "Normalize a database schema for an e-commerce application with customers, orders, and products."

The skill will:
1. Analyze the existing schema for normalization violations.
2. Decompose tables to eliminate redundancy and ensure compliance with normalization rules.
3. Generate an updated ERD and SQL statements reflecting the normalized schema.