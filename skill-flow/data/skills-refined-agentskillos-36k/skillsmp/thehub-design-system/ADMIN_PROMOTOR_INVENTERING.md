# TheHUB Admin & Promotor - Inventering

**Datum:** 2026-01-12
**Analyserad av:** Claude Code
**Version:** v1.0 [2026-01-12]

---

## 1. EXECUTIVE SUMMARY

TheHUB har ett välstrukturerat rollbaserat åtkomstsystem med 4 roller: `rider`, `promotor`, `admin`, och `super_admin`.

**Sammanfattning:**
- **Admin-funktioner:** Ca 150+ PHP-filer i `/admin/` med 6 huvudgrupper (Tävlingar, Serier, Databas, Konfiguration, Import, System)
- **Promotor-funktioner:** 4 dedikerade filer + begränsad åtkomst till vissa admin-sidor
- **Största risken:** Tre olika navigationsfiler med delvis duplicerad logik kan orsaka inkonsistenser

---

## 2. DOKUMENTERAD VS IMPLEMENTERAD

### Enligt Roadmap/Docs:

| Funktion | Admin | Promotor | Status |
|----------|-------|----------|--------|
| CRUD Events | Yes | Tilldelade | Implementerad |
| CRUD Resultat | Yes | Tilldelade | Implementerad |
| Anmälningshantering | Yes | Tilldelade | Implementerad |
| Betalningshantering | Yes | Begränsad | Implementerad |
| Användarhantering | Yes | Nej | Implementerad |
| Systemverktyg | Yes | Nej | Implementerad |
| Import funktioner | Yes | Nej | Implementerad |
| Serie-inställningar | Yes | Egna serier | Implementerad |
| Sponsorhantering | Yes | Tilldelade | Delvis implementerad |

### Implementerat men inte dokumenterat i ROADMAP:
- Eliminationsformat (Dual Slalom) - Helt implementerat men bara kort nämnt
- Gravity ID system - Rabattkoder för medlemmar
- Stage bonus points - Bonuspoäng per etapp
- Club championship 100%/50% regel
- Promotor payments - Utbetalningshantering

---

## 3. MENYSTRUKTUR - ADMIN

### Navigationsfiler:

| Fil | Plats | Syfte |
|-----|-------|-------|
| `sidebar.php` | `/components/` | **Primär** - Huvudnavigation för hela sajten (publik + admin) |
| `admin-sidebar.php` | `/admin/components/` | **Sekundär** - Äldre admin-specifik navigation |
| `navigation.php` | `/includes/` | **Alternativ** - Liknande logik som sidebar.php |
| `admin-tabs-config.php` | `/includes/config/` | **Konfiguration** - Definierar alla admin-flikar och grupper |
| `admin-submenu.php` | `/includes/components/` | Submenyer inom admin |
| `admin-mobile-nav.php` | `/admin/components/` | Mobilnavigation |

### Menyträd (från admin-tabs-config.php):

```
Admin Dashboard
├── Tävlingar (competitions)
│   ├── Events (events.php, event-create.php, event-edit.php, event-map.php)
│   ├── Resultat (results.php, edit-results.php, clear-event-results.php)
│   ├── Texter (global-texts.php)
│   ├── Prismallar (pricing-templates.php) [super_admin]
│   └── Elimination (elimination.php, elimination-manage.php, elimination-live.php)
│
├── Serier (standings)
│   ├── Serier (series.php, series-events.php, series-pricing.php, series-manage.php)
│   ├── Ranking (ranking.php)
│   ├── Klubbpoäng (club-points.php, club-points-detail.php)
│   └── Anmälningsregler (registration-rules.php)
│
├── Databas (database)
│   ├── Deltagare (riders.php, rider-edit.php, enrich-riders.php)
│   ├── Klubbar (clubs.php, club-edit.php)
│   └── Anläggningar (venues.php, venue-edit.php)
│
├── Konfiguration (config)
│   ├── Ekonomi (ekonomi.php, orders.php, payment-settings.php, etc.)
│   ├── Rabattkoder (discount-codes.php)
│   ├── Gravity ID (gravity-id.php)
│   ├── Klasser (classes.php)
│   ├── Licenser (license-class-matrix.php)
│   ├── Poängskalor (point-scales.php, point-scale-edit.php)
│   ├── Publikt (public-settings.php)
│   ├── Media (media.php)
│   ├── Sponsorer (sponsors.php)
│   ├── Reklamplatser (sponsor-placements.php) [super_admin]
│   └── Race Reports (race-reports.php) [super_admin]
│
├── Import (import)
│   ├── Översikt (import.php)
│   ├── Deltagare (import-riders.php, import-gravity-id.php)
│   ├── Resultat (import-results.php, import-results-preview.php)
│   ├── Events (import-events.php, import-series.php, import-classes.php)
│   ├── UCI (import-uci.php, import-uci-preview.php)
│   ├── Venues (import-venues.php)
│   └── Historik (import-history.php)
│
└── System (settings) [ENDAST super_admin]
    ├── Användare (users.php, user-edit.php, user-events.php)
    ├── Behörigheter (role-permissions.php)
    ├── Databas (system-settings.php, run-migrations.php)
    ├── Verktyg (tools.php, normalize-names.php, find-duplicates.php, etc.)
    └── Branding (branding.php)
```

### Admin-sidor (filer) - Urval av viktiga:

| Fil | Syfte | CRUD | Databas-tabeller |
|-----|-------|------|------------------|
| `dashboard.php` | Översikt med statistik | R | flera |
| `events.php` | Lista/hantera events | CRUD | events |
| `event-edit.php` | Redigera enskilt event | CRU | events, results, classes |
| `riders.php` | Lista/hantera deltagare | CRUD | riders |
| `rider-edit.php` | Redigera deltagare | CRU | riders, results |
| `clubs.php` | Lista/hantera klubbar | CRUD | clubs |
| `series.php` | Lista/hantera serier | CRUD | series |
| `users.php` | Användarhantering | CRUD | admin_users |
| `orders.php` | Beställningar | RU | orders, order_items |
| `import.php` | Importöversikt | R | import_history |
| `elimination.php` | Dual Slalom brackets | CRUD | elimination_* |

---

## 4. MENYSTRUKTUR - PROMOTOR

### Navigationsfiler:

| Fil | Plats | Syfte |
|-----|-------|-------|
| `sidebar.php` | `/components/` | Visar promotor-sektion när `$isPromotorOnly = true` |

### Menyträd (från sidebar.php linjer 157-162):

```
Promotor Dashboard
├── Tävlingar (/admin/promotor.php)
│   └── [visar endast tilldelade events via promotor_events]
│
├── Serier (/admin/promotor-series.php)
│   └── [visar endast tilldelade serier via promotor_series]
│
├── Sponsorer (/admin/sponsors.php)
│   └── [begränsad åtkomst?]
│
└── Direktanmälan (/admin/onsite-registration.php)
    └── [för anmälan på plats vid event]
```

### Promotor-sidor (filer):

| Fil | Syfte | CRUD | Databas-tabeller |
|-----|-------|------|------------------|
| `promotor.php` | Huvudpanel - "Mina tävlingar" | R | events, series (tilldelade) |
| `promotor-registrations.php` | Hantera anmälningar för event | RU | event_registrations |
| `promotor-payments.php` | Se/hantera betalningar | RU | orders, payment_transactions |
| `promotor-series.php` | Serie-inställningar | RU | series (tilldelade) |

### Promotor kan också nå:

| Sida | Via | Begränsning |
|------|-----|-------------|
| `event-edit.php` | Link från promotor.php | Endast tilldelade events (`canAccessEvent()`) |
| `sponsors.php` | Sidebar | Oklart vilka begränsningar |
| `onsite-registration.php` | Sidebar | Endast för events de har tillgång till |

---

## 5. JÄMFÖRELSE: ADMIN vs PROMOTOR

### Funktioner bara Admin har:
- [x] Användarhantering (users.php)
- [x] Systeminställningar (settings.php, system-settings.php)
- [x] Databas-verktyg (tools.php, find-duplicates.php, etc.)
- [x] Import av data (import-*.php)
- [x] Skapa nya events/serier (event-create.php)
- [x] Betalningsinställningar (payment-settings.php, gateway-settings.php)
- [x] Klasser och licensmatris
- [x] Poängskalor
- [x] Branding
- [x] Migration/databas-hantering

### Funktioner bara Promotor har:
- [x] `promotor.php` - Förenklad översikt med bara tilldelade events
- [x] `promotor-series.php` - Begränsad serie-redigering (Swish, banner)

### Delade funktioner (finns i båda men med olika åtkomst):

| Funktion | Admin-fil | Promotor-fil/åtkomst | Identisk kod? |
|----------|-----------|----------------------|---------------|
| Event-redigering | `event-edit.php` | Samma fil, `canAccessEvent()` | Ja, filterad |
| Anmälningar | `event-registrations.php` | `promotor-registrations.php` | Nej, separata |
| Betalningar | `orders.php` | `promotor-payments.php` | Nej, separata |
| Sponsorer | `sponsors.php` | Samma fil? | Oklart |
| Serie-hantering | `series-edit.php` | `promotor-series.php` (begränsad) | Nej, begränsad |

---

## 6. ROLLBASERAD ÅTKOMST

### Hur roller definieras:

Roller lagras i:
- `$_SESSION['admin_role']` - Vid inloggning
- `admin_users.role` - I databasen (ENUM: 'super_admin', 'admin', 'promotor', 'rider')

### Roller som finns:

| Roll | ID/Hierarki | Beskrivning |
|------|-------------|-------------|
| `rider` | 1 | Kan logga in, se/redigera sin egen profil |
| `promotor` | 2 | Kan hantera tilldelade events och serier |
| `admin` | 3 | Full åtkomst till admin (utom System-sektionen) |
| `super_admin` | 4 | Full åtkomst + System, Användare, Branding |

### Åtkomstkontroll:

**Fil:** `/includes/auth.php`

**Huvudfunktioner:**
```php
hasRole($role)        // Hierarkisk kontroll (promotor kan inte access admin)
isRole($role)         // Exakt kontroll (är exakt denna roll)
canAccessEvent($id)   // Kontrollerar promotor_events-tabell
canAccessSeries($id)  // Kontrollerar promotor_series-tabell
canManageClub($id)    // Kontrollerar club_admins-tabell
```

**Exempel på användning i kod:**
```php
// Dashboard - omdirigerar promotors
if (isRole('promotor')) {
    redirect('/admin/promotor.php');
}

// Users - kräver super_admin
if (!hasRole('super_admin')) {
    die('Access denied');
}

// Event-redigering - tillåt admin ELLER tilldelad promotor
if (!hasRole('admin') && !canAccessEvent($eventId)) {
    redirect('/admin/promotor.php');
}
```

### Kopplingstabeller:

| Tabell | Syfte | Fält |
|--------|-------|------|
| `promotor_events` | Kopplar user_id till event_id | can_edit, can_manage_results, can_manage_registrations, can_manage_payments |
| `promotor_series` | Kopplar user_id till series_id | can_edit, can_manage_results, can_manage_registrations |
| `club_admins` | Kopplar user_id till club_id | can_edit_profile, can_upload_logo, can_manage_members |

---

## 7. DUPLICERAD KOD / TEKNISK SKULD

### Identifierade dupliceringar:

| Kod/Funktion | Förekommer i | Bedömning |
|--------------|--------------|-----------|
| Navigationsdefinitioner | `sidebar.php`, `admin-sidebar.php`, `navigation.php` | Medium - Samma meny definieras på 3 ställen |
| Promotor meny | `sidebar.php` (rad 157-162), `admin-sidebar.php` (rad 20-44) | Medium - Liknande men inte identisk |
| Anmälningshantering | `event-registrations.php`, `promotor-registrations.php` | Låg - Avsiktligt olika vyer |
| Betalningshantering | `orders.php`, `promotor-payments.php` | Låg - Avsiktligt olika vyer |

### Inkonsistenser:

1. **Navigationsfiler:**
   - `sidebar.php` använder `hub_icon()` för ikoner
   - `admin-sidebar.php` har inline SVG-ikoner
   - `navigation.php` har egen `nav_icon()` funktion

2. **Rollnamn i databas:**
   - `schema.sql` definierar ENUM som `'super_admin', 'admin', 'editor'`
   - `auth.php` hanterar `'rider', 'promotor', 'admin', 'super_admin'`
   - `'editor'` verkar vara legacy och ersatt med `'promotor'`

3. **Layout-komponenter:**
   - Admin-sidor använder olika layout-inkluderingar:
     - `components/unified-layout.php` (nyare)
     - `includes/admin-header.php` + `includes/admin-footer.php` (äldre)

---

## 8. SAKNAS / INTE IMPLEMENTERAT

### Enligt Roadmap men saknas:
- [ ] Live-uppdateringar (real-time leaderboard)
- [ ] Push-notiser
- [ ] Head-to-Head jämförelser
- [ ] Event-kartsystem (GPX-uppladdning finns, men ofullständigt)
- [ ] Predictions / Fantasy League
- [ ] Community Features
- [ ] Marknadsplats
- [ ] Automatisk taggning av bilder
- [ ] API för tredjepartsintegrationer

### Borde finnas men verkar saknas:
- [ ] Tydlig dokumentation om promotor-flödet
- [ ] Auditloggning av admin-åtgärder
- [ ] Bättre felhantering vid rollkontroll (ibland `die()`, ibland redirect)
- [ ] E-postnotifieringar till promotors vid nya anmälningar
- [ ] Dashboard för promotors med statistik (finns `promotor.php` men begränsad)

---

## 9. REKOMMENDATIONER

### Prioritet 1 (Bör åtgärdas):

1. **Konsolidera navigationsfiler**
   - Använd endast `sidebar.php` + `admin-tabs-config.php`
   - Ta bort eller depreca `navigation.php` och `admin-sidebar.php`

2. **Synka databas-schema med kod**
   - Uppdatera `schema.sql` ENUM att matcha faktiska roller: `'rider', 'promotor', 'admin', 'super_admin'`
   - Ta bort `'editor'` om det inte används

3. **Standardisera layout-inkludering**
   - Migrera alla admin-sidor till `unified-layout.php`
   - Dokumentera vilken header/footer som ska användas

### Prioritet 2 (Bör planeras):

1. **Förbättra promotor-upplevelsen**
   - Lägg till dashboard med statistik (anmälningar, intäkter)
   - E-postnotifieringar vid nya anmälningar
   - Möjlighet att exportera deltagarlistor

2. **Dokumentera rollsystemet**
   - Skapa tydlig dokumentation om vilka rättigheter varje roll har
   - Lägg till i CLAUDE.md eller separat ROLES.md

3. **Förbättra åtkomstkontroll**
   - Skapa enhetlig middleware för rollkontroll
   - Logga åtkomstförsök för säkerhet

### Prioritet 3 (Nice to have):

1. **Audit-loggning**
   - Logga alla CRUD-operationer i admin
   - Spåra vem som gjort vad

2. **Promotor self-service**
   - Låt promotors själva bjuda in andra promotors
   - Hantera sina egna serier/events utan admin-inblandning

---

## 10. FRÅGOR TILL JALLE

1. **Ska `editor`-rollen finnas kvar?**
   - Den nämns i schema.sql men används inte i koden
   - Om den ska bort, kan databas-migrering behövas

2. **Vilka funktioner ska promotors ha tillgång till som de inte har idag?**
   - Ska de kunna skapa nya events själva?
   - Ska de ha tillgång till import-funktioner?
   - Ska de kunna hantera klasser för sina events?

3. **Hur ska sponsorhantering fungera för promotors?**
   - Just nu pekar sidebar på `sponsors.php` utan tydlig filtrering
   - Ska de bara se/hantera sponsorer för sina egna events?

4. **Ska det finnas fler roller?**
   - T.ex. `club_admin` (klubbansvarig) är delvis implementerat via `club_admins`-tabellen
   - Ska detta vara en separat roll eller fortsätta vara en "permission"?

5. **Vilken navigationsfil ska vara master?**
   - `sidebar.php` verkar vara primär nu
   - Ska de andra tas bort eller behållas för bakåtkompatibilitet?

6. **Vad är status på Elimination/Dual Slalom?**
   - Finns fullständig implementation
   - Används den aktivt? Behöver den dokumenteras mer?

---

## APPENDIX A: ALLA ADMIN-FILER

```
admin/
├── api/                          # API-endpoints
├── archived/                     # Arkiverade/oanvända filer
├── assets/                       # Admin-specifika assets
├── components/                   # Layout-komponenter
│   ├── admin-mobile-nav.php
│   ├── admin-sidebar.php
│   ├── unified-layout.php
│   └── unified-layout-footer.php
├── migrations/                   # Databasmigrationer
├── tools/                        # Verktygs-scripts
│
├── dashboard.php                 # Admin-översikt
├── login.php                     # Inloggning
├── logout.php                    # Utloggning
│
├── events.php                    # Event-lista
├── event-create.php              # Skapa event
├── event-edit.php                # Redigera event
├── event-delete.php              # Ta bort event
├── event-map.php                 # Event-karta (GPX)
├── event-economy.php             # Event-ekonomi
├── event-orders.php              # Event-beställningar
├── event-payment.php             # Event-betalning
├── event-pricing.php             # Event-prissättning
├── event-registrations.php       # Event-anmälningar
├── event-tickets.php             # Event-biljetter
│
├── series.php                    # Serie-lista
├── series-edit.php               # Redigera serie
├── series-events.php             # Serie-events och poäng
├── series-manage.php             # Serie-hantering
├── series-pricing.php            # Serie-prissättning
├── series-registrations.php      # Serie-anmälningar (säsongspass)
├── series-brands.php             # Serie-varumärken
│
├── riders.php                    # Deltagar-lista
├── rider-edit.php                # Redigera deltagare
├── rider-claims.php              # Profilkrav (claim rider)
├── rider-delete.php              # Ta bort deltagare
│
├── clubs.php                     # Klubb-lista
├── club-edit.php                 # Redigera klubb
├── club-admins.php               # Klubb-administratörer
├── club-points.php               # Klubb-poäng
│
├── results.php                   # Resultat-översikt
├── edit-results.php              # Redigera resultat
├── quick-edit-results.php        # Snabbredigering
│
├── users.php                     # Användar-lista [super_admin]
├── user-edit.php                 # Redigera användare [super_admin]
├── user-events.php               # Tilldela events till användare
│
├── promotor.php                  # Promotor-panel
├── promotor-registrations.php    # Promotor: anmälningar
├── promotor-payments.php         # Promotor: betalningar
├── promotor-series.php           # Promotor: serie-inställningar
│
├── ekonomi.php                   # Ekonomi-översikt
├── orders.php                    # Beställningar
├── payment-settings.php          # Betalningsinställningar
├── payment-recipients.php        # Betalningsmottagare
├── gateway-settings.php          # Gateway-inställningar
├── certificates.php              # Swish-certifikat
├── swish-accounts.php            # Swish-konton
├── discount-codes.php            # Rabattkoder
├── pricing-templates.php         # Prismallar
├── refund-requests.php           # Återbetalningar
│
├── classes.php                   # Klass-hantering
├── license-class-matrix.php      # Licens-matris
├── point-scales.php              # Poängskalor
├── point-templates.php           # Poängmallar
├── registration-rules.php        # Anmälningsregler
│
├── sponsors.php                  # Sponsor-hantering
├── sponsor-placements.php        # Sponsor-placeringar
├── media.php                     # Mediabibliotek
├── branding.php                  # Branding-inställningar [super_admin]
│
├── import.php                    # Import-översikt
├── import-riders.php             # Import deltagare
├── import-results.php            # Import resultat
├── import-events.php             # Import events
├── import-uci.php                # Import UCI
├── import-history.php            # Import-historik
│
├── elimination.php               # Elimination-översikt
├── elimination-manage.php        # Hantera brackets
├── elimination-live.php          # Live-uppdatering
│
├── ranking.php                   # Ranking-hantering
├── rebuild-stats.php             # Bygg om statistik
│
├── venues.php                    # Anläggningar
├── venue-edit.php                # Redigera anläggning
│
├── settings.php                  # Inställningar [super_admin]
├── system-settings.php           # Systeminställningar [super_admin]
├── role-management.php           # Roller [super_admin]
├── role-permissions.php          # Behörigheter [super_admin]
├── global-texts.php              # Globala texter
├── public-settings.php           # Publika inställningar
│
├── tools.php                     # Verktyg [super_admin]
├── run-migrations.php            # Köra migrationer [super_admin]
├── find-duplicates.php           # Hitta dubletter
├── cleanup-duplicates.php        # Rensa dubletter
├── cleanup-clubs.php             # Rensa klubbar
└── ... (50+ fler verktygs/fix-filer)
```

---

## APPENDIX B: DATABAS-TABELLER FÖR ROLLER

### admin_users
```sql
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role ENUM('super_admin', 'admin', 'editor') DEFAULT 'editor',
    active BOOLEAN DEFAULT 1,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**OBS:** ENUM matchar inte koden - bör uppdateras till:
`ENUM('rider', 'promotor', 'admin', 'super_admin')`

### promotor_events
```sql
CREATE TABLE promotor_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    can_edit TINYINT(1) DEFAULT 1,
    can_manage_results TINYINT(1) DEFAULT 1,
    can_manage_registrations TINYINT(1) DEFAULT 1,
    can_manage_payments TINYINT(1) DEFAULT 0,
    granted_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_event (user_id, event_id)
);
```

### promotor_series
```sql
CREATE TABLE promotor_series (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    series_id INT NOT NULL,
    can_edit TINYINT(1) DEFAULT 1,
    can_manage_results TINYINT(1) DEFAULT 1,
    can_manage_registrations TINYINT(1) DEFAULT 1,
    granted_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_series (user_id, series_id)
);
```

### club_admins
```sql
CREATE TABLE club_admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    club_id INT NOT NULL,
    can_edit_profile TINYINT(1) DEFAULT 1,
    can_upload_logo TINYINT(1) DEFAULT 1,
    can_manage_members TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_club (user_id, club_id)
);
```

---

**END OF RAPPORT**
