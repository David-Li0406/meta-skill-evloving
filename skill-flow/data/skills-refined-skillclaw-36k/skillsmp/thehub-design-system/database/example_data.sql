-- ==========================================
-- EXEMPELDATA FÖR TheHUB
-- ==========================================

-- ==========================================
-- 1. KLUBBAR (Exempel)
-- ==========================================
INSERT INTO clubs (name, short_name, city, country, active) VALUES
('Uppsala Cykelklubb', 'UCC', 'Uppsala', 'Sverige', 1),
('Göteborg MTB', 'GMTB', 'Göteborg', 'Sverige', 1),
('Stockholm CK', 'SCK', 'Stockholm', 'Sverige', 1),
('Malmö Cykelklubb', 'MCC', 'Malmö', 'Sverige', 1),
('Åre Bike Park Team', 'ABPT', 'Åre', 'Sverige', 1),
('Team GravitySeries', 'TGS', 'Stockholm', 'Sverige', 1),
('CK Olympia', 'CKO', 'Göteborg', 'Sverige', 1),
('Team Sportson', 'TSP', 'Malmö', 'Sverige', 1),
('IFK Göteborg CK', 'IFKG', 'Göteborg', 'Sverige', 1),
('Cykelklubben Borås', 'CKB', 'Borås', 'Sverige', 1);

-- ==========================================
-- 2. KATEGORIER
-- ==========================================
INSERT INTO categories (name, gender, age_min, age_max, active) VALUES
('Elite Herr', 'M', 19, NULL, 1),
('Elite Dam', 'F', 19, NULL, 1),
('Junior Herr', 'M', 17, 18, 1),
('Junior Dam', 'F', 17, 18, 1),
('U17 Herr', 'M', 15, 16, 1),
('U17 Dam', 'F', 15, 16, 1),
('Master 35+', 'M', 35, NULL, 1),
('Master 35+ Dam', 'F', 35, NULL, 1);

-- ==========================================
-- 3. SERIER
-- ==========================================
INSERT INTO series (name, season, discipline, count_best_results, active, description) VALUES
('GravitySeries Enduro', 2025, 'Enduro', 4, 1, 'Nationell enduroserie med 6 deltävlingar. Bästa 4 resultat räknas.'),
('GravitySeries Downhill', 2025, 'Downhill', 4, 1, 'Nationell downhillserie. Både seeding och race ger poäng.'),
('Capital GravitySeries', 2025, 'Enduro', 3, 1, 'Regional enduroserie i Stockholmsområdet.'),
('Götaland GravitySeries', 2025, 'Enduro', 3, 1, 'Regional enduroserie i Götaland.'),
('Jämtland GravitySeries', 2025, 'Downhill', 3, 1, 'Regional downhillserie i Jämtland.'),
('Dalarna GravitySeries', 2025, 'Enduro', 3, 1, 'Regional enduroserie i Dalarna.');

-- ==========================================
-- 4. EVENTS
-- ==========================================
INSERT INTO events (name, event_date, location, event_type, discipline, status, max_participants, series_id) VALUES
('Järvsö Enduro #1', '2025-05-10', 'Järvsö Bergscykelpark', 'race', 'Enduro', 'upcoming', 150, 1),
('Åre DH #1', '2025-06-15', 'Åre Bike Park', 'race', 'Downhill', 'upcoming', 100, 2),
('Stockholm Enduro', '2025-05-25', 'Vallåsen Bike Park', 'race', 'Enduro', 'upcoming', 120, 3),
('Järvsö DH Finals 2024', '2024-09-15', 'Järvsö Bergscykelpark', 'race', 'Downhill', 'completed', 80, NULL),
('Gesunda Enduro', '2025-07-20', 'Gesunda Bike Park', 'race', 'Enduro', 'upcoming', 140, 6);

-- ==========================================
-- 5. DELTAGARE (Cyclists)
-- ==========================================
INSERT INTO cyclists (firstname, lastname, birth_year, gender, license_number, club_id, active) VALUES
('Johan', 'Andersson', 1995, 'M', 'SWE-2025-1001', 1, 1),
('Emma', 'Svensson', 1998, 'F', 'SWE-2025-1002', 2, 1),
('Erik', 'Nilsson', 2003, 'M', 'SWE-2025-1003', 3, 1),
('Lisa', 'Karlsson', 2004, 'F', 'SWE-2025-1004', 4, 1),
('Anders', 'Johansson', 1988, 'M', 'SWE-2025-1005', 5, 1),
('Sofia', 'Lundqvist', 1992, 'F', 'SWE-2025-1006', 1, 1),
('Marcus', 'Berg', 2005, 'M', 'SWE-2025-1007', 2, 1),
('Anna', 'Larsson', 1990, 'F', 'SWE-2025-1008', 3, 1),
('Oscar', 'Eriksson', 2002, 'M', 'SWE-2025-1009', 4, 1),
('Klara', 'Pettersson', 2006, 'F', 'SWE-2025-1010', 5, 1),
('Erik', 'Andersson', 1995, 'M', 'SWE-2025-1234', 6, 1),
('Anna', 'Karlsson', 1998, 'F', 'SWE-2025-2345', 7, 1),
('Johan', 'Svensson', 1992, 'M', 'SWE-2025-3456', 3, 1),
('Maria', 'Lindström', 1996, 'F', 'SWE-2025-4567', 8, 1),
('Peter', 'Nilsson', 1990, 'M', 'SWE-2025-5678', 9, 1),
('Lisa', 'Bergman', 1999, 'F', 'SWE-2025-6789', 6, 1);

-- ==========================================
-- 6. RESULTAT (Järvsö DH Finals 2024)
-- ==========================================

-- Hämta event_id för Järvsö DH Finals 2024
SET @event_2024 = (SELECT id FROM events WHERE name = 'Järvsö DH Finals 2024' LIMIT 1);
SET @category_elite_men = (SELECT id FROM categories WHERE name = 'Elite Herr' LIMIT 1);
SET @category_elite_women = (SELECT id FROM categories WHERE name = 'Elite Dam' LIMIT 1);

-- Elite Men resultat
INSERT INTO results (event_id, cyclist_id, category_id, position, finish_time, status, points) VALUES
(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Johan' AND lastname = 'Andersson' LIMIT 1),
  @category_elite_men, 1, '00:03:05.45', 'finished', 100),

(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Anders' AND lastname = 'Johansson' LIMIT 1),
  @category_elite_men, 2, '00:03:07.92', 'finished', 95),

(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Oscar' AND lastname = 'Eriksson' LIMIT 1),
  @category_elite_men, 3, '00:03:09.23', 'finished', 92),

(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Erik' AND lastname = 'Andersson' LIMIT 1),
  @category_elite_men, 4, '00:03:10.15', 'finished', 90),

(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Peter' AND lastname = 'Nilsson' LIMIT 1),
  @category_elite_men, 5, '00:03:11.78', 'finished', 88);

-- Elite Women resultat
INSERT INTO results (event_id, cyclist_id, category_id, position, finish_time, status, points) VALUES
(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Emma' AND lastname = 'Svensson' LIMIT 1),
  @category_elite_women, 1, '00:03:15.78', 'finished', 100),

(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Sofia' AND lastname = 'Lundqvist' LIMIT 1),
  @category_elite_women, 2, '00:03:18.34', 'finished', 95),

(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Anna' AND lastname = 'Larsson' LIMIT 1),
  @category_elite_women, 3, '00:03:21.12', 'finished', 92),

(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Anna' AND lastname = 'Karlsson' LIMIT 1),
  @category_elite_women, 4, '00:03:23.45', 'finished', 90),

(@event_2024,
  (SELECT id FROM cyclists WHERE firstname = 'Lisa' AND lastname = 'Bergman' LIMIT 1),
  @category_elite_women, 5, '00:03:25.67', 'finished', 88);
