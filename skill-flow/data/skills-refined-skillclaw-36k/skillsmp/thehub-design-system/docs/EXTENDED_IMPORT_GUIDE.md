# Extended Rider Import Guide

## Overview

TheHUB now supports importing complete rider data including private information for administrative purposes and registration autofill features. This guide explains how to use the extended import functionality.

## Quick Start

### Step 1: Run Database Migration

Before using the extended import, you must add the new database fields:

1. Log in to TheHUB admin
2. Navigate to: `/admin/run-migration-extended-riders.php`
3. The migration will add these fields:
   - `address` - Street address
   - `postal_code` - Postal code
   - `country` - Country
   - `emergency_contact` - Emergency contact
   - `district` - District/Region
   - `team` - Team name
   - `disciplines` - Multiple disciplines (JSON)
   - `license_year` - License year

### Step 2: Prepare Your CSV File

Use the following column format (tab-separated, semicolon-separated, or comma-separated):

```
Födelsedatum	Förnamn	Efternamn	Postadress	Postnummer	Ort	Land	Epostadress	Telefon	Emergency contact	Distrikt	Huvudförening	Road	Track	BMX	CX	Trial	Para	MTB	E-cycling	Gravel	Kategori	Licenstyp	LicensÅr	UCIKod	Team
```

**Example row:**
```
19400525-0651	Lars	Nordenson	När Andarve 358	62348	Stånga	Sverige	ernorde@gmail.com		Helen Nordenson, +46709609560	Smålands Cykelförbund	Ringmurens Cykelklubb	Road								Gravel	Men	Master Men	2025	101 637 581 11
```

See `example_extended_import.csv` for a complete example file.

### Step 3: Import the Data

1. Navigate to: `/admin/import-riders-extended.php`
2. Select your CSV file
3. Click "Importera"
4. Review the import statistics

## Column Descriptions

### Required Fields

| Column | Description | Example |
|--------|-------------|---------|
| **Förnamn** | First name | Lars |
| **Efternamn** | Last name | Nordenson |

### Personal Information (PRIVATE)

| Column | Description | Example |
|--------|-------------|---------|
| **Födelsedatum** | Personal number (YYYYMMDD-XXXX) - **Parsed to birth_year only, NOT stored** | 19400525-0651 |
| **Postadress** | Street address | När Andarve 358 |
| **Postnummer** | Postal code | 62348 |
| **Ort** | City | Stånga |
| **Land** | Country | Sverige |
| **Epostadress** | Email address | ernorde@gmail.com |
| **Telefon** | Phone number | 070-1234567 |
| **Emergency contact** | Emergency contact (name + phone) | Helen Nordenson, +46709609560 |

### Organization

| Column | Description | Example |
|--------|-------------|---------|
| **Distrikt** | District federation | Smålands Cykelförbund |
| **Huvudförening** | Club/Association | Ringmurens Cykelklubb |
| **Team** | Team name (if different from club) | Team GravitySeries |

### Disciplines

Mark disciplines with any value (leave empty for no):

| Column | Description |
|--------|-------------|
| **Road** | Road cycling |
| **Track** | Track cycling |
| **BMX** | BMX |
| **CX** | Cyclocross |
| **Trial** | Trial |
| **Para** | Para-cycling |
| **MTB** | Mountain biking |
| **E-cycling** | E-cycling |
| **Gravel** | Gravel cycling |

**Example:** To indicate a rider does Road and Gravel, put "Road" in the Road column and "Gravel" in the Gravel column. Leave other discipline columns empty.

### License Information

| Column | Description | Example |
|--------|-------------|---------|
| **Kategori** | License category | Men |
| **Licenstyp** | License type | Master Men |
| **LicensÅr** | License year | 2025 |
| **UCIKod** | UCI ID number | 101 637 581 11 |

## Privacy & Security

### IMPORTANT: Private Data Protection

The following fields are **STRICTLY CONFIDENTIAL** and must never be exposed publicly:

- Postadress (Address)
- Postnummer (Postal code)
- Telefon (Phone)
- Emergency contact

**Note:** Personnummer is **NOT stored** in the database. It is only used during import to extract the birth_year.

### Allowed Uses

Private data may ONLY be used for:
1. Internal administration
2. Auto-filling registration forms (for the rider themselves)
3. Emergency contact purposes

### Public Display

Public pages (riders.php, rider.php) will NEVER show:
- Addresses
- Phone numbers
- Emergency contacts

These fields are only visible to authenticated administrators.

## Duplicate Handling

The import will check for duplicates using:
1. **UCI Code** (if provided)
2. **Name + Birth year** (as fallback)

If a duplicate is found, the existing rider record will be **updated** with new data.

## Tips

1. **Encoding:** Save your CSV file in UTF-8 encoding to preserve Swedish characters (å, ä, ö)

2. **Separators:** The import auto-detects tab, semicolon (;), or comma (,) separators

3. **Empty Fields:** Leave fields empty if data is not available (don't use "N/A" or "-")

4. **Disciplines:** To mark a discipline as active, put any non-empty value in the column. The exact value doesn't matter.

5. **Personnummer:** The birth year will be automatically extracted from personnummer if provided. **Note: Only birth_year is stored - personnummer is NOT stored in the database.**

6. **Testing:** Start with a small test file (2-3 riders) before importing large datasets

## Troubleshooting

### Import fails with "Missing fields"
- Check that Förnamn and Efternamn are present in all rows
- Verify column headers match expected names

### Duplicate errors
- Check for duplicate rows in your CSV file
- Look for riders with the same UCI Code or name+birth_year combination

### Wrong separator detected
- Ensure consistent use of separator throughout the file
- Don't mix tabs, semicolons, and commas

### Swedish characters appear wrong
- Save file as UTF-8 encoding
- Check that your text editor supports UTF-8

## Support

For questions about:
- **Privacy/GDPR compliance:** See `PRIVACY.md`
- **Database structure:** See `database/schema.sql`
- **Regular import:** Use `/admin/import-riders.php` for basic imports without private data

## Example CSV

See `docs/example_extended_import.csv` for a complete example file with 3 sample riders.

---

**Last Updated:** 2025-12-01
**Version:** 1.1

### Changelog
- 2025-12-01: Removed personnummer storage - only birth_year is extracted and stored
