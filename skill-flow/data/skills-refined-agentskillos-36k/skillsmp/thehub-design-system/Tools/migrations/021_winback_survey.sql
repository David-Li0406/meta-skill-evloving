-- ============================================================================
-- Migration 014: Win-Back Survey System
-- Enables churned rider surveys with automatic discount code generation
-- ============================================================================

-- WINBACK CAMPAIGNS
-- Defines different survey campaigns (per brand or combined)
CREATE TABLE IF NOT EXISTS winback_campaigns (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NULL,

    -- Target criteria
    target_type ENUM('brand', 'multi_brand', 'all') DEFAULT 'brand',
    brand_ids JSON NULL COMMENT 'Array of brand_ids for multi_brand type',

    -- Survey period - riders who competed in these years but not target_year
    start_year YEAR NOT NULL DEFAULT 2021,
    end_year YEAR NOT NULL DEFAULT 2024,
    target_year YEAR NOT NULL DEFAULT 2025 COMMENT 'Year they did NOT compete',

    -- Discount code settings
    discount_type ENUM('fixed', 'percentage') DEFAULT 'fixed',
    discount_value DECIMAL(10,2) DEFAULT 100,
    discount_valid_until DATE NULL,
    discount_applicable_to ENUM('all', 'brand', 'series') DEFAULT 'all',
    discount_series_id INT NULL,

    -- Status
    is_active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_active (is_active),
    INDEX idx_target (target_type, target_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- WINBACK QUESTIONS
-- Survey questions (similar to event_rating_questions)
CREATE TABLE IF NOT EXISTS winback_questions (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT UNSIGNED NULL COMMENT 'NULL = applies to all campaigns',
    question_text VARCHAR(500) NOT NULL,
    question_type ENUM('radio', 'checkbox', 'scale', 'text') DEFAULT 'checkbox',
    options JSON NULL COMMENT 'Array of options for radio/checkbox',
    sort_order INT DEFAULT 0,
    is_required TINYINT(1) DEFAULT 0,
    active TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_campaign (campaign_id, active, sort_order),
    INDEX idx_active (active, sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- WINBACK RESPONSES
-- Stores survey responses (anonymized for reporting, linked for code generation)
CREATE TABLE IF NOT EXISTS winback_responses (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    campaign_id INT UNSIGNED NOT NULL,
    rider_id INT NOT NULL,

    -- Generated discount code
    discount_code_id INT NULL,
    discount_code VARCHAR(50) NULL,

    -- Metadata
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_hash VARCHAR(64) NULL COMMENT 'Hashed IP for duplicate detection',

    UNIQUE INDEX idx_rider_campaign (rider_id, campaign_id),
    INDEX idx_campaign (campaign_id),
    INDEX idx_submitted (submitted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- WINBACK ANSWERS
-- Individual question answers
CREATE TABLE IF NOT EXISTS winback_answers (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    response_id INT UNSIGNED NOT NULL,
    question_id INT UNSIGNED NOT NULL,
    answer_value TEXT NULL COMMENT 'JSON for checkbox, text for others',
    answer_scale INT NULL COMMENT 'For scale type questions (1-10)',

    INDEX idx_response (response_id),
    INDEX idx_question (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- SEED DATA: Default questions
-- ============================================================================

INSERT INTO winback_questions (campaign_id, question_text, question_type, options, sort_order, is_required, active) VALUES
-- Q1: Why did you stop (checkbox - multiple answers)
(NULL, 'Vad ar huvudorsaken till att du inte tavlade 2025?', 'checkbox',
 '["Tidsbrist / livssituation", "Skada eller sjukdom", "Kostnad (anmalningsavgifter, resor, utrustning)", "Brist pa motivation / intresse", "Flyttat / for langt till tavlingar", "Saknade traningskompisar / team", "Event passade inte min niva", "Bytte sport / aktivitet", "Annat"]',
 1, 1, 1),

-- Q2: What would bring you back (checkbox)
(NULL, 'Vad skulle fa dig att tavla igen?', 'checkbox',
 '["Lagre anmalningsavgifter", "Fler tavlingar i min region", "Battre klasser for min niva", "Tavla med vanner / klubbkompisar", "Kortare / enklare format", "Battre prispengar / premier", "Roligare banor / venues", "Battre stamning / community", "Inget speciellt - planerar redan aterkomma"]',
 2, 1, 1),

-- Q3: Comeback likelihood (scale 1-10)
(NULL, 'Hur troligt ar det att du tavlar 2026?', 'scale', NULL, 3, 1, 1),

-- Q4: Preferred discipline (checkbox)
(NULL, 'Vilken disciplin lockar dig mest?', 'checkbox',
 '["Enduro", "Downhill", "XC / Cross Country", "Gravel", "Oppen for allt"]',
 4, 1, 1),

-- Q5: Free text (optional)
(NULL, 'Nagot annat du vill dela med dig av?', 'text', NULL, 5, 0, 1);

-- ============================================================================
-- SEED DATA: Default campaigns
-- ============================================================================

-- Campaign for Brand 1 (GravitySeries)
INSERT INTO winback_campaigns (name, description, target_type, brand_ids, start_year, end_year, target_year, discount_type, discount_value, discount_valid_until, is_active) VALUES
('GravitySeries Comeback 2026', 'Ateraktivera tidigare GravitySeries-deltagare', 'brand', '[1]', 2021, 2024, 2025, 'fixed', 100, '2026-12-31', 1);

-- Campaign for Brands 3, 9, 10 combined
INSERT INTO winback_campaigns (name, description, target_type, brand_ids, start_year, end_year, target_year, discount_type, discount_value, discount_valid_until, is_active) VALUES
('Multi-Brand Comeback 2026', 'Ateraktivera deltagare fran flera varumarken', 'multi_brand', '[3, 9, 10]', 2021, 2024, 2025, 'fixed', 100, '2026-12-31', 1);
