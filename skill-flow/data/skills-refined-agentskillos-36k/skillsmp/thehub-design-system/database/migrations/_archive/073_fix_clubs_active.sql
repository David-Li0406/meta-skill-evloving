-- Fix clubs active status
-- Sets all clubs to active = 1

UPDATE clubs SET active = 1 WHERE active IS NULL OR active = 0;
