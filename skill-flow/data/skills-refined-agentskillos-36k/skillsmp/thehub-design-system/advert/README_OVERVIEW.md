# TheHUB - Global Sponsor & Race Reports System
## Översikt och Sammanfattning

Detta är en komplett lösning för att hantera globala sponsorer och race reports (blogginlägg) på TheHUB.

---

## 📦 Vad ingår i leveransen

### 1. Databas-struktur
**Fil:** `100_global_sponsors_system.sql`

**Nya tabeller:**
- `sponsor_placements` - Styr var sponsorer visas globalt
- `sponsor_tier_benefits` - Definierar rättigheter per nivå
- `race_reports` - Huvudtabell för race reports
- `race_report_tags` - Taggar för kategorisering
- `race_report_tag_relations` - Kopplingstabell reports-tags
- `race_report_comments` - Kommentarer med svar-funktion
- `race_report_likes` - Gillamarkeringar
- `sponsor_analytics` - Detaljerad tracking
- `sponsor_settings` - Systemkonfiguration

**Modifieringar:**
- Utökade `sponsors`-tabellen med nya tiers och global-flagga
- Bevarar befintliga `event_sponsors` och `series_sponsors`

### 2. PHP-klasser
**Fil:** `GlobalSponsorManager.php`

**Huvudfunktioner:**
- `getSponsorsForPlacement()` - Hämta sponsorer för specifik plats
- `getTitleSponsor()` - Hämta GravitySeries titelsponsor
- `getSeriesTitleSponsor()` - Hämta titelsponsor för serie
- `trackImpression()` - Registrera visning
- `trackClick()` - Registrera klick
- `renderSponsor()` - Generera HTML för sponsor
- `renderSection()` - Rendera hel sponsor-sektion
- `getSponsorStats()` - Hämta statistik
- `generateReport()` - Generera rapport för admin

**Fil:** `RaceReportManager.php`

**Huvudfunktioner:**
- `createReport()` - Skapa nytt race report
- `updateReport()` - Uppdatera befintligt
- `getReport()` - Hämta enskilt report
- `listReports()` - Lista med filtrering/paginering
- `addComment()` - Lägg till kommentar
- `getComments()` - Hämta kommentarer (träd-struktur)
- `toggleLike()` - Like/unlike funktion
- Auto-generering av excerpt, slug, läs-tid
- Instagram-integration (förbered för auto-import)

### 3. CSS-styling
**Fil:** `sponsor-blog-system.css`

**Omfattar:**
- Sponsor-sektioner (alla positioner)
- Sponsor-grid layouts (responsive)
- Tier-specifik styling (färgkodning)
- Race report cards (featured + standard)
- Single report view
- Kommentars-system
- Like-knappar
- Filters och paginering
- Admin-gränssnitt (placement matrix, stats dashboard)
- Mobil-anpassning

### 4. API Endpoints
**Fil:** `api-sponsors-tracking.php`

**Endpoints:**
- `POST /api/sponsors/track-impression` - Tracka visning
- `POST /api/sponsors/track-click` - Tracka klick
- `GET /api/sponsors/get-stats` - Hämta statistik (admin)

### 5. Dokumentation
**Fil:** `IMPLEMENTATIONSGUIDE.md`

**Innehåller:**
- Steg-för-steg installation
- Kodexempel för alla sidor
- Admin-gränssnitt guide
- JavaScript tracking-kod
- Prissättnings-exempel
- Framtida utveckling

---

## 🎯 Sponsornivåer och rättigheter

### Titelsponsor GravitySeries (högst)
**Rekommenderat pris:** 200.000 kr/år
- Varumärke i GravitySeries logotyp
- Exklusiv startsidesplacering (header banner)
- Header-placering alla sidor
- Integration i tröjor/priser
- Max 10 sponsorplatser
- Dedikerad analytics

### Titelsponsor Serie
**Rekommenderat pris:** 75.000 kr/år per serie
- Varumärke i serienamn (ex: "Sponsor X-cupen")
- Banner på seriesidor
- Branding på seriers evenemang
- Max 5 sponsorplatser

### Guldsponsor
**Rekommenderat pris:** 40.000 kr/år
- Sidebar startsida
- Alla resultsidor
- Ranking sidebar
- Max 3 sponsorplatser

### Silversponsor
**Rekommenderat pris:** 20.000 kr/år
- Valda sidor
- Content bottom
- Max 2 sponsorplatser

### Branschsponsor
**Rekommenderat pris:** 10.000 kr/år
- Databas sidebar (perfekt för cykelbutiker/verkstäder)
- Footer rotation
- Max 2 sponsorplatser

---

## 📍 Sponsorplaceringar per sidtyp

### Startsida (home)
- `header_banner` - Stor banner överst (endast titelsponsor)
- `sidebar_top` - Sidebar topp
- `content_bottom` - Under huvudinnehåll
- `footer` - Footer rotation

### Resultat (results)
- `sidebar_top` - Sidebar
- `content_mid` - Mellan resultat-sektioner

### Serieoversikt (series_list)
- `content_top` - Över serie-grid
- `sidebar_mid` - Sidebar

### Enskild serie (series_single)
- `header_banner` - Serie-titelsponsor banner
- `sidebar_mid` - Sidebar
- `content_bottom` - Under ställningar

### Databas (database - riders/clubs)
- `sidebar_top` - Branschsponsorer (relevant!)
- `content_bottom` - Under databas-innehåll

### Ranking (ranking)
- `sidebar_mid` - Sidebar
- `content_bottom` - Under rankinglistor

### Kalender (calendar)
- `sidebar_top` - Sidebar
- `content_mid` - Mellan events

### Blogg/Race Reports (blog)
- `sidebar_top` - Sidebar
- `content_bottom` - Under inlägg

---

## 🎨 Race Reports / Blogg-funktioner

### För deltagare
- Skriva race reports direkt i TheHUB
- Länka till event (optional)
- Ladda upp bilder
- Importera från Instagram (förbered för auto-import)
- Taggar för kategorisering
- Draft/Published/Archived status
- Kommentars-funktion
- Like-funktion
- Visa statistik (visningar, likes)

### För besökare
- Bläddra alla race reports
- Filtrera på tag, deltagare, event
- Sortera: senaste, populära, mest gillad
- Featured reports på startsidan
- Kommentera (kräver inloggning)
- Gilla inlägg
- Dela på sociala medier

### För admin
- Moderera race reports
- Markera featured reports
- Hantera tags
- Moderera kommentarer
- Visa statistik (views, engagement)

---

## 📊 Analytics & Rapportering

### Sponsor Analytics
Varje sponsor får tillgång till:
- **Impressions** - Antal visningar
- **Clicks** - Antal klick
- **Unique Sessions** - Unika besökare
- **CTR** (Click-Through Rate) - Klick/Visningar ratio
- **Daglig breakdown** - Detaljerad data per dag
- **Placement performance** - Vilka platser fungerar bäst
- **Tid på sidan** - Engagement-data

### Race Report Analytics
- Views per report
- Likes per report
- Kommentars-aktivitet
- Populäraste taggar
- Mest lästa författare
- Genomsnittlig läs-tid

---

## 🔧 Tekniska detaljer

### Kompatibilitet
- Bygger på befintlig TheHUB-struktur
- Utökar `sponsors`-tabellen utan att bryta befintlig funktionalitet
- Bevarar `event_sponsors` och `series_sponsors`
- Använder samma design tokens och CSS-variabler

### Performance
- Indexerade queries för snabb hämtning
- Lazy loading av sponsorbilder
- Intersection Observer för smart tracking
- Caching-vänlig struktur
- Optimerad för 1000+ riders och 100+ events

### Security
- Prepared statements (SQL injection-säkert)
- XSS-skydd via htmlspecialchars()
- CSRF-skydd för formulär
- Session-baserad autentisering
- Rate limiting på tracking

### SEO
- Semantisk HTML
- Open Graph tags (förberett)
- Strukturerad data (Schema.org)
- SEO-vänliga URLs (slugs)
- Meta descriptions auto-genererade

---

## 🚀 Installation

### Steg 1: Databas
```bash
mysql -u root -p thehub_db < 100_global_sponsors_system.sql
```

### Steg 2: PHP-filer
Kopiera till rätt platser:
- `GlobalSponsorManager.php` → `/includes/`
- `RaceReportManager.php` → `/includes/`
- `api-sponsors-tracking.php` → `/api/sponsors/tracking.php`

### Steg 3: CSS
Kopiera till:
- `sponsor-blog-system.css` → `/assets/css/`

Inkludera i `<head>`:
```html
<link rel="stylesheet" href="/assets/css/sponsor-blog-system.css">
```

### Steg 4: Initiera i config
I `config.php` eller motsvarande:
```php
require_once __DIR__ . '/includes/GlobalSponsorManager.php';
require_once __DIR__ . '/includes/RaceReportManager.php';

$globalSponsors = new GlobalSponsorManager($db);
$raceReports = new RaceReportManager($db);
```

### Steg 5: Lägg till på sidor
Se `IMPLEMENTATIONSGUIDE.md` för exakt kod per sida.

---

## 📋 Checklista för lansering

### Innan lansering
- [ ] Kör databas-migration
- [ ] Testa alla sponsorplaceringar
- [ ] Skapa test-sponsors för alla tiers
- [ ] Skapa test race reports
- [ ] Testa kommentars-funktion
- [ ] Testa like-funktion
- [ ] Verifiera tracking fungerar
- [ ] Mobil-testa alla sidor
- [ ] SEO-optimera race reports
- [ ] Skapa admin-dokumentation

### Efter lansering
- [ ] Sätt upp Instagram API (optional)
- [ ] Konfigurera email-notiser
- [ ] Skapa RSS-feed
- [ ] Implementera newsletter-integration
- [ ] Träna admin-användare
- [ ] Börja sälja sponsorpaket!

---

## 💡 Försäljningsargument

### Till sponsorer
1. **Synlighet** - Hela TheHUB-plattformen, 1000+ licensierade
2. **Målgrupp** - Dedikerade cyklister (köpstarka)
3. **Analytics** - Full transparens på ROI
4. **Flexibilitet** - Olika nivåer för olika budgetar
5. **Long-term** - Hela säsongskontakt

### Till deltagare
1. **Dela upplevelser** - Berätta din historia
2. **Community** - Bygg engagemang
3. **Synlighet** - Exponering i communityt
4. **Portfolio** - Visa upp dina prestationer
5. **Instagram-integration** - Enkel publicering

---

## 🔮 Framtida utveckling

### Fas 2 (3-6 månader)
- Instagram Auto-Import API
- Email-notiser vid nya reports
- RSS-feed för race reports
- Newsletter-integration
- Avancerad sponsor ROI-dashboard
- A/B-testing av sponsorplaceringar

### Fas 3 (6-12 månader)
- Video race reports
- Live race blogging
- Sponsor-specifika landningssidor
- Programmatic ad server
- Machine learning för optimal placering
- Mobil app för race reporting

---

## ❓ Vanliga frågor

**Q: Kan sponsorer själva hantera sina placeringar?**
A: Ja, kan implementeras via dedikerat sponsor-portal (rekommenderat fas 2).

**Q: Kostar det för deltagare att blogga?**
A: Nej, helt gratis för alla licensierade riders.

**Q: Kan man moderera race reports innan publicering?**
A: Ja, inställning finns i `sponsor_settings` tabellen.

**Q: Hur hanteras GDPR?**
A: Analytics hashar IP-adresser, ingen persondata sparas utan samtycke.

**Q: Kan man ha flera titelsponsorer?**
A: GravitySeries kan bara ha EN, men varje serie kan ha sin egen titelsponsor.

---

## 📞 Support

För frågor eller support, kontakta utvecklare.

**Lycka till med lanseringen! 🚴‍♂️💨**
