---
name: burp-suite-web-application-testing
description: Use this skill when you need to perform web application security testing with Burp Suite, including intercepting HTTP traffic, modifying web requests, and conducting vulnerability scans.
---

# Skill body

## Purpose

Execute comprehensive web application security testing using Burp Suite's integrated toolset, including HTTP traffic interception and modification, request analysis and replay, automated vulnerability scanning, and manual testing workflows. This skill enables systematic discovery and exploitation of web application vulnerabilities through a proxy-based testing methodology.

## Inputs / Prerequisites

### Required Tools
- Burp Suite Community or Professional Edition installed
- Burp's embedded browser or configured external browser
- Target web application URL
- Valid credentials for authenticated testing (if applicable)

### Environment Setup
- Launch Burp Suite with a temporary or named project
- Ensure the proxy listener is active on 127.0.0.1:8080 (default)
- Configure your browser to use Burp proxy (or use Burp's browser)
- Install CA certificate for HTTPS interception

### Editions Comparison
| Feature     | Community | Professional |
|-------------|-----------|--------------|
| Proxy       | ✓         | ✓            |
| Repeater    | ✓         | ✓            |
| Intruder    | Limited   | Full         |
| Scanner     | ✗         | ✓            |
| Extensions   | ✓         | ✓            |

## Outputs / Deliverables

### Primary Outputs
- Intercepted and modified HTTP requests/responses
- Vulnerability scan reports with remediation advice
- HTTP history and site map documentation
- Proof-of-concept exploits for identified vulnerabilities

## Core Workflow

### Phase 1: Intercepting HTTP Traffic

#### Launch Burp's Browser
Navigate to the integrated browser for seamless proxy integration:

1. Open Burp Suite and create or open a project.
2. Go to **Proxy > Intercept** tab.
3. Click **Open Browser** to launch the preconfigured browser.
4. Position windows to view both Burp and the browser simultaneously.

#### Configure Interception
Control which requests are captured:

```
Proxy > Intercept > Intercept is on/off toggle

When ON: Requests pause for review/modification.
When OFF: Requests pass through, logged to history.
```

#### Intercept and Forward Requests
Process intercepted traffic:

1. Set intercept toggle to **Intercept on**.
2. Review and modify requests as needed.
3. Click **Forward** to send the request to the server or **Drop** to discard it.