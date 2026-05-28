---
name: detecting-data-anomalies
description: Use this skill when you need to identify anomalies and outliers within datasets, such as detecting fraud or unusual patterns in data.
---

# Skill body

## Overview

This skill empowers Claude to identify anomalies and outliers within datasets by leveraging the anomaly-detection-system plugin. It automates the process of anomaly detection, providing insights into potential errors, fraud, or other significant deviations from expected patterns.

## How It Works

1. **Data Analysis**: Analyze the user's request and the provided data to understand the context and requirements for anomaly detection.
2. **Algorithm Selection**: Select an appropriate anomaly detection algorithm based on the data characteristics (e.g., Isolation Forest, One-Class SVM).
3. **Anomaly Identification**: Apply the selected algorithm to the data to identify potential anomalies based on their deviation from the norm.

## When to Use This Skill

This skill activates when you need to:
- Identify fraudulent transactions in financial data.
- Detect unusual network traffic patterns that may indicate a security breach.
- Find manufacturing defects based on sensor data from production lines.

## Examples

### Example 1: Fraud Detection

User request: "Analyze this transaction data for potential fraud."

The skill will:
1. Use the anomaly-detection-system plugin to identify transactions that deviate significantly from typical spending patterns.
2. Highlight the potentially fraudulent transactions and provide a summary of their characteristics.

### Example 2: Network Security

User request: "Detect anomalies in network traffic to identify potential security threats."

The skill will:
1. Use the anomaly-detection-system plugin to analyze network traffic data for unusual patterns.
2. Identify potential security breaches based on deviations from normal network behavior.

## Best Practices

- **Data Preprocessing**: Ensure the data is clean, properly formatted, and scaled appropriately before applying anomaly detection algorithms.
- **Algorithm Selection**: Choose an anomaly detection algorithm that best fits the data characteristics and the specific use case.