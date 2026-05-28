# TheHUB - Plattform för Cykeltävlingar

Sveriges centrala plattform för cykeltävlingar med resultat, cyklistprofiler och tävlingsdata.

## Översikt

TheHUB är en PHP + MySQL-baserad plattform som hanterar:
- 3000+ cyklister
- 50+ tävlingar (2019-2025)
- Historiska resultat
- Klubbar och kategorier
- Import från Excel/CSV

**Tech Stack:**
- PHP 7.4+
- MySQL/MariaDB
- PhpSpreadsheet för Excel-import
- Native PHP (ingen framework)
- Dark theme med orange/gul accent

## Projektstruktur

```
TheHUB/
├── config/              # Konfigurationsfiler
│   ├── database.example.php
│   └── config.example.php
├── database/            # Databas-scheman
│   ├── schema.sql
│   └── migrations/
├── public/              # Publika sidor
│   ├── index.php
│   ├── events.php
│   ├── results.php
│   └── css/
├── admin/               # Admin-interface
│   ├── index.php
│   ├── login.php
│   ├── import.php
│   └── logout.php
├── includes/            # PHP-funktioner och klasser
│   ├── db.php
│   ├── functions.php
│   └── auth.php
├── imports/             # Import-scripts
│   ├── import_cyclists.php
│   └── import_results.php
├── templates/           # HTML-templates
└── uploads/             # Uppladdade filer
```

## Installation

### 1. Klona repositoryt

```bash
git clone https://github.com/ECABBIKE/TheHUB.git
cd TheHUB
```

### 2. Installera dependencies

```bash
composer install
```

Om du inte har Composer installerat, hämta det från: https://getcomposer.org/

### 3. Konfigurera databas

Kopiera example-filerna:

```bash
cp config/database.example.php config/database.php
cp config/config.example.php config/config.php
```

Redigera `config/database.php` med dina Uppsala Webbhotell-credentials:

```php
define('DB_HOST', 'your-mysql-host');
define('DB_NAME', 'your-database-name');
define('DB_USER', 'your-database-user');
define('DB_PASS', 'your-database-password');
```

### 4. Skapa databas och tabeller

Logga in på din MySQL-databas och kör schema-filen:

```bash
mysql -u your-user -p your-database < database/schema.sql
```

Eller via phpMyAdmin:
1. Öppna phpMyAdmin
2. Välj din databas
3. Gå till "Import"
4. Välj `database/schema.sql`
5. Kör import

### 5. Konfigurera uploads-katalog

```bash
mkdir -p uploads
chmod 755 uploads
```

### 6. Standard admin-inlogg

Efter att du kört `schema.sql` finns ett standard admin-konto:

- **Användarnamn:** admin
- **Lösenord:** changeme123

⚠️ **VIKTIGT:** Byt lösenord omedelbart efter första inloggningen!

## Användning

### Admin-interface

Gå till: `https://yourdomain.se/admin/login.php`

**Funktioner:**
- Dashboard med statistik
- Hantera cyklister, tävlingar, resultat
- Importera data från Excel
- Se importhistorik

### Importera data

#### Via Admin-interface (rekommenderat)

1. Logga in på admin
2. Gå till "Import"
3. Välj importtyp (Cyklister eller Resultat)
4. Ladda upp Excel-fil (.xlsx, .xls)
5. Klicka "Importera"

#### Via kommandorad

**Importera cyklister:**

```bash
php imports/import_cyclists.php /path/to/cyclists.xlsx 2
```

Format för cyklistfil:
```
A: Förnamn
B: Efternamn
C: Födelseår
D: Kön (M/F)
E: Klubb
F: Licensnummer
G: E-post
H: Telefon
I: Ort
```

**Importera resultat:**

```bash
php imports/import_results.php /path/to/results.xlsx 2
```

Format för resultatfil:
```
A: Tävlingsnamn
B: Datum (YYYY-MM-DD)
C: Plats
D: Placering
E: Startnummer
F: Förnamn
G: Efternamn
H: Födelseår
I: Klubb
J: Tid (HH:MM:SS)
K: Kategori
```

### Publika sidor

- **Startsida:** `/public/index.php`
- **Tävlingar:** `/public/events.php`
- **Resultat:** `/public/results.php?event_id=X`

## Databas-schema

### Huvudtabeller

**cyclists** - Cyklister
- id, firstname, lastname, birth_year, gender, club_id, license_number, email, phone, city

**events** - Tävlingar
- id, name, event_date, location, event_type, distance, status, description

**results** - Resultat
- id, event_id, cyclist_id, category_id, position, finish_time, bib_number, status

**clubs** - Klubbar
- id, name, short_name, region

**categories** - Kategorier
- id, name, short_name, age_min, age_max, gender

### Standard kategorier

- Herr Elite (19-34 år)
- Dam Elite (19-34 år)
- Herr Junior (17-18 år)
- Dam Junior (17-18 år)
- Herr Veteran 35-44
- Herr Veteran 45-54
- Herr Veteran 55+
- Dam Veteran 35+
- Herr Motion
- Dam Motion

## Funktioner

### Implementerade features

✅ MySQL-databas med komplett schema
✅ Excel-import för cyklister
✅ Excel-import för resultat
✅ Admin-interface med autentisering
✅ Dashboard med statistik
✅ Import-interface med historik
✅ Public views (events, results)
✅ Responsive dark theme
✅ Session management
✅ Flash messages
✅ Pagination
✅ Fuzzy matching för namnmatchning

### Kommande features (inte inkluderade)

❌ Poäng-beräkning (maj 2025)
❌ Serie-ställningar (maj 2025)
❌ Anmälningssystem
❌ Foto-upload/tagging
❌ WordPress SSO
❌ Advanced sökning

## Tips för import

### Hantering av dubbletter

Import-scripten hanterar automatiskt dubbletter:

1. **Cyklister:** Matchar först på licensnummer, sedan namn + födelseår
2. **Resultat:** Matchar på event + cyklist (en cyklist per event)

### Fuzzy matching

För framtida implementering av fuzzy matching (85%+), använd PHP-bibliotek som:
- `levenshtein()` - Inbyggd PHP-funktion
- `similar_text()` - Inbyggd PHP-funktion
- `fzaninotto/faker` - För testdata

### Stora filer

För import av stora Excel-filer (>5000 rader):
- Använd kommandorad-scripten istället för web-interface
- Öka PHP memory_limit om nödvändigt
- Kör import i batchar om möjligt

## Uppsala Webbhotell Setup

### .htaccess för clean URLs

Skapa `.htaccess` i root:

```apache
RewriteEngine On
RewriteBase /

# Redirect to public if no specific folder
RewriteCond %{REQUEST_URI} !^/(admin|public|uploads)
RewriteRule ^(.*)$ /public/$1 [L]

# PHP settings
php_value upload_max_filesize 10M
php_value post_max_size 10M
php_value memory_limit 256M
php_value max_execution_time 300
```

### Säkerhet

- Flytta `config/database.php` utanför web root om möjligt
- Använd HTTPS (Uppsala Webbhotell erbjuder Let's Encrypt)
- Sätt `DB_ERROR_DISPLAY` till `false` i produktion
- Byt admin-lösenord omedelbart

## Troubleshooting

### "Database connection failed"

- Kontrollera `config/database.php` credentials
- Verifiera att databasen existerar
- Testa anslutning via phpMyAdmin

### "Composer dependencies missing"

```bash
composer install --no-dev --optimize-autoloader
```

### "Permission denied" för uploads

```bash
chmod 755 uploads/
chown www-data:www-data uploads/  # Linux
```

### Import timeout

Öka PHP timeout i `.htaccess` eller `php.ini`:

```ini
max_execution_time = 300
memory_limit = 256M
```

## Utveckling

### Lägg till nya admin-sidor

1. Skapa fil i `/admin/`
2. Inkludera `auth.php` och `requireLogin()`
3. Använd navigation från `index.php`

### Lägg till nya publika sidor

1. Skapa fil i `/public/`
2. Inkludera `db.php` och `functions.php`
3. Använd header/footer från templates

### Uppdatera databas-schema

1. Skapa migration-fil i `database/migrations/`
2. Namnge: `YYYYMMDD_description.sql`
3. Kör manuellt via MySQL

## Support & Kontakt

**GitHub Issues:** https://github.com/ECABBIKE/TheHUB/issues

**Launch:** 17-19 januari 2025

## Licens

Proprietary - Alla rättigheter förbehållna

---

**Utvecklad med ❤️ för svensk cykling**
