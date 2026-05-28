-- Migration 016: Event Ratings System
-- Allows riders to rate events they have participated in
-- Data is collected anonymously for analysis by organizers and series admins

-- Main ratings table
CREATE TABLE IF NOT EXISTS event_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    rider_id INT NOT NULL,
    overall_rating TINYINT NOT NULL CHECK (overall_rating BETWEEN 1 AND 10),
    comment TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Foreign keys
    CONSTRAINT fk_event_ratings_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    CONSTRAINT fk_event_ratings_rider FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,

    -- One rating per rider per event
    UNIQUE KEY unique_rider_event (rider_id, event_id),

    -- Indexes for lookups
    INDEX idx_event_ratings_event (event_id),
    INDEX idx_event_ratings_submitted (submitted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Questions definition table
CREATE TABLE IF NOT EXISTS event_rating_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_key VARCHAR(50) NOT NULL UNIQUE,
    question_text VARCHAR(255) NOT NULL,
    question_text_en VARCHAR(255),
    category VARCHAR(50) NOT NULL DEFAULT 'general',
    sort_order INT NOT NULL DEFAULT 0,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Individual question answers
CREATE TABLE IF NOT EXISTS event_rating_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rating_id INT NOT NULL,
    question_id INT NOT NULL,
    score TINYINT NOT NULL CHECK (score BETWEEN 1 AND 10),

    CONSTRAINT fk_rating_answers_rating FOREIGN KEY (rating_id) REFERENCES event_ratings(id) ON DELETE CASCADE,
    CONSTRAINT fk_rating_answers_question FOREIGN KEY (question_id) REFERENCES event_rating_questions(id) ON DELETE CASCADE,

    UNIQUE KEY unique_rating_question (rating_id, question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed default questions (Swedish MTB focus)
INSERT INTO event_rating_questions (question_key, question_text, question_text_en, category, sort_order) VALUES
('course_marking', 'Banmarkeringar och skyltning', 'Course marking and signage', 'course', 1),
('course_quality', 'Banans kvalitet och underhall', 'Course quality and maintenance', 'course', 2),
('safety', 'Sakerhet och sjukvardsberedskap', 'Safety and medical preparedness', 'safety', 3),
('registration', 'Anmalan och incheckningsprocess', 'Registration and check-in process', 'logistics', 4),
('timing', 'Tidtagning och resultathantering', 'Timing and results management', 'logistics', 5),
('schedule', 'Tidschema och punktlighet', 'Schedule and punctuality', 'logistics', 6),
('facilities', 'Faciliteter (parkering, toaletter, etc)', 'Facilities (parking, toilets, etc)', 'facilities', 7),
('atmosphere', 'Stamning och upplevelse', 'Atmosphere and experience', 'experience', 8),
('value', 'Varde for pengarna', 'Value for money', 'value', 9),
('recommend', 'Skulle rekommendera till andra', 'Would recommend to others', 'overall', 10);

-- View for aggregated event ratings (anonymous)
CREATE OR REPLACE VIEW v_event_ratings_summary AS
SELECT
    e.id AS event_id,
    e.name AS event_name,
    e.date AS event_date,
    s.name AS series_name,
    COUNT(er.id) AS total_ratings,
    ROUND(AVG(er.overall_rating), 1) AS avg_overall_rating,
    MIN(er.overall_rating) AS min_rating,
    MAX(er.overall_rating) AS max_rating
FROM events e
LEFT JOIN event_ratings er ON e.id = er.event_id
LEFT JOIN series s ON e.series_id = s.id
GROUP BY e.id, e.name, e.date, s.name;

-- View for question-level averages (anonymous)
CREATE OR REPLACE VIEW v_event_question_averages AS
SELECT
    er.event_id,
    q.question_key,
    q.question_text,
    q.category,
    COUNT(a.id) AS response_count,
    ROUND(AVG(a.score), 1) AS avg_score
FROM event_rating_questions q
LEFT JOIN event_rating_answers a ON q.id = a.question_id
LEFT JOIN event_ratings er ON a.rating_id = er.id
WHERE q.active = 1
GROUP BY er.event_id, q.id, q.question_key, q.question_text, q.category;
