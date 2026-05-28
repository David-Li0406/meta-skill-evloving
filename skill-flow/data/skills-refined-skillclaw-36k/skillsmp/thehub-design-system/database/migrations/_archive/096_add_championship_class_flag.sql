-- Migration: 096_add_championship_class_flag
-- Description: Add flag to specify which classes award SM medals at championship events
-- Date: 2026-01-05

-- Add is_championship_class column to classes table
-- Only classes with this flag will award SM medals at championship events
ALTER TABLE classes ADD COLUMN IF NOT EXISTS is_championship_class TINYINT(1) DEFAULT 0
    COMMENT 'If 1, wins in this class at championship events count as SM titles';

-- By default, set main classes (not "motion", "kids", "open" etc) to championship classes
-- Admin can adjust this in the classes admin panel
UPDATE classes SET is_championship_class = 1
WHERE (name NOT LIKE '%motion%'
   AND name NOT LIKE '%motions%'
   AND name NOT LIKE '%barn%'
   AND name NOT LIKE '%kids%'
   AND name NOT LIKE '%open%'
   AND name NOT LIKE '%öppen%'
   AND name NOT LIKE '%nybörjar%'
   AND name NOT LIKE '%fun%'
   AND name NOT LIKE '%intro%')
   AND awards_points = 1;
