---
name: running-clustering-algorithms
description: Use this skill when you need to perform clustering analysis on datasets to identify groups or analyze data structure.
---

# Skill body

## Overview

This skill empowers Claude to execute various clustering algorithms on provided datasets, offering insights into data groupings and structures.

## How It Works

1. **Analyzing the Context**: Determine the dataset and desired clustering algorithm (if specified) from the user's request.
2. **Generating Code**: Create Python code using appropriate ML libraries (e.g., scikit-learn) for data loading, preprocessing, algorithm execution, and result visualization.
3. **Executing Clustering**: Run the generated code to apply the clustering algorithm to the dataset.
4. **Providing Results**: Present results, including cluster assignments, performance metrics (e.g., silhouette score, Davies-Bouldin index), and visualizations (e.g., scatter plots with cluster labels).

## When to Use This Skill

Activate this skill when you need to:
- Identify distinct groups within a dataset.
- Perform a cluster analysis to understand data structure.
- Run K-means, DBSCAN, or hierarchical clustering on a given dataset.

## Examples

### Example 1: Customer Segmentation

User request: "Run clustering on this customer data to identify customer segments. The data is in customer_data.csv."

The skill will:
1. Load the customer_data.csv dataset.
2. Perform K-means clustering to identify distinct customer segments based on their attributes.
3. Provide a visualization of the customer segments and their characteristics.

### Example 2: Anomaly Detection

User request: "Perform DBSCAN clustering on this network traffic data to identify anomalies. The data is available at network_traffic.txt."

The skill will:
1. Load the network_traffic.txt dataset.
2. Perform DBSCAN clustering to identify outliers representing anomalies.
3. Present the results and visualizations of the identified anomalies.