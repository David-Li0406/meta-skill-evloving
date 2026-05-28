-- Migration: Add invitation global text entry
-- Date: 2025-12-16

-- Add invitation global text if not exists
INSERT INTO global_texts (field_key, field_name, field_category, content, sort_order)
SELECT 'invitation', 'Inbjudan', 'general', '', 0
WHERE NOT EXISTS (SELECT 1 FROM global_texts WHERE field_key = 'invitation');
