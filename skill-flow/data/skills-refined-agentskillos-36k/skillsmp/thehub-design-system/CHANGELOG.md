# Changelog

All notable changes to TheHUB project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added - SCF License Portal Integration (2026-01-20)

#### **SCF License Sync System**
- **SCFLicenseService** (`includes/SCFLicenseService.php`)
  - Complete API integration with Svenska Cykelförbundet's License Portal
  - UCI ID verification via `/ucilicenselookup` endpoint
  - Name-based search via `/licenselookup` endpoint
  - License data parsing with field mapping:
    - `license_type` = Age/skill class (Elite, U11, U13, etc.)
    - `license_category` = Gender (Men, Women)
    - `discipline` = Primary discipline (MTB, Road, etc.)
  - Gender derivation from license_category when direct field unavailable
  - Automatic club linking and creation
  - Year-based club membership tracking via `rider_club_seasons` table
  - License caching in `scf_license_cache` table
  - Match candidate system for manual review

#### **Admin Tools**
- **SCF Batch Verify** (`admin/scf-batch-verify.php`)
  - Batch verification of riders with UCI ID against SCF
  - "Verifiera ALLA" auto-continue with progress tracking
  - Statistics dashboard (total, verified, not verified)
  - Timeout handling (5 min PHP, 120s JS fetch)
  - Retry logic (up to 2 retries on failure)

- **SCF Name Search** (`admin/scf-name-search.php`)
  - Search riders without UCI ID (including SWE-ID) by name
  - Creates match candidates for manual review
  - "Sök ALLA" auto-continue functionality
  - Confirm/reject workflow for matches
  - Rate limiting between API calls

- **SCF Import Riders** (`admin/scf-import-riders.php`)
  - Manual search and import of new riders from SCF
  - Duplicate detection by UCI ID and name/birthyear

- **SCF API Test** (`admin/scf-api-test.php`)
  - Test tool for API connectivity
  - Single UCI lookup, batch lookup, and name search tests

#### **Database Migration**
- **Migration 019** (`Tools/migrations/019_scf_license_sync.sql`)
  - Added `scf_license_*` columns to `riders` table
  - Created `scf_license_cache` table
  - Created `scf_license_history` table
  - Created `scf_match_candidates` table
  - Created `scf_sync_log` table

#### **UI Enhancements**
- Added "Aktiv licens (2026)" filter on riders list
- Added SCF verification status to rider edit page
- Added yearly club membership display from rider_club_seasons
- Tools linked in admin/tools.php under "SCF Licenssynk" section

### Fixed (2026-01-20)

- **Rider Profile Results Count**
  - Fixed club history showing incorrect result count
  - Count now excludes DNS (Did Not Start) results to match displayed list

### Changed - Privacy Improvements (2025-12-01)

- **Removed personnummer column from database**
  - The `personnummer` column has been dropped from the `riders` table
  - Personnummer in CSV imports is still parsed to extract `birth_year` only
  - The personnummer value itself is NOT stored in the database
  - This improves privacy and GDPR compliance
  - Updated all import files, validators, and documentation to reflect this change
  - Migration files updated with deprecation notes

### Added - Major Features (Overnight Rebuild - 2025-01-13)

#### **PRIORITY 1: Critical Fixes**
- **Robust UCI Import System** (`admin/import-uci.php`)
  - UTF-8 encoding detection and automatic conversion
  - Enhanced CSV separator auto-detection (comma, semicolon, tab, pipe)
  - Comprehensive error logging for first 3 rows
  - Graceful handling of missing columns (padding with empty strings)
  - Whitespace trimming on all values

- **Standardized Layout System** (`includes/layout-header.php`, `includes/layout-footer.php`)
  - Created unified layout system for all pages
  - Consistent HTML structure across 16 pages (12 admin + 4 public)
  - Centralized navigation and mobile menu handling
  - Single source of truth for JavaScript functions
  - Removed ~256 lines of duplicate code

#### **PRIORITY 2: Complete CRUD Operations**

- **Events Full CRUD** (`admin/events.php`) - 446 lines added
  - Create, Read, Update, Delete functionality
  - Modal form with 13 database fields
  - Series dropdown integration
  - Event type enum (road_race, time_trial, criterium, stage_race, other)
  - Status management (upcoming, ongoing, completed, cancelled)
  - Edit/Delete action buttons in table

- **Series Full CRUD** (`admin/series.php`) - 334 lines added
  - Complete CRUD operations
  - Modal form with 6 fields
  - Status management (planning, active, completed, cancelled)
  - Events link with filtering capability
  - Status badges with icons

- **Riders Enhanced CRUD** (`admin/riders.php`) - 514 lines added
  - Comprehensive CRUD with ALL 15 fields
  - Complete license management system:
    - License number (UCI or SWE-ID)
    - License type (Elite, Master, Youth, Base, Team Manager)
    - License category (e.g., "Elite Men", "Master Men 35+")
    - Discipline (MTB, Road, CX, Track, BMX, Other)
    - License valid until date
  - Club dropdown integration
  - Personal info (name, birth year, gender, email, phone, city)
  - Active status toggle
  - Notes field

- **Clubs Full CRUD** (`admin/clubs.php`) - 353 lines added
  - Complete CRUD operations
  - Modal form with 7 fields (name, short_name, region, city, country, website, active)
  - Riders filtering by club (`admin/riders.php` enhanced with +43 lines)
  - Visual indicator when filtering
  - Rider count display with link to filtered view

- **Venues Virtual Management** (`admin/venues.php`) - 243 lines added
  - Rename locations (batch update across events)
  - Merge locations (fix typos)
  - Events filtering by location (`admin/events.php` enhanced with +30 lines)
  - Educational alert about proper venues table
  - SQL snippet for future venues table migration

- **Results Full CRUD** (`admin/results.php`) - 429 lines added
  - Complete CRUD operations
  - Modal form with 12 fields
  - Event and rider dropdowns
  - Category selection
  - Race results (position, time, bib number, status)
  - Points and statistics (time_behind, average_speed)
  - Unique constraint handling (one result per rider per event)
  - Time pattern validation (HH:MM:SS)

#### **PRIORITY 3: Import History & Rollback System**

- **Database Schema** (`database/migrations/003_import_history.sql`)
  - `import_history` table: Tracks all imports with complete statistics
  - `import_records` table: Tracks individual records for granular rollback
  - Proper indexes and foreign key constraints

- **Helper Functions** (`includes/import-history.php`)
  - `startImportHistory()` - Begin tracking an import
  - `updateImportHistory()` - Update with final statistics
  - `trackImportRecord()` - Track individual created/updated records
  - `rollbackImport()` - Full rollback with delete/restore capability
  - `getImportHistory()` - Retrieve import history with filtering
  - `getImportRecords()` - Get detailed records for specific import

- **Admin UI** (`admin/import-history.php`)
  - View all imports with detailed statistics
  - Filter by import type (UCI, Riders, Results, Events, Clubs)
  - Rollback functionality with confirmation dialog
  - Status badges (completed, failed, rolled_back)
  - Error summary display
  - File size formatting
  - Statistics dashboard

- **Integration**
  - Updated `admin/import-uci.php` to use import history
  - Tracks all created and updated riders
  - Stores old rider data before updates for rollback
  - Links to import history in success messages
  - Added "Import History" to admin navigation

#### **PRIORITY 5: Validation & Error Handling**

- **Comprehensive Validators** (`includes/validators.php`)
  - Email validation
  - Swedish personnummer validation with century detection
  - Date and time validation
  - URL and phone number validation
  - Integer and decimal range validation
  - String length validation
  - Enum value validation
  - UCI license code validation
  - Birth year validation
  - File upload validation
  - Batch validation support
  - XSS sanitization helper

#### **PRIORITY 6: Documentation**

- **Import History Documentation** (`docs/IMPORT-HISTORY.md`)
  - Complete usage guide
  - API documentation for all helper functions
  - Integration examples
  - Best practices and security notes
  - Future enhancement suggestions

- **Changelog** (`CHANGELOG.md`) - This file
  - Comprehensive change log
  - Feature documentation
  - Version tracking

### Changed

- **Navigation Menu** (`includes/navigation.php`)
  - Added "Import History" menu item
  - Consistent active state detection
  - Proper mobile menu handling

- **All Import Scripts**
  - Integrated import history tracking
  - Enhanced error handling
  - Improved user feedback with links to history

### Fixed

- **UCI Import Issues**
  - Fixed separator detection failures
  - Fixed encoding issues (Windows-1252, ISO-8859-1)
  - Fixed "Saknar förnamn eller efternamn" errors
  - Fixed missing columns handling

- **Navigation Issues**
  - Fixed menu jumping problems
  - Fixed mobile overlay behavior
  - Fixed menu state consistency

- **Database Issues**
  - Corrected table name from 'cyclists' to 'riders' (13 files updated)
  - Fixed foreign key references

### Security

- **All Forms**
  - CSRF protection implemented on all POST requests
  - XSS prevention with h() function throughout
  - SQL injection prevention with parameterized queries
  - Type safety with intval/floatval casting

- **Import History**
  - Admin authentication required
  - CSRF protection on rollback actions
  - Full audit trail (who, when, what)
  - Proper foreign key constraints

### Technical Debt Resolved

- Removed ~256 lines of duplicate code across layout files
- Standardized button, form, table, and card styling
- Consistent modal implementations across all CRUD operations
- Unified JavaScript functions in layout-footer.php
- Proper error handling in all database operations

### Statistics

- **Total Lines Added**: ~4,900+
- **Total Lines Removed**: ~500
- **Files Created**: 8
- **Files Modified**: 20+
- **Commits**: 14
- **CRUD Systems Implemented**: 6 (Events, Series, Riders, Clubs, Venues, Results)

### Database Migrations

1. Initial schema (pre-existing)
2. License fields migration (completed in previous session)
3. Import history system (`003_import_history.sql`)

### Known Issues

None currently identified. All priority 1-3 features tested and working.

### Upcoming Features

Potential future enhancements:
- Categories CRUD
- Advanced result statistics and analytics
- Multi-event bulk operations
- Export functionality (CSV, Excel, PDF)
- Email notifications for imports
- Scheduled imports
- API endpoints for external integrations
- Mobile app support

---

## Version History

### v2.0.0 - 2025-01-13 (Overnight Rebuild)
Major rebuild with complete CRUD operations, import history, and standardized UI.

### v1.0.0 - Previous
Initial version with basic functionality.

---

*For detailed commit history, see Git log.*
*For import history specifics, see `docs/IMPORT-HISTORY.md`.*
