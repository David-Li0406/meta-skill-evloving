---
name: generating-database-seed-data
description: Use this skill when you need to quickly populate a database with realistic test data for development, testing, or demonstration purposes.
---

# Skill body

## Overview

This skill automates the creation of database seed scripts, populating your database with realistic and consistent test data. It leverages Faker libraries to generate diverse and believable data, ensuring relational integrity and configurable data volumes.

## How It Works

1. **Analyze Schema**: Analyze the database schema to understand table structures and relationships.
2. **Generate Data**: Use Faker libraries to generate realistic data for each table, respecting data types and constraints.
3. **Maintain Relationships**: Ensure foreign key relationships are maintained, creating consistent and valid data across tables.
4. **Create Seed Script**: Generate a database seed script (e.g., SQL, JavaScript) containing the generated data.

## When to Use This Skill

This skill activates when you need to:
- Populate a development database with realistic data.
- Create a seed script for automated database setup.
- Generate test data for application testing.
- Demonstrate an application with pre-populated data.

## Examples

### Example 1: Populating a User Database

User request: "Create a seed script to populate my users table with 50 realistic users."

The skill will:
1. Analyze the 'users' table schema (name, email, password, etc.).
2. Generate 50 sets of realistic user data using Faker libraries.
3. Create a SQL seed script to insert the generated user data into the 'users' table.

### Example 2: Seeding a Blog Database

User request: "Generate test data for my blog database, including posts, comments, and users."

The skill will:
1. Analyze the 'posts', 'comments', and 'users' table schemas and their relationships.
2. Generate realistic data for each table, ensuring foreign key relationships are maintained (e.g., comments linked to posts, posts linked to users).
3. Create a seed script to insert the generated data into the respective tables.