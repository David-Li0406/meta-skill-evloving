# Privacy and Data Protection - TheHUB

## Overview

TheHUB stores sensitive personal information about riders for administrative purposes and registration autofill features. This document outlines which data is PRIVATE and how it must be protected.

## Private Fields

The following fields in the `riders` table contain **STRICTLY CONFIDENTIAL** information:

### High Sensitivity (NEVER expose publicly)
- `address` - Street address
- `postal_code` - Postal code
- `phone` - Phone number
- `emergency_contact` - Emergency contact information

**Note:** The `personnummer` column has been removed from the database (2025-12-01). Personnummer is only used during CSV import to extract birth_year - it is never stored.

### Medium Sensitivity (Internal use only)
- `email` - Email address (only show to authenticated admins or rider themselves)
- `password` - Hashed password (never show)
- `password_reset_token` - Password reset tokens (never show)

## Allowed Public Fields

The following fields MAY be shown publicly on rider profile pages:

- `id` - Rider ID
- `firstname` - First name
- `lastname` - Last name
- `birth_year` - Birth year (for age calculation)
- `gender` - Gender (M/F)
- `club_id` / `club_name` - Club affiliation
- `team` - Team name
- `license_number` - UCI/SWE license number
- `license_type` - License type (e.g., "Master Men")
- `license_category` - License category
- `disciplines` - Disciplines (Road, MTB, Gravel, etc.)
- `license_year` - License year
- `city` - City (general location, NOT address)
- `country` - Country
- `district` - District/Region
- `active` - Active status
- Results and statistics

## Implementation Requirements

### Public Pages (riders.php, rider.php, etc.)

**MUST NOT include** private fields in SQL SELECT statements:

```php
// GOOD - Safe query
$rider = $db->getRow("
    SELECT
        r.id,
        r.firstname,
        r.lastname,
        r.birth_year,
        r.gender,
        r.club_id,
        c.name as club_name,
        r.license_number,
        r.license_type,
        r.city
    FROM riders r
    LEFT JOIN clubs c ON r.club_id = c.id
    WHERE r.id = ?
", [$riderId]);

// BAD - Exposes private data!
$rider = $db->getRow("SELECT * FROM riders WHERE id = ?", [$riderId]);
```

### Admin Pages

Admin pages MAY show private data, but should:
- Require authentication (`require_admin()`)
- Mark private fields visually
- Log access to sensitive data (future feature)

### API Endpoints

If creating APIs for autofill features:
- Require authentication
- Only return private data to the rider themselves (match user session to rider ID)
- Never expose private data in bulk exports

## Testing Checklist

Before deploying changes that touch rider data:

- [ ] Verify `riders.php` does NOT select private fields
- [ ] Verify `rider.php` does NOT display private fields
- [ ] Check any API endpoints for data leaks
- [ ] Ensure export functions exclude private data (unless admin export)
- [ ] Test that autofill features only work when authenticated

## Data Breach Response

If private data is accidentally exposed:

1. **Immediately** remove the exposure (update code, restart server)
2. Notify affected riders by email
3. Document the breach (what, when, who was affected)
4. Review code to prevent similar issues

## Compliance

This data protection approach follows:
- GDPR (General Data Protection Regulation)
- Swedish Data Protection Act (Dataskyddslagen)
- Swedish Personal Data Act (Personuppgiftslagen)

## Questions

Contact system administrator or data protection officer if unsure about data handling.

---

**Last Updated:** 2025-12-01
**Version:** 1.1

### Changelog
- 2025-12-01: Removed personnummer from private fields list (column dropped from database)
