---
name: modeling-nosql-data
description: Use this skill when you need assistance with designing NoSQL database schemas, including creating models for MongoDB or DynamoDB, optimizing data structures, or translating relational models to NoSQL.
---

# Skill body

## Overview

This skill facilitates the design of efficient NoSQL data models, providing guidance on schema creation, denormalization strategies, and query optimization for document and key-value databases. It helps users translate their data requirements into production-ready NoSQL implementations.

## How It Works

1. **Identify Database Type**: Determine the target NoSQL database (e.g., MongoDB, DynamoDB).
2. **Analyze Data Requirements**: Understand the data entities, attributes, and relationships.
3. **Design Data Model**: Create a NoSQL data model based on the identified database type and data requirements, considering embedding vs. referencing and access patterns.
4. **Suggest Schema Definition**: Provide a schema definition or table structure based on the designed data model.

## When to Use This Skill

This skill activates when you need to:
- Design a new NoSQL database schema.
- Optimize an existing NoSQL data model for performance.
- Translate relational data models to NoSQL.
- Choose appropriate sharding keys for a NoSQL database.
- Generate MongoDB or DynamoDB schema definitions.

## Examples

### Example 1: Designing a MongoDB Schema for an E-commerce Application

User request: "Design a MongoDB schema for an e-commerce application, focusing on products and customers."

The skill will:
1. Analyze the data requirements for products and customers, considering attributes like product name, price, description, customer ID, name, and address.
2. Design a MongoDB schema with embedded product reviews and customer order history, optimizing for common query patterns.

### Example 2: Creating a DynamoDB Table for a Social Media Platform

User request: "Create a DynamoDB table for storing social media posts, considering high read and write throughput."

The skill will:
1. Analyze the data requirements for social media posts, considering attributes like user ID, timestamp, and content.
2. Design a DynamoDB table structure that supports efficient querying and scalability.