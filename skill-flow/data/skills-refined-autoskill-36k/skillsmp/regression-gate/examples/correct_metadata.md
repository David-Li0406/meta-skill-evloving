# Esempio di Metadata Corretti per FixLog

Quando salvi in Chroma (collection: `fix_logs`), il documento deve rispettare rigorosamente questo schema.

## ✅ Esempio JSON Valido
```json
{
  "id": "AG.fix.20260114.update-auth",
  "document": "Updated auth.py to use OAuth2 scopes...",
  "metadatas": {
    "project": "Antigravity",
    "type": "fix_log",
    "date": "2026-01-14",
    "files": "backend/auth.py, tests/test_auth.py",
    "tests": "pytest passed (14/14)",
    "result": "pass",
    "notes": "Regression gate passed successfully."
  }
}
```

## ❌ Errori Comuni (Da Evitare)
- **Missing Keys**: Omettere `project` o `result` causa il fallimento immediato del gate.
- **Null Values**: Nessun campo può essere `null` o stringa vuota `""`.
- **Wrong ID Format**: Usa sempre `<Prefix>.fix.<YYYYMMDD>.<slug>`.
