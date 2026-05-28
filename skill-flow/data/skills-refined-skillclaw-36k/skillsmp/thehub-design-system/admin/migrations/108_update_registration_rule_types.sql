-- Migration 108: Update registration rule types to match license matrix
-- Ensures consistency between registration-rules.php and license-class-matrix.php

-- First, clear existing rule types
DELETE FROM registration_rule_types WHERE 1=1;

-- Insert the three standard rule types
INSERT INTO registration_rule_types (code, name, description, is_system) VALUES
('national', 'Nationellt', 'Nationella tävlingar med strikta licensregler och full rankingpoäng', 1),
('sportmotion', 'Sportmotion', 'Sportmotion-event med 50% rankingpoäng', 1),
('motion', 'Motion', 'Motion-event utan rankingpoäng, öppet för alla', 1);

-- Update any series that had old rule type IDs
UPDATE series SET registration_rule_type_id = NULL WHERE registration_rule_type_id NOT IN (SELECT id FROM registration_rule_types);
