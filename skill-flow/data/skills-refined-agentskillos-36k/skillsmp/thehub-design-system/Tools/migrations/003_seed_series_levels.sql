-- ============================================================================
-- SEED SERIES LEVELS
-- TheHUB Analytics Platform
-- Version: 1.0
--
-- Kategoriserar befintliga serier baserat pa namn.
-- ANPASSA DESSA QUERIES EFTER ERA FAKTISKA SERIENAMN!
--
-- Kor EFTER 002_series_extensions.php
-- ============================================================================

-- ============================================================================
-- NATIONELLA SERIER
-- Dessa ar de stora, rikstackande serierna
-- ============================================================================

UPDATE series SET series_level = 'national'
WHERE name LIKE '%SweCup%'
   OR name LIKE '%SWE Cup%'
   OR name LIKE '%Swedish Cup%';

UPDATE series SET series_level = 'national'
WHERE name LIKE '%ESS%'
   OR name LIKE '%Enduro Series Sweden%'
   OR name LIKE '%Enduro Sverige%';

-- ============================================================================
-- SM / MASTERSKAPSSERIER
-- ============================================================================

UPDATE series SET series_level = 'championship'
WHERE name LIKE '%SM%'
   OR name LIKE '%Svenska Masterskapen%'
   OR name LIKE '%Masterskapet%'
   OR name LIKE '%Championship%';

-- ============================================================================
-- REGIONALA SERIER
-- Storre regionala serier som fungerar som "feeder" till nationella
-- ============================================================================

UPDATE series SET series_level = 'regional', region = 'Stockholm'
WHERE name LIKE '%Capital%'
   OR name LIKE '%Stockholm%';

UPDATE series SET series_level = 'regional', region = 'Vastra Gotaland'
WHERE name LIKE '%Gotaland%'
   OR name LIKE '%GGS%'
   OR name LIKE '%Goteborg%';

UPDATE series SET series_level = 'regional', region = 'Jamtland'
WHERE name LIKE '%Jamtland%'
   OR name LIKE '%Are%';

UPDATE series SET series_level = 'regional', region = 'Skane'
WHERE name LIKE '%Skane%'
   OR name LIKE '%Syd%';

UPDATE series SET series_level = 'regional', region = 'Dalarna'
WHERE name LIKE '%Dalarna%'
   OR name LIKE '%Salen%'
   OR name LIKE '%Falun%';

-- ============================================================================
-- LOKALA SERIER
-- Mindre, lokala serier och klubbserier
-- ============================================================================

-- Alla som inte matchat nagot ovan blir lokala
UPDATE series SET series_level = 'local'
WHERE series_level IS NULL
   OR series_level = '';

-- ============================================================================
-- SPECIAL: GRAVITY SERIES (baserat pa ert system)
-- ============================================================================

-- GGS = Gotland/Gotaland Gravity Series
UPDATE series SET series_level = 'regional', region = 'Vastra Gotaland'
WHERE name LIKE '%GGS%'
   AND series_level != 'national';

-- GSS = Stockholm/Svealand Gravity Series
UPDATE series SET series_level = 'regional', region = 'Stockholm'
WHERE name LIKE '%GSS%'
   AND series_level != 'national';

-- GES = Ostra Gravity Series
UPDATE series SET series_level = 'regional', region = 'Ostra Sverige'
WHERE name LIKE '%GES%'
   AND series_level != 'national';

-- ============================================================================
-- PARENT SERIES MAPPNING
-- Koppla regionala serier till deras nationella motsvarighet
-- OBS: Anpassa serie-IDs efter er databas!
-- ============================================================================

-- Exempel: Koppla Capital Enduro till ESS (Enduro Series Sweden)
-- UPDATE series SET parent_series_id = (SELECT id FROM series WHERE name LIKE '%ESS%' LIMIT 1)
-- WHERE name LIKE '%Capital%';

-- Exempel: Koppla GGS till SweCup DH
-- UPDATE series SET parent_series_id = (SELECT id FROM series WHERE name LIKE '%SweCup DH%' LIMIT 1)
-- WHERE name LIKE '%GGS%';
