---
name: preprocessing-data-with-automated-pipelines
description: Use this skill when you need to preprocess and clean data for machine learning tasks, automating data preparation through pipelines that ensure data quality and readiness.
---

# Skill body

## Overview

This skill enables Claude to construct and execute automated data preprocessing pipelines, ensuring data quality and readiness for machine learning. It streamlines the data preparation process by automating common tasks such as data cleaning, transformation, and validation.

## How It Works

1. **Analyze Requirements**: Claude analyzes the user's request to understand the specific data preprocessing needs, including data sources, target format, and desired transformations.
2. **Generate Pipeline Code**: Based on the requirements, Claude generates Python code for an automated data preprocessing pipeline using relevant libraries and best practices. This includes data validation and error handling.
3. **Execute Pipeline**: The generated code is executed, performing the data preprocessing steps.
4. **Provide Metrics and Insights**: Claude provides performance metrics and insights about the pipeline's execution, including data quality reports and potential issues encountered.

## When to Use This Skill

This skill activates when you need to:
- Prepare raw data for machine learning models.
- Automate data cleaning and transformation processes.
- Implement a robust ETL (Extract, Transform, Load) pipeline.

## Examples

### Example 1: Cleaning Customer Data

User request: "Preprocess the customer data from the CSV file to remove duplicates and handle missing values."

The skill will:
1. Generate a Python script to read the CSV file, remove duplicate entries, and impute missing values using appropriate techniques (e.g., mean imputation).
2. Execute the script and provide a summary of the changes made, including the number of duplicates removed and the number of missing values imputed.

### Example 2: Transforming Sensor Data

User request: "Create an ETL pipeline to transform sensor data from multiple sources into a unified format."

The skill will:
1. Generate a Python script to extract data from the specified sources, transform it into the desired format, and load it into a target database.
2. Execute the script and provide a summary of the data transformation process, including any errors encountered.