ALTER TABLE sponsors ADD COLUMN contact_name VARCHAR(255) NULL AFTER description;
ALTER TABLE sponsors ADD COLUMN contact_email VARCHAR(255) NULL AFTER contact_name;
ALTER TABLE sponsors ADD COLUMN contact_phone VARCHAR(50) NULL AFTER contact_email;
ALTER TABLE sponsors ADD COLUMN display_order INT DEFAULT 0 AFTER contact_phone;
ALTER TABLE sponsors ADD COLUMN logo_media_id INT NULL AFTER logo_dark;
