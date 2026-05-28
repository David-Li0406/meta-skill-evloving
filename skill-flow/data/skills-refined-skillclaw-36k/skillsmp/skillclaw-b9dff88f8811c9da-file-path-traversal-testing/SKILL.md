---
name: file-path-traversal-testing
description: Use this skill when you need to test for directory traversal vulnerabilities, exploit path traversal issues, or access files outside the web root in web applications.
---

# File Path Traversal Testing

## Purpose

Identify and exploit file path traversal (directory traversal) vulnerabilities that allow attackers to read arbitrary files on the server, potentially including sensitive configuration files, credentials, and source code. This vulnerability occurs when user-controllable input is passed to filesystem APIs without proper validation.

## Prerequisites

### Required Tools
- Web browser with developer tools
- Burp Suite or OWASP ZAP
- cURL for testing payloads
- Wordlists for automation
- ffuf or wfuzz for fuzzing

### Required Knowledge
- HTTP request/response structure
- Linux and Windows filesystem layout
- Web application architecture
- Basic understanding of file APIs

## Outputs and Deliverables

1. **Vulnerability Report** - Identified traversal points and severity
2. **Exploitation Proof** - Extracted file contents
3. **Impact Assessment** - Accessible files and data exposure
4. **Remediation Guidance** - Secure coding recommendations

## Core Workflow

### Phase 1: Understanding Path Traversal

Path traversal occurs when applications use user input to construct file paths:

```php
// Vulnerable PHP code example
$template = "blue.php";
if (isset($_COOKIE['template']) && !empty($_COOKIE['template'])) {
    $template = $_COOKIE['template'];
}
include("/home/user/templates/" . $template);
```

**Attack principle:**
- `../` sequence moves up one directory
- Chain multiple sequences to reach root
- Access files outside intended directory

**Impact:**
- **Confidentiality** - Read sensitive files
- **Integrity** - Write/modify files (in some cases)
- **Availability** - Delete files (in some cases)
- **Code Execution** - If combined with file upload or log poisoning

### Phase 2: Identifying Traversal Points

Map application for potential file operations:

```bash
# Parameters that often handle files
?file=
?path=
?page=
?template=
?filename=
?doc=
?document=
?folder=
?dir=
?include=
?src=
?source=
?content=
?view=
?download=
?load=
?read=
?retrieve=
```

**Common vulnerable functionality:**
- Image loading: `/image?filename=23.jpg`
- Template selection: `?template=blue.php`