# 🚀 SUPER-ENKEL Deploy till InfinityFree

## ⚡ ONE-CLICK SETUP (Första gången)

### Steg 1: Git pull på servern

Via InfinityFree File Manager eller SSH:
```bash
cd /htdocs
git pull origin claude/thehub-comprehensive-audit-01Sf5tTNHBQtMzEgsXZUmLP9
```

### Steg 2: Besök deploy-scriptet EN GÅNG

Öppna i webbläsaren (från mobil funkar!):
```
https://thehub.infinityfree.me/deploy-infinityfree.php
```

Detta fixar automatiskt:
- ✅ Skapar `.env` med alla credentials
- ✅ Konfigurerar databas
- ✅ Aktiverar produktion-läge
- ✅ Visar nästa steg

### Steg 3: RADERA deploy-infinityfree.php

**VIKTIGT!** Radera filen direkt i File Manager efter att du körst den!

(`.htaccess` blockerar access, men radera ändå för säkerhet)

### Steg 4: Kör SQL migrations

Gå till phpMyAdmin och kör dessa två filer:

1. `database/migrations/003_import_history.sql`
2. `database/migrations/004_point_scales.sql`

### Steg 5: Verifiera

Besök: `https://thehub.infinityfree.me/admin/test-database-connection.php`

Förväntat resultat:
- ✅ Config files exist
- ✅ Database constants defined
- ✅ NOT in demo mode
- ✅ Connection successful
- ✅ All tables exist
- ✅ 2598+ riders in database

---

## 🔄 Framtida uppdateringar

Efter initial setup behöver du bara:

```bash
cd /htdocs
git pull
```

Inga fler setup-script behövs! `.env` ligger kvar på servern.

---

## 📋 Filer som skapas på servern (gitignored)

Dessa filer finns BARA på servern, inte i git:

- `.env` - Databas credentials
- `uploads/*` - Uppladdade filer
- `*.log` - Log-filer

---

## ❓ Troubleshooting

**Problem:** "Connection failed"
- Kolla att `.env` finns i `/htdocs/`
- Verifiera DB credentials i `.env`

**Problem:** "Import tables missing"
- Kör migrations i phpMyAdmin (steg 4 ovan)

**Problem:** "Demo mode active"
- Kör setup-scriptet igen
- Kolla att `config/database.php` finns

---

## 🔐 Säkerhet

- ✅ `.env` är gitignored (credentials ej i git)
- ✅ `setup-production.php` ska raderas efter användning
- ✅ `config/database.php` innehåller INTE credentials (safe att commita)
