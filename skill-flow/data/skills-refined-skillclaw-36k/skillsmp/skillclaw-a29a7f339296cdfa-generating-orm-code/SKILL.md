---
name: generating-orm-code
description: Use this skill when you need to generate ORM models or database schemas for various ORM frameworks, facilitating both database-to-code and code-to-database schema generation.
---

# Skill body

## Overview

This skill empowers Claude to automate the creation of Object-Relational Mapping (ORM) models and database schemas, significantly accelerating backend development. It handles generating code for various ORM frameworks, simplifying database interactions.

## How It Works

1. **Identify ORM and Language**: The skill parses the user's request to determine the target ORM framework (e.g., TypeORM, SQLAlchemy) and programming language (e.g., TypeScript, Python).
2. **Schema/Model Definition**: Based on the request, the skill either interprets an existing database schema or defines a new schema based on provided model specifications.
3. **Code Generation**: The skill generates the corresponding ORM model code, including entities, relationships, and any necessary configuration files, tailored to the chosen ORM framework.

## When to Use This Skill

This skill activates when you need to:
- Create ORM models from a database schema.
- Generate a database schema from existing ORM models.
- Generate model code for a specific ORM framework (e.g., TypeORM, Prisma).

## Examples

### Example 1: Generating TypeORM entities

User request: "Generate TypeORM entities for a blog with users, posts, and comments, including relationships and validation rules."

The skill will:
1. Generate TypeScript code defining TypeORM entities for `User`, `Post`, and `Comment`, including properties, relationships (e.g., one-to-many), and validation decorators.
2. Output the generated code, ready to be integrated into a TypeORM project.

### Example 2: Creating a SQLAlchemy schema

User request: "Create a SQLAlchemy schema for an e-commerce application with products, categories, and orders."

The skill will:
1. Generate Python code defining SQLAlchemy models for `Product`, `Category`, and `Order`, including relationships and necessary configurations.