# TheHUB - Komplett Menyträd

> Dokumentation av hela navigationsstrukturen för TheHUB-applikationen.
> Källa: `includes/navigation.php`

---

## Navigationsöversikt

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              TheHUB MENY                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════    │
│  PUBLIK SEKTION (Alla användare)                                            │
│  ═══════════════════════════════════════════════════════════════════════    │
│                                                                              │
│  🏠 Hem                    → /index.php                                      │
│  📅 Kalender               → /events.php                                     │
│  🏆 Resultat               → /results.php                                    │
│  🎖️ Serier                 → /series.php                                     │
│  👥 Deltagare              → /riders.php                                     │
│  🏆 Klubbar                → /clubs/leaderboard.php                          │
│  📈 Ranking                → /ranking/                                       │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════    │
│  ADMIN SEKTION (Inloggade användare)                                        │
│  ═══════════════════════════════════════════════════════════════════════    │
│                                                                              │
│  📊 Dashboard              → /admin/dashboard.php                            │
│  📅 Events                 → /admin/events.php                               │
│  🎫 Ticketing              → /admin/ticketing.php                            │
│  🎖️ Serier                 → /admin/series.php                               │
│  🛡️ Registreringsregler    → /admin/registration-rules.php                   │
│  👤 Deltagare              → /admin/riders.php                               │
│  🏢 Klubbar                → /admin/clubs.php                                │
│  🏆 Klubbpoäng             → /admin/club-points.php                          │
│  📈 Ranking                → /admin/ranking.php                              │
│  ⛰️ Venues                 → /admin/venues.php                               │
│  🏆 Resultat               → /admin/results.php                              │
│  📤 Import                 → /admin/import.php                               │
│  ⚙️ Publika Inställningar  → /admin/public-settings.php                      │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════    │
│  SYSTEM SEKTION (Endast Super Admin)                                        │
│  ═══════════════════════════════════════════════════════════════════════    │
│                                                                              │
│  👥 Användare              → /admin/users.php                                │
│  🛡️ Rollbehörigheter       → /admin/role-permissions.php                     │
│  ⚙️ Systeminställningar    → /admin/system-settings.php                      │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│  🚪 Logga ut               → /admin/logout.php                               │
│                                                                              │
│  ═══════════════════════════════════════════════════════════════════════    │
│  EJ INLOGGAD                                                                 │
│  ═══════════════════════════════════════════════════════════════════════    │
│                                                                              │
│  🔐 Admin Login            → /admin/login.php                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detaljerad Sidstruktur med Undersidor

### 1. Publika Sidor (/)

| Menypunkt | Huvudsida | Undersidor/Relaterade sidor |
|-----------|-----------|----------------------------|
| **Hem** | `/index.php` | - |
| **Kalender** | `/events.php` | → `/event.php` (event-detalj)<br>→ `/event-results.php` (event-resultat) |
| **Resultat** | `/results.php` | - |
| **Serier** | `/series.php` | → `/series-standings.php` (serieställningar) |
| **Deltagare** | `/riders.php` | → `/rider.php` (rider-profil publik) |
| **Klubbar** | `/clubs/leaderboard.php` | → `/clubs/detail.php` (klubb-detalj)<br>→ `/club.php` (klubb-sida) |
| **Ranking** | `/ranking/index.php` | → `/ranking/rider.php` (rider-ranking) |

---

### 2. Rider-Portal (Ej i huvudmeny)

| Sida | Sökväg | Beskrivning |
|------|--------|-------------|
| Rider-inloggning | `/rider-login.php` | Inloggningssida för riders |
| Rider-utloggning | `/rider-logout.php` | Loggar ut rider |
| Rider-registrering | `/rider-register.php` | Registrera ny rider |
| Rider-profil | `/rider-profile.php` | Profil för inloggad rider |
| Licensinformation | `/rider-license.php` | Visa/hantera licens |
| Byt lösenord | `/rider-change-password.php` | Byt lösenord |
| Återställ lösenord | `/rider-reset-password.php` | Återställ glömt lösenord |
| Mina biljetter | `/my-tickets.php` | Visa köpta biljetter |

---

### 3. Admin-Sidor (/admin/)

#### 📊 Dashboard

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/dashboard.php` | - |

---

#### 📅 Events

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/events.php` | → `/admin/event-create.php` (skapa event) |
| | → `/admin/event-edit.php` (redigera event) |
| | → `/admin/event-delete.php` (ta bort event) |
| | → `/admin/clear-event-results.php` (rensa resultat) |

---

#### 🎫 Ticketing

> **Meny-highlight:** Aktiv på 5 sidor (`ticketing.php`, `event-pricing.php`, `event-tickets.php`, `refund-requests.php`, `pricing-templates.php`)

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/ticketing.php` | → `/admin/event-pricing.php` (eventpriser) |
| | → `/admin/event-tickets.php` (eventbiljetter) |
| | → `/admin/event-ticketing.php` (event-biljetthantering) |
| | → `/admin/refund-requests.php` (återbetalningar) |
| | → `/admin/pricing-templates.php` (prismallar) |

---

#### 💳 Betalningar

> **Meny-highlight:** Aktiv på 2 sidor (`orders.php`, `payment-settings.php`)

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/orders.php` | → Ordrar & betalningsbekräftelse |
| `/admin/payment-settings.php` | → Swish-inställningar per event/serie |

---

#### 🎖️ Serier

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/series.php` | → `/admin/series-events.php` (serie-events) |
| | → `/admin/series-pricing.php` (seriepriser) |

---

#### 🛡️ Registreringsregler

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/registration-rules.php` | - |

---

#### 👤 Deltagare (Riders)

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/riders.php` | → `/admin/rider-edit.php` (redigera rider) |
| | → `/admin/rider-delete.php` (ta bort rider) |

---

#### 🏢 Klubbar

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/clubs.php` | → `/admin/club-edit.php` (redigera klubb) |
| | → `/admin/cleanup-clubs.php` (städa klubbar) |

---

#### 🏆 Klubbpoäng

> **Meny-highlight:** Aktiv på 2 sidor (`club-points.php`, `club-points-detail.php`)

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/club-points.php` | → `/admin/club-points-detail.php` (klubbpoäng-detalj) |

---

#### 📈 Ranking

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/ranking.php` | → `/admin/ranking-debug.php` (debug) |
| | → `/admin/ranking-minimal.php` (minimal) |
| | → `/admin/setup-ranking-system.php` (setup) |
| | → `/admin/point-scales.php` (poängskalor) |
| | → `/admin/point-scale-edit.php` (redigera skala) |
| | → `/admin/point-templates.php` (poängmallar) |

---

#### ⛰️ Venues

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/venues.php` | - |

---

#### 🏆 Resultat

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/results.php` | → `/admin/edit-results.php` (redigera resultat) |
| | → `/admin/recalculate-results.php` (räkna om resultat) |
| | → `/admin/reset-results.php` (återställ resultat) |

---

#### 📤 Import

> **Meny-highlight:** Aktiv på 2 sidor (`import.php`, `import-history.php`)

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/import.php` | → `/admin/import-history.php` (importhistorik) |
| | → `/admin/import-riders.php` (importera riders) |
| | → `/admin/import-riders-flexible.php` (flexibel import) |
| | → `/admin/import-riders-extended.php` (utökad import) |
| | → `/admin/import-results.php` (importera resultat) |
| | → `/admin/import-results-preview.php` (förhandsgranska) |
| | → `/admin/import-events.php` (importera events) |
| | → `/admin/import-series.php` (importera serier) |
| | → `/admin/import-classes.php` (importera klasser) |
| | → `/admin/import-clubs.php` (importera klubbar) |
| | → `/admin/import-uci-preview.php` (UCI-preview) |
| | → `/admin/import-uci-simple.php` (UCI enkel) |
| | → `/admin/import-gravity-id.php` (Gravity ID) |

---

#### ⚙️ Publika Inställningar

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/public-settings.php` | → `/admin/global-texts.php` (globala texter) |

---

### 4. System-Sidor (Endast Super Admin)

#### 👥 Användare

> **Meny-highlight:** Aktiv på 4 sidor (`users.php`, `user-edit.php`, `user-events.php`, `user-rider.php`)

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/users.php` | → `/admin/user-edit.php` (redigera användare) |
| | → `/admin/user-events.php` (användarens events) |
| | → `/admin/user-rider.php` (koppla rider) |

---

#### 🛡️ Rollbehörigheter

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/role-permissions.php` | - |

---

#### ⚙️ Systeminställningar

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/system-settings.php` | → `/admin/settings.php` (äldre inställningar) |
| | → `/admin/setup-database.php` (databas-setup) |
| | → `/admin/run-migrations.php` (migrationer) |

---

### 5. Klasser (Admin - ej i meny)

| Huvudsida | Undersidor |
|-----------|------------|
| `/admin/classes.php` | → `/admin/reassign-classes.php` |
| | → `/admin/reset-classes.php` |
| | → `/admin/move-class-results.php` |

---

## Sammanfattning

| Sektion | Antal huvudmenyalternativ | Totalt antal sidor |
|---------|---------------------------|-------------------|
| **Publik** | 7 | ~14 |
| **Admin** | 13 | ~50+ |
| **System** | 3 | ~8 |
| **Rider-portal** | 0 (ej i meny) | 8 |
| **Hjälp/Debug** | 0 (ej i meny) | ~20+ |

---

## Åtkomstnivåer

| Roll | Nivå | Åtkomst |
|------|------|---------|
| `super_admin` | 4 | Publik + Admin + System |
| `admin` | 3 | Publik + Admin |
| `promotor` | 2 | Publik + begränsad Admin (egna events) |
| `rider` | 1 | Publik + Rider-portal |
| (ej inloggad) | 0 | Publik endast |

---

## Teknisk Information

### Aktiv sida-detektion

Navigationen använder flera metoder för att markera aktiv sida:

```php
// Metod 1: Direkt sidnamn
$current_page == 'index.php'

// Metod 2: Flera sidnamn i array
in_array($current_page, ['ticketing.php', 'event-pricing.php', ...])

// Metod 3: Sökväg-kontroll (skilja admin från publik)
$current_page == 'events.php' && strpos($_SERVER['PHP_SELF'], '/admin/') === false

// Metod 4: Katalog-kontroll
strpos($_SERVER['PHP_SELF'], '/ranking/') !== false
```

### Ikoner

Systemet använder **Lucide Icons** via `data-lucide` attribut.

### CSS-klasser

- `gs-sidebar` - Huvudnavigation
- `gs-menu-section` - Menysektion
- `gs-main-menu` - Publik meny
- `gs-menu-title` - Sektionsrubrik
- `gs-menu` - Menylista

---

## Changelog

| Version | Datum | Beskrivning |
|---------|-------|-------------|
| 1.0 | 2025-11-27 | Initial dokumentation av befintlig menystruktur |
| 2.0 | 2025-11-27 | Omstrukturering till 5 grupper med fliknavigation |

---

## Version 2.0 - Ny Menystruktur

### Sidebar (5 huvudgrupper)

```
ADMIN SIDEBAR v2.0
├── 📊 Dashboard
├── 📅 Tävlingar         → [Events] [Resultat] [Venues] [Biljetter] [Betalningar]
├── 🎖️ Serier & Poäng    → [Serier] [Ranking] [Klubbpoäng] [Poängskalor]
├── 👥 Deltagare & Klubbar → [Deltagare] [Klubbar] [Klasser]
├── 📤 Import & Data     → [Översikt] [Riders] [Resultat] [Events] [UCI] [Historik]
└── ⚙️ Inställningar     → [Användare] [Behörigheter] [Publikt] [System]
```

### Nya filer i v2.0

| Fil | Beskrivning |
|-----|-------------|
| `/includes/components/admin-tabs.php` | Återanvändbar flik-komponent |
| `/includes/config/admin-tabs-config.php` | Konfiguration för alla flikgrupper |
| `/includes/admin-layout.php` | Layout-wrapper med flikar |
| `/public/css/components/_admin-tabs.css` | CSS för flikar (mobile-first) |

### Design-principer v2.0

- **Mobile-first:** Vertikala flikar på mobil, horisontella på desktop
- **Orientation-aware:** Anpassar sig till portrait/landscape
- **Touch targets:** Minst 44px på mobil
- **Ikoner + text:** Alltid båda på mobil för tillgänglighet
- **Desktop:** Endast text (ikoner dolda för renare design)

---

*Senast uppdaterad: 2025-12-05*
