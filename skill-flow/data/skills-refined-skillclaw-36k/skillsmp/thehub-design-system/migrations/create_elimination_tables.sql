-- Elimination / Dual Slalom Tables
-- Supports bracket-style racing with qualification rounds and elimination brackets
-- Created: 2025-12-28

-- ============================================================================
-- ELIMINATION QUALIFYING RESULTS
-- Stores qualification run times (1 or 2 runs, best time for seeding)
-- ============================================================================
CREATE TABLE IF NOT EXISTS elimination_qualifying (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    class_id INT NOT NULL,
    rider_id INT NOT NULL,
    bib_number VARCHAR(20),

    -- Qualification times (up to 2 runs)
    run_1_time DECIMAL(10,3),           -- Time in seconds with milliseconds
    run_2_time DECIMAL(10,3),
    best_time DECIMAL(10,3),            -- Best of the two runs (for seeding)

    -- Seeding position based on best_time
    seed_position INT,

    -- Status
    status ENUM('finished', 'dnf', 'dns', 'dq') DEFAULT 'finished',
    advances_to_bracket TINYINT(1) DEFAULT 0,  -- Made it to elimination bracket

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,

    UNIQUE KEY unique_event_class_rider (event_id, class_id, rider_id),
    INDEX idx_event_class (event_id, class_id),
    INDEX idx_seed (event_id, class_id, seed_position),
    INDEX idx_best_time (event_id, class_id, best_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ELIMINATION BRACKETS
-- Stores head-to-head matchups in the elimination rounds
-- ============================================================================
CREATE TABLE IF NOT EXISTS elimination_brackets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    class_id INT NOT NULL,

    -- Bracket type: 'main' for A-bracket, 'consolation' for B-bracket
    bracket_type ENUM('main', 'consolation') DEFAULT 'main',

    -- Round information
    -- round_name: 'round_of_32', 'round_of_16', 'quarterfinal', 'semifinal', 'final', 'third_place', 'b_final', etc.
    round_name VARCHAR(50) NOT NULL,
    round_number INT NOT NULL,           -- 1=first round, 2=second, etc.
    heat_number INT NOT NULL,            -- Position within the round (1, 2, 3, etc.)

    -- Competitors
    rider_1_id INT,                      -- Higher seed / winner from previous round
    rider_2_id INT,                      -- Lower seed / winner from previous round
    rider_1_seed INT,                    -- Original seed position
    rider_2_seed INT,

    -- Run times (2 runs per matchup, total time determines winner)
    rider_1_run1 DECIMAL(10,3),
    rider_1_run2 DECIMAL(10,3),
    rider_1_total DECIMAL(10,3),

    rider_2_run1 DECIMAL(10,3),
    rider_2_run2 DECIMAL(10,3),
    rider_2_total DECIMAL(10,3),

    -- Result
    winner_id INT,
    loser_id INT,

    -- Status
    status ENUM('pending', 'in_progress', 'completed', 'bye') DEFAULT 'pending',

    -- Bracket position for visualization (helps draw the bracket)
    bracket_position INT,                -- Position in the visual bracket (for rendering)

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (rider_1_id) REFERENCES riders(id) ON DELETE SET NULL,
    FOREIGN KEY (rider_2_id) REFERENCES riders(id) ON DELETE SET NULL,
    FOREIGN KEY (winner_id) REFERENCES riders(id) ON DELETE SET NULL,
    FOREIGN KEY (loser_id) REFERENCES riders(id) ON DELETE SET NULL,

    UNIQUE KEY unique_bracket_heat (event_id, class_id, bracket_type, round_name, heat_number),
    INDEX idx_event_class (event_id, class_id),
    INDEX idx_round (event_id, class_id, round_name),
    INDEX idx_rider1 (rider_1_id),
    INDEX idx_rider2 (rider_2_id),
    INDEX idx_winner (winner_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ELIMINATION FINAL RESULTS
-- Final standings after all brackets are complete
-- ============================================================================
CREATE TABLE IF NOT EXISTS elimination_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    class_id INT NOT NULL,
    rider_id INT NOT NULL,

    -- Final placement
    final_position INT,                  -- 1, 2, 3, 4, etc.

    -- How far they got
    qualifying_position INT,             -- Seed from qualifying
    eliminated_in_round VARCHAR(50),     -- Which round they were eliminated (null for top 4)

    -- Points (if applicable)
    points INT DEFAULT 0,

    -- Bracket they ended up in
    bracket_type ENUM('main', 'consolation') DEFAULT 'main',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE,

    UNIQUE KEY unique_event_class_rider (event_id, class_id, rider_id),
    INDEX idx_event_class (event_id, class_id),
    INDEX idx_position (event_id, class_id, final_position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Add elimination settings to events table
-- ============================================================================
ALTER TABLE events
    ADD COLUMN IF NOT EXISTS elimination_bracket_size ENUM('8', '16', '32') DEFAULT '16',
    ADD COLUMN IF NOT EXISTS elimination_qualifying_runs INT DEFAULT 2,
    ADD COLUMN IF NOT EXISTS elimination_has_b_final TINYINT(1) DEFAULT 1;
