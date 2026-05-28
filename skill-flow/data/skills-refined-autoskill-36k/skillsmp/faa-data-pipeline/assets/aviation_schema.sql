-- MagentaLine Aviation Database Schema
-- SQLite schema for FAA aviation data

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ============================================
-- AIRPORTS
-- ============================================
CREATE TABLE IF NOT EXISTS airports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_site_number TEXT UNIQUE NOT NULL,
    location_id TEXT NOT NULL,
    icao_id TEXT,
    facility_name TEXT NOT NULL,
    facility_type TEXT,
    city_name TEXT,
    state_code TEXT,
    state_name TEXT,
    county_name TEXT,
    latitude REAL,
    longitude REAL,
    elevation_ft REAL,
    magnetic_variation REAL,
    ownership_type TEXT,
    use_type TEXT,
    owner_name TEXT,
    manager_name TEXT,
    pattern_altitude INTEGER,
    sectional_chart TEXT,
    boundary_artcc TEXT,
    resp_artcc TEXT,
    tie_in_fss TEXT,
    notam_facility TEXT,
    status TEXT,
    customs_entry TEXT,
    military_joint_use TEXT,
    effective_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_airports_location_id ON airports(location_id);
CREATE INDEX IF NOT EXISTS idx_airports_icao_id ON airports(icao_id);
CREATE INDEX IF NOT EXISTS idx_airports_state ON airports(state_code);
CREATE INDEX IF NOT EXISTS idx_airports_coords ON airports(latitude, longitude);

-- ============================================
-- RUNWAYS
-- ============================================
CREATE TABLE IF NOT EXISTS runways (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_site_number TEXT NOT NULL,
    runway_id TEXT NOT NULL,
    length_ft INTEGER,
    width_ft INTEGER,
    surface_type TEXT,
    surface_treatment TEXT,
    pcn TEXT,
    edge_lights TEXT,

    -- Base end
    base_id TEXT,
    base_true_heading INTEGER,
    base_latitude REAL,
    base_longitude REAL,
    base_elevation_ft REAL,
    base_displaced_ft INTEGER,
    base_tora_ft INTEGER,
    base_toda_ft INTEGER,
    base_asda_ft INTEGER,
    base_lda_ft INTEGER,
    base_ils_type TEXT,
    base_rgt_traffic TEXT,
    base_markings TEXT,
    base_vgsi TEXT,
    base_reil TEXT,
    base_centerline_lights TEXT,
    base_tdz_lights TEXT,

    -- Reciprocal end
    recip_id TEXT,
    recip_true_heading INTEGER,
    recip_latitude REAL,
    recip_longitude REAL,
    recip_elevation_ft REAL,
    recip_displaced_ft INTEGER,
    recip_tora_ft INTEGER,
    recip_toda_ft INTEGER,
    recip_asda_ft INTEGER,
    recip_lda_ft INTEGER,
    recip_ils_type TEXT,
    recip_rgt_traffic TEXT,
    recip_markings TEXT,
    recip_vgsi TEXT,
    recip_reil TEXT,
    recip_centerline_lights TEXT,
    recip_tdz_lights TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(facility_site_number, runway_id),
    FOREIGN KEY (facility_site_number) REFERENCES airports(facility_site_number)
);

CREATE INDEX IF NOT EXISTS idx_runways_facility ON runways(facility_site_number);
CREATE INDEX IF NOT EXISTS idx_runways_length ON runways(length_ft);

-- ============================================
-- NAVAIDS
-- ============================================
CREATE TABLE IF NOT EXISTS navaids (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_id TEXT NOT NULL,
    facility_type TEXT,
    type_category TEXT,
    official_id TEXT,
    name TEXT,
    city TEXT,
    state_code TEXT,
    state_name TEXT,
    country TEXT,
    latitude REAL,
    longitude REAL,
    elevation_ft REAL,
    magnetic_variation REAL,
    frequency_mhz REAL,
    tacan_channel TEXT,
    transmitted_id TEXT,
    navaid_class TEXT,
    artcc TEXT,
    low_artcc TEXT,
    vor_service_volume TEXT,
    dme_service_volume TEXT,
    hours_of_operation TEXT,
    public_use TEXT,
    nav_status TEXT,
    effective_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(facility_id, facility_type)
);

CREATE INDEX IF NOT EXISTS idx_navaids_id ON navaids(facility_id);
CREATE INDEX IF NOT EXISTS idx_navaids_type ON navaids(type_category);
CREATE INDEX IF NOT EXISTS idx_navaids_coords ON navaids(latitude, longitude);

-- ============================================
-- FIXES (Waypoints)
-- ============================================
CREATE TABLE IF NOT EXISTS fixes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fix_id TEXT NOT NULL,
    state_code TEXT,
    icao_region TEXT,
    latitude REAL,
    longitude REAL,
    fix_category TEXT,
    fix_type TEXT,
    fix_use TEXT,
    artcc_hi TEXT,
    artcc_lo TEXT,
    charting_info TEXT,
    nas_id TEXT,
    publish_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(fix_id, state_code)
);

CREATE INDEX IF NOT EXISTS idx_fixes_id ON fixes(fix_id);
CREATE INDEX IF NOT EXISTS idx_fixes_coords ON fixes(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_fixes_type ON fixes(fix_type);

-- ============================================
-- AIRWAYS
-- ============================================
CREATE TABLE IF NOT EXISTS airways (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    airway_id TEXT NOT NULL UNIQUE,
    airway_type TEXT,
    airway_category TEXT,
    segment_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_airways_id ON airways(airway_id);
CREATE INDEX IF NOT EXISTS idx_airways_category ON airways(airway_category);

CREATE TABLE IF NOT EXISTS airway_segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    airway_id TEXT NOT NULL,
    sequence_number INTEGER,
    from_fix TEXT,
    from_fix_state TEXT,
    to_fix TEXT,
    to_fix_state TEXT,
    from_latitude REAL,
    from_longitude REAL,
    to_latitude REAL,
    to_longitude REAL,
    mea_ft INTEGER,
    max_altitude_ft INTEGER,
    moa_ft INTEGER,
    maa_ft INTEGER,
    distance_nm REAL,
    changeover_nm REAL,
    course_out_deg REAL,
    course_in_deg REAL,
    mea_direction TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(airway_id, sequence_number),
    FOREIGN KEY (airway_id) REFERENCES airways(airway_id)
);

CREATE INDEX IF NOT EXISTS idx_segments_airway ON airway_segments(airway_id);
CREATE INDEX IF NOT EXISTS idx_segments_fixes ON airway_segments(from_fix, to_fix);

-- ============================================
-- PROCEDURES (SIDs, STARs, Approaches)
-- ============================================
CREATE TABLE IF NOT EXISTS procedures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    airport_id TEXT NOT NULL,
    procedure_id TEXT NOT NULL,
    procedure_type TEXT,
    procedure_name TEXT,
    transition_id TEXT,
    route_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(airport_id, procedure_id, transition_id)
);

CREATE INDEX IF NOT EXISTS idx_procedures_airport ON procedures(airport_id);
CREATE INDEX IF NOT EXISTS idx_procedures_type ON procedures(procedure_type);

CREATE TABLE IF NOT EXISTS procedure_legs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    airport_id TEXT NOT NULL,
    procedure_id TEXT NOT NULL,
    transition_id TEXT,
    sequence_number INTEGER,
    fix_id TEXT,
    fix_icao TEXT,
    path_termination TEXT,
    path_termination_desc TEXT,
    turn_direction TEXT,
    outbound_course REAL,
    distance_time TEXT,
    altitude_desc TEXT,
    altitude1 INTEGER,
    altitude2 INTEGER,
    speed_limit INTEGER,
    vertical_angle REAL,
    rnp REAL,
    arc_radius REAL,
    center_fix TEXT,
    waypoint_desc TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_legs_procedure ON procedure_legs(airport_id, procedure_id);
CREATE INDEX IF NOT EXISTS idx_legs_fix ON procedure_legs(fix_id);

-- ============================================
-- OBSTACLES
-- ============================================
CREATE TABLE IF NOT EXISTS obstacles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oas_number TEXT UNIQUE NOT NULL,
    country TEXT,
    state TEXT,
    city TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    obstacle_type TEXT,
    obstacle_type_desc TEXT,
    quantity INTEGER DEFAULT 1,
    agl_height_ft INTEGER,
    msl_height_ft INTEGER,
    lighting TEXT,
    lighting_desc TEXT,
    horizontal_accuracy TEXT,
    vertical_accuracy TEXT,
    mark_indicator TEXT,
    faa_study_number TEXT,
    action TEXT,
    verification_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_obstacles_coords ON obstacles(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_obstacles_msl ON obstacles(msl_height_ft);
CREATE INDEX IF NOT EXISTS idx_obstacles_type ON obstacles(obstacle_type);
CREATE INDEX IF NOT EXISTS idx_obstacles_state ON obstacles(state);

-- ============================================
-- CHARTS (d-TPP)
-- ============================================
CREATE TABLE IF NOT EXISTS charts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_code TEXT,
    state_name TEXT,
    city_name TEXT,
    airport_id TEXT,
    airport_name TEXT,
    chart_seq TEXT,
    chart_code TEXT,
    chart_name TEXT,
    user_action TEXT,
    pdf_name TEXT,
    cn_flag TEXT,
    cn_page TEXT,
    cn_date TEXT,
    bvsection TEXT,
    procedure_uid TEXT,
    two_colored TEXT,
    civil TEXT,
    military TEXT,
    copter TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(airport_id, chart_code, chart_name)
);

CREATE INDEX IF NOT EXISTS idx_charts_airport ON charts(airport_id);
CREATE INDEX IF NOT EXISTS idx_charts_code ON charts(chart_code);
CREATE INDEX IF NOT EXISTS idx_charts_state ON charts(state_code);

-- ============================================
-- AIRPORT FREQUENCIES
-- ============================================
CREATE TABLE IF NOT EXISTS airport_frequencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facility_site_number TEXT,
    terminal_id TEXT,
    airport_name TEXT,
    frequency_type TEXT,
    frequency_mhz REAL,
    frequency_use TEXT,
    sectorization TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(facility_site_number, frequency_type, frequency_mhz)
);

CREATE INDEX IF NOT EXISTS idx_freqs_facility ON airport_frequencies(facility_site_number);
CREATE INDEX IF NOT EXISTS idx_freqs_terminal ON airport_frequencies(terminal_id);
CREATE INDEX IF NOT EXISTS idx_freqs_type ON airport_frequencies(frequency_type);

-- ============================================
-- METADATA
-- ============================================
CREATE TABLE IF NOT EXISTS data_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_type TEXT NOT NULL,
    cycle_id TEXT,
    effective_date TEXT,
    expiration_date TEXT,
    source_url TEXT,
    record_count INTEGER,
    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(data_type, cycle_id)
);

-- ============================================
-- VIEWS
-- ============================================

-- Airports with runway info
CREATE VIEW IF NOT EXISTS v_airports_with_runways AS
SELECT
    a.location_id,
    a.icao_id,
    a.facility_name,
    a.city_name,
    a.state_code,
    a.latitude,
    a.longitude,
    a.elevation_ft,
    MAX(r.length_ft) as longest_runway_ft,
    COUNT(r.id) as runway_count
FROM airports a
LEFT JOIN runways r ON a.facility_site_number = r.facility_site_number
GROUP BY a.id;

-- Airports with frequencies
CREATE VIEW IF NOT EXISTS v_airports_with_frequencies AS
SELECT
    a.location_id,
    a.facility_name,
    af.frequency_type,
    af.frequency_mhz
FROM airports a
JOIN airport_frequencies af ON a.facility_site_number = af.facility_site_number
ORDER BY a.location_id, af.frequency_type;
