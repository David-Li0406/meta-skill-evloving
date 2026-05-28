# 🚀 TheHUB LAUNCH CHECKLIST
**Launch Time**: T-12 timmar
**Target**: LIVE PRODUCTION
**Date**: 2025-12-28

---

## 🔴 KRITISKA ÅTGÄRDER (MÅSTE GÖRAS FÖRE LAUNCH)

### 1. ✅ Skapa .env-fil på Produktionsserver

**Plats**: `/home/user/TheHUB/.env`

```bash
# Skapa .env-fil
nano /home/user/TheHUB/.env
```

**Innehåll**:
```env
# Database Configuration
DB_HOST=localhost
DB_NAME=u994733455_thehub
DB_USER=u994733455_rogerthat
DB_PASS=DITT_RIKTIGA_DATABAS_LÖSENORD

# Admin Credentials
ADMIN_USERNAME=roger
ADMIN_PASSWORD_HASH=GENERERA_MED_KOMMANDOT_NEDAN

# Environment
APP_ENV=production
FORCE_HTTPS=true
SITE_URL=https://thehub.gravityseries.se
```

### 2. ✅ Generera Admin Password Hash

```bash
# Kör detta på servern:
php -r "echo password_hash('DittNyaSäkraLösenord', PASSWORD_DEFAULT) . PHP_EOL;"

# Kopiera resultatet (börjar med $2y$10$...) till .env:
# ADMIN_PASSWORD_HASH=$2y$10$...ditt_hash_här...
```

**VIKTIGT**: Spara det nya lösenordet säkert! Du behöver det för att logga in.

### 3. ✅ Sätt Rätt File Permissions

```bash
# Gå till TheHUB-mappen
cd /home/user/TheHUB

# Sätt säkra permissions
chmod 755 .
chmod 644 *.php
chmod 600 .env                    # ⚠️ KRITISKT - Bara owner kan läsa
chmod -R 755 includes admin api pages
chmod -R 644 includes/*.php admin/*.php api/*.php pages/*.php
chmod 755 logs uploads
chmod 666 logs/error.log          # Skrivbar för PHP
chmod 755 uploads/media uploads/icons
chmod -R 644 uploads/media/* uploads/icons/*  # Förhindra execution
```

### 4. ✅ Kör Databas-index för Prestanda

```bash
# Logga in i MySQL
mysql -u u994733455_rogerthat -p u994733455_thehub

# Kör index-skriptet
source /home/user/TheHUB/database/performance-indexes.sql
```

**Förväntat resultat**: ~40 index skapas, tar 10-30 sekunder

### 5. ✅ Verifiera Säkerhetsinställningar

```bash
# Kontrollera att .env existerar och inte är läsbar för alla
ls -la /home/user/TheHUB/.env
# Ska visa: -rw------- (600 permissions)

# Kontrollera att display_errors är avstängd
php -r "require 'config.php'; echo ini_get('display_errors') . PHP_EOL;"
# Ska visa: 0 (eller tomt)

# Kontrollera APP_ENV
php -r "require 'config.php'; echo APP_ENV . PHP_EOL;"
# Ska visa: production
```

---

## 🟡 VIKTIGA ÅTGÄRDER (BÖR GÖRAS)

### 6. ⚠️ Backup av Databas

```bash
# Ta full backup INNAN deployment
mysqldump -u u994733455_rogerthat -p u994733455_thehub > /home/user/backups/thehub_pre_launch_$(date +%Y%m%d_%H%M%S).sql

# Verifiera backup
ls -lh /home/user/backups/thehub_pre_launch_*.sql
```

### 7. ⚠️ Test Security Headers

Öppna sidan i Chrome/Firefox DevTools:

1. Öppna F12 → Network
2. Ladda om sidan
3. Klicka på första requesten
4. Gå till "Headers" → "Response Headers"

**Verifiera att dessa finns**:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains` (om HTTPS)
- `Content-Security-Policy: default-src 'self'...`

### 8. ⚠️ Git Status

```bash
cd /home/user/TheHUB

# Kontrollera vilken branch du är på
git branch --show-current
# Bör vara: claude/security-audit-thehub-01DEoBmsGmcQ6FSfL7g9Nvbt

# Se senaste commits
git log --oneline -5

# Pusha senaste ändringar
git add .
git commit -m "PRODUCTION: Ready for launch - security hardened"
git push origin claude/security-audit-thehub-01DEoBmsGmcQ6FSfL7g9Nvbt
```

---

## ✅ FUNKTIONELLA TESTER (POST-DEPLOYMENT)

### Test 1: Rider Registration Flow

1. Gå till `/rider-register.php`
2. Ange en e-post som finns i databasen MEN saknar lösenord
3. Välj ett lösenord (testa svagt lösenord först - ska avvisas)
4. Välj starkt lösenord: `TestLösen123!`
5. ✅ Ska redirect till `/rider-profile.php?welcome=1`

**Verifiera**:
- [ ] Lösenord med < 8 tecken avvisas
- [ ] Lösenord utan komplexitet avvisas (bara "password123")
- [ ] Starkt lösenord accepteras
- [ ] Redirect till profil fungerar

### Test 2: Rider Login

1. Logga ut (om inloggad)
2. Gå till `/rider-login.php`
3. Logga in med e-post + lösenord från Test 1
4. ✅ Ska visa rider-profil med resultat

**Verifiera**:
- [ ] Fel e-post/lösenord ger fel
- [ ] Rätt credentials loggar in
- [ ] Session persisterar (refresh = fortfarande inloggad)

### Test 3: Rate Limiting

1. Gå till `/rider-login.php`
2. Försök logga in med FEL lösenord 5 gånger
3. ✅ Sjätte försöket ska ge: "För många inloggningsförsök. Vänta 15 minuter"

**Verifiera**:
- [ ] Rate limiting aktiveras efter 5 försök
- [ ] Felmeddelande visas korrekt

### Test 4: Password Reset

1. Gå till `/rider-reset-password.php`
2. Ange en e-postadress
3. ✅ Ska visa: "Om e-postadressen finns i systemet..."

**Verifiera**:
- [ ] Ingen info läcker om e-post existerar
- [ ] Ingen token/link visas på sidan (KRITISKT!)
- [ ] Admin kan hitta token i `riders`-tabellen om manuell reset behövs

### Test 5: Admin Login

1. Gå till `/admin/login.php`
2. Logga in med USERNAME från .env + nya lösenordet
3. ✅ Ska redirect till `/admin/dashboard.php`

**Verifiera**:
- [ ] Admin login fungerar med nya hashat lösenordet
- [ ] CSRF-token skickas med formulär
- [ ] Session timeout fungerar (vänta 30 min)

### Test 6: Event Registration (API)

1. Logga in som rider
2. Gå till event-sida
3. Försök registrera dig till ett event
4. ✅ Registration ska fungera (redirect till checkout)

**Verifiera**:
- [ ] CSRF-token krävs (annars 403 error)
- [ ] Endast inloggade kan registrera
- [ ] Validering fungerar (korrekt klass, licens, etc)

### Test 7: HTTPS Redirect

**Endast om HTTPS är aktiverat:**

1. Försök nå `http://thehub.gravityseries.se` (utan S)
2. ✅ Ska automatiskt redirect till `https://...`

**Verifiera**:
- [ ] HTTP → HTTPS redirect fungerar
- [ ] 301 Moved Permanently status

### Test 8: XSS Protection

1. Gå till `/rider-register.php`
2. I e-post-fältet, ange: `<script>alert('XSS')</script>@test.com`
3. Submitta formulär
4. ✅ Ingen alert ska visas (script escapad)

**Verifiera**:
- [ ] Script-tags escapas i felmeddelanden
- [ ] HTML entities visas som text

### Test 9: SQL Injection Protection

1. Gå till `/rider-login.php`
2. I e-post-fältet, ange: `' OR 1=1--@test.com`
3. Försök logga in
4. ✅ Ska ge "Ogiltig e-post eller lösenord"

**Verifiera**:
- [ ] SQL injection fungerar INTE
- [ ] Inga databas-fel visas

### Test 10: File Upload Security

**Om admin:**

1. Gå till `/admin/import-riders.php` (eller liknande)
2. Försök ladda upp fil: `test.php.csv` (dubbel extension)
3. ✅ Ska avvisas: "Misstänkt dubbel filändelse"

**Verifiera**:
- [ ] Dubbla extensions blockeras
- [ ] Körbara filer (.php, .exe) blockeras
- [ ] Endast CSV/XLSX accepteras

---

## 📊 PRESTANDA-TESTER

### Test 11: Sidan Under Belastning

**Verktyg**: Apache Bench eller Browser DevTools

```bash
# Test med 50 samtidiga requests (installera apache2-utils först)
ab -n 100 -c 50 https://thehub.gravityseries.se/

# ELLER öppna 20 tabs snabbt i browser och refresh alla samtidigt
```

**Målvärden**:
- Requests per second: > 10
- Average response time: < 500ms
- Failed requests: 0

**Verifiera**:
- [ ] Sidan laddar snabbt även vid belastning
- [ ] Inga 500/502/504 errors
- [ ] Databas hanterar queries

### Test 12: Error Log Monitoring

```bash
# Följ error log live under tester
tail -f /home/user/TheHUB/logs/error.log

# Eller kolla efter tester
cat /home/user/TheHUB/logs/error.log
```

**Förväntat**:
- Password reset requests loggas (bara email)
- Inga PHP warnings/errors
- Inga SQL errors
- Inga stack traces

---

## 🔒 SÄKERHETS-VERIFIERING

### Checklist för Säkerhetsfunktioner

**Autentisering**:
- [x] Password hashing (bcrypt)
- [x] Session regeneration vid login
- [x] Rate limiting (5/15min)
- [x] Secure session cookies (httponly, samesite)

**CSRF Protection**:
- [x] Alla POST-formulär har csrf_field()
- [x] API endpoints validerar CSRF-token
- [x] Timing-safe token comparison

**SQL Injection**:
- [x] Prepared statements i alla queries
- [x] Input sanitization (intval, trim, etc)

**XSS Protection**:
- [x] h() function för output escaping
- [x] htmlspecialchars() i alla templates
- [x] JSON auto-escaping i API responses

**File Upload**:
- [x] Extension whitelist
- [x] MIME type validation
- [x] Double extension blocking
- [x] Executable file blocking

**Error Handling**:
- [x] display_errors=0 i production
- [x] Errors loggas till fil
- [x] Generic error messages till användare

**Security Headers**:
- [x] X-Content-Type-Options: nosniff
- [x] X-Frame-Options: SAMEORIGIN
- [x] X-XSS-Protection
- [x] Strict-Transport-Security (HSTS)
- [x] Content-Security-Policy

**HTTPS**:
- [x] HTTPS enforcement
- [x] Proxy-aware (X-Forwarded-Proto)

**Password Security**:
- [x] Minimum 8 characters
- [x] Complexity requirements (3 of 4)
- [x] Common password blacklist

**Session Security**:
- [x] 30 min activity timeout
- [x] Session ID regeneration
- [x] Secure cookie flags

---

## 🎯 GO/NO-GO BESLUT

### KRITISKA KRAV (Alla MÅSTE vara ✅)

- [ ] .env-fil skapad med rätt credentials
- [ ] ADMIN_PASSWORD_HASH genererat och testat
- [ ] File permissions satta korrekt (.env = 600)
- [ ] display_errors=0 verifierat i production
- [ ] APP_ENV=production satt
- [ ] Databas-backup tagen
- [ ] Rider registration fungerar
- [ ] Rider login fungerar
- [ ] Admin login fungerar
- [ ] HTTPS redirect fungerar (om aktiverat)

**OM ALLA OVAN ÄR ✅**: 🟢 **GO FOR LAUNCH**
**OM NÅGON ÄR ❌**: 🔴 **NO-GO - FIX FÖRST**

---

## 📞 SUPPORT EFTER LAUNCH

### Om problem uppstår:

**1. Sidan visar blank/white screen:**
```bash
# Kolla error log
tail -50 /home/user/TheHUB/logs/error.log

# Vanliga orsaker:
# - .env-fil saknas
# - Databas credentials fel
# - PHP syntax error
```

**2. "Database configuration missing":**
```bash
# Verifiera .env finns
cat /home/user/TheHUB/.env

# Kolla permissions
ls -la /home/user/TheHUB/.env
```

**3. Admin login fungerar inte:**
```bash
# Generera nytt hash
php -r "echo password_hash('NyttLösenord', PASSWORD_DEFAULT) . PHP_EOL;"

# Uppdatera .env
nano /home/user/TheHUB/.env
# ADMIN_PASSWORD_HASH=$2y$10$...nya_hashen...
```

**4. Password reset visar token/link:**
```bash
# Kontrollera att du har senaste koden
cd /home/user/TheHUB
git pull origin claude/security-audit-thehub-01DEoBmsGmcQ6FSfL7g9Nvbt

# Kolla includes/rider-auth.php rad 216-219
# Ska INTE innehålla 'token' eller 'link' i return array
```

**5. Manuell Password Reset (om e-post ej fungerar):**
```sql
-- Logga in i MySQL
mysql -u u994733455_rogerthat -p u994733455_thehub

-- Hitta rider
SELECT id, firstname, lastname, email, password_reset_token
FROM riders
WHERE email = 'rider@example.com';

-- Kopiera token från password_reset_token kolumnen
-- Skicka denna URL till rider:
-- https://thehub.gravityseries.se/rider-reset-password.php?token=TOKENHÄR
```

**6. Prestanda-problem:**
```bash
# Kolla slow queries
mysql -u u994733455_rogerthat -p -e "SHOW FULL PROCESSLIST;"

# Verifiera index
mysql -u u994733455_rogerthat -p u994733455_thehub < database/performance-indexes.sql
```

---

## 🎉 POST-LAUNCH MONITORING

### Första 24 timmarna:

**Varje timme:**
- [ ] Kolla error log: `tail -20 /home/user/TheHUB/logs/error.log`
- [ ] Testa rider login/registration
- [ ] Verifiera sidan är uppe

**Första veckan:**
- [ ] Samla feedback från användare
- [ ] Övervaka databas-storlek och prestanda
- [ ] Planera e-post-implementation för password reset

---

## 📝 NOTES & LEARNINGS

**Framtida förbättringar**:
1. Implementera e-post för password reset (prioritet 1)
2. Lägg till IP-baserad rate limiting för DDoS-skydd
3. Implementera e-post-verifiering vid registrering
4. Cache för statiska sidor
5. CDN för assets

**Vad gick bra**:
- [Lista framgångar efter launch]

**Vad kan förbättras**:
- [Lista lärdomar efter launch]

---

**LYCKA TILL MED LANSERINGEN! 🚀**

**Support**: Om kritiska problem uppstår, kontakta claude för hjälp.

**Kom ihåg**: Ta det lugnt, andas, och testa noggrant. Du har gjort ett fantastiskt jobb med säkerheten! 💪
