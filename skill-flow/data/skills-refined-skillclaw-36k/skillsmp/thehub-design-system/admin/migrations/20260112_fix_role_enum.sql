-- Migration: Uppdatera role ENUM i admin_users
-- Datum: 2026-01-12
-- Syfte: Ersätt 'editor' med 'promotor', lägg till 'rider'
--
-- INSTRUKTIONER:
-- 1. SKAPA BACKUP FÖRST: mysqldump -u user -p database admin_users > admin_users_backup.sql
-- 2. Kör denna migration i phpMyAdmin eller MySQL CLI
-- 3. Verifiera med SELECT-frågan i slutet
--
-- VARNING: Denna migration ändrar ENUM-typen vilket kan ta tid på stora tabeller

-- ========================================
-- STEG 1: Kontrollera nuvarande data
-- ========================================
-- Kör denna först för att se vilka roller som finns:
-- SELECT role, COUNT(*) as count FROM admin_users GROUP BY role;

-- ========================================
-- STEG 2: Konvertera 'editor' till 'admin' (temporärt)
-- ========================================
-- Om det finns användare med role='editor', uppdatera dem först
UPDATE admin_users SET role = 'admin' WHERE role = 'editor';

-- ========================================
-- STEG 3: Ändra ENUM-typen
-- ========================================
-- Ny ENUM med korrekta roller enligt koden:
-- rider (1) - Vanlig användare
-- promotor (2) - Kan hantera tilldelade events/serier
-- admin (3) - Full admin-åtkomst (utom System)
-- super_admin (4) - Full åtkomst inklusive System

ALTER TABLE admin_users
MODIFY COLUMN role ENUM('rider', 'promotor', 'admin', 'super_admin')
NOT NULL DEFAULT 'rider';

-- ========================================
-- STEG 4: Verifiera ändringen
-- ========================================
-- Kör dessa för att verifiera:
SELECT role, COUNT(*) as count FROM admin_users GROUP BY role;
SHOW COLUMNS FROM admin_users LIKE 'role';

-- ========================================
-- ROLLBACK (om något går fel)
-- ========================================
-- ALTER TABLE admin_users
-- MODIFY COLUMN role ENUM('super_admin', 'admin', 'editor')
-- NOT NULL DEFAULT 'editor';
