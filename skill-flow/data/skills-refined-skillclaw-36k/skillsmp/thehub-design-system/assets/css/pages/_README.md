# Page-Specific CSS

Denna katalog innehaller sid-specifik CSS som laddas villkorligt baserat pa vilken sida som visas.

## Hur det fungerar

1. CSS-filer namnges efter routerns `$pageInfo['page']` varde
2. `components/head.php` laddar automatiskt ratt fil om den finns
3. Inline CSS i PHP-filer kan gradvis flyttas hit

## Filnamnskonvention (VIKTIGT!)

Routern (`router.php`) satter sidnamn enligt formatet `{section}-{subpage}`.

### Section Routes (vanligast)

| URL | `$pageInfo['page']` | CSS-fil |
|-----|---------------------|---------|
| `/results` | `results-index` | `results-index.css` |
| `/results/123` | `results-event` | `results-event.css` |
| `/calendar` | `calendar-index` | `calendar-index.css` |
| `/calendar/123` | `calendar-event` | `calendar-event.css` |
| `/database` | `database-index` | `database-index.css` |
| `/database/rider/123` | `database-rider` | `database-rider.css` |
| `/profile` | `profile-index` | `profile-index.css` |
| `/profile/edit` | `profile-edit` | `profile-edit.css` |
| `/ranking` | `ranking-index` | `ranking-index.css` |
| `/series` | `series-index` | `series-index.css` |
| `/series/123` | `series-show` | `series-show.css` |

### Legacy Single Pages

| URL | `$pageInfo['page']` | CSS-fil |
|-----|---------------------|---------|
| `/event/123` | `event` | `event.css` |
| `/rider/123` | `rider` | `rider.css` |
| `/club/123` | `club` | `club.css` |

### Simple Pages

| URL | `$pageInfo['page']` | CSS-fil |
|-----|---------------------|---------|
| `/login` | `login` | `login.css` |
| `/checkout` | `checkout` | `checkout.css` |
| `/` | `welcome` | `welcome.css` |

## Migrerade sidor

- [x] `results-index.css` - Migrerad 2025-12-14

## Migrationsprocess

1. Kontrollera routerns `$pageInfo['page']` for sidan (se tabellen ovan)
2. Skapa CSS-fil med exakt samma namn + `.css`
3. Kopiera inline `<style>` fran PHP-filen till CSS-filen
4. Testa att sidan ser likadan ut
5. Ta bort inline CSS fran PHP-filen
6. Markera som migrerad i denna README

## Debug Tips

Om CSS inte laddas, lagg till i `components/head.php`:
```php
echo "<!-- Page CSS Loader: page='" . htmlspecialchars($currentPage ?? 'null') . "' -->\n";
```

## Viktigt

- Anvand CSS-variabler fran tokens.css
- Folj CLAUDE-CSS.md for alla stilregler
- Testa pa mobil, tablet och desktop
