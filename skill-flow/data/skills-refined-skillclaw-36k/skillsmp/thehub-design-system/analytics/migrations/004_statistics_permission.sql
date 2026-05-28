-- =========================================================
-- TheHUB Analytics - Statistics Permission
-- Version: 1.0
--
-- Lagger till 'statistics' behörigheten så att
-- icke-super_admin användare kan få tillgång till Analytics
-- =========================================================

-- Lägg till statistics permission om den inte finns
INSERT INTO permissions (name, description, category)
SELECT 'statistics', 'Tillgång till Analytics Dashboard och rapporter', 'analytics'
WHERE NOT EXISTS (
    SELECT 1 FROM permissions WHERE name = 'statistics'
);

-- För att ge en roll (t.ex. admin) statistics-behörighet, kör:
-- INSERT INTO role_permissions (role, permission_id)
-- SELECT 'admin', id FROM permissions WHERE name = 'statistics';
