---
name: top-100-web-vulnerabilities-reference
description: Use this skill when you need to identify web application vulnerabilities, explain common security flaws, or assess security misconfigurations across various web security categories.
---

# Top 100 Web Vulnerabilities Reference

## Purpose

Provide a comprehensive, structured reference for the 100 most critical web application vulnerabilities organized by category. This skill enables systematic vulnerability identification, impact assessment, and remediation guidance across the full spectrum of web security threats.

## Prerequisites

- Basic understanding of web application architecture (client-server model, HTTP protocol)
- Familiarity with common web technologies (HTML, JavaScript, SQL, XML, APIs)
- Understanding of authentication and authorization concepts
- Access to web application security testing tools (e.g., Burp Suite, OWASP ZAP)
- Knowledge of secure coding principles recommended

## Outputs and Deliverables

- Complete vulnerability catalog with definitions, root causes, impacts, and mitigations
- Category-based vulnerability groupings for systematic assessment
- Quick reference for security testing and remediation
- Foundation for vulnerability assessment checklists and security policies

## Core Workflow

### Phase 1: Injection Vulnerabilities Assessment

Evaluate injection attack vectors targeting data processing components:

**SQL Injection**
- **Definition**: Malicious SQL code inserted into input fields to manipulate database queries.
- **Root Cause**: Lack of input validation, improper use of parameterized queries.
- **Impact**: Unauthorized data access, data manipulation, database compromise.
- **Mitigation**: Use parameterized queries/prepared statements, input validation, least privilege database accounts.

**Cross-Site Scripting (XSS)**
- **Definition**: Injection of malicious scripts into web pages viewed by other users.
- **Root Cause**: Insufficient output encoding.
- **Impact**: User data theft, session hijacking, defacement of web applications.
- **Mitigation**: Implement proper output encoding, use Content Security Policy (CSP), validate and sanitize user inputs.

### Additional Vulnerability Categories

- **Access Control Vulnerabilities**
- **Security Misconfigurations**
- **API Security Issues**
- **Client-Side Vulnerabilities**
- **Mobile and IoT Security Flaws**

This skill serves as a foundational resource for understanding and addressing web application vulnerabilities effectively.