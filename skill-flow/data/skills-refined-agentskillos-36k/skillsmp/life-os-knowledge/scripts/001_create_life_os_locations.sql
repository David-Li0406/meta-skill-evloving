-- Life OS Knowledge Base - Database Schema
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/mocerqjnksmhcjzxrewo/sql

-- Create the life_os_locations table
CREATE TABLE IF NOT EXISTS life_os_locations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    category TEXT NOT NULL CHECK (category IN ('HOTEL', 'SWIM_VENUE', 'RESTAURANT', 'SERVICE_PROVIDER', 'TRAVEL_ROUTE')),
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    context TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    notes JSONB DEFAULT '{}',
    last_visited DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for common queries
CREATE INDEX IF NOT EXISTS idx_locations_category ON life_os_locations(category);
CREATE INDEX IF NOT EXISTS idx_locations_city ON life_os_locations(city);
CREATE INDEX IF NOT EXISTS idx_locations_context ON life_os_locations USING gin(to_tsvector('english', context));

-- Enable RLS
ALTER TABLE life_os_locations ENABLE ROW LEVEL SECURITY;

-- Create policy for authenticated access
CREATE POLICY "Enable all operations for authenticated users" ON life_os_locations
    FOR ALL USING (true);

-- Insert initial data: Staybridge Suites Ocala
INSERT INTO life_os_locations (category, name, address, city, state, context, rating, notes, last_visited)
VALUES (
    'HOTEL',
    'Staybridge Suites Ocala',
    '4627 NW Blitchton Rd',
    'Ocala',
    'FL',
    'Michael swim meets at Ocala Aquatic Center (fast pool)',
    5,
    '{"room_type": "studio with queen beds", "amenities": ["full kitchen", "free breakfast", "spacious rooms"], "value": "excellent", "tips": "Great value for money, good for multi-night swim meet stays"}',
    '2025-12-04'
);

-- Insert initial data: Ocala Aquatic Center
INSERT INTO life_os_locations (category, name, address, city, state, context, rating, notes, last_visited)
VALUES (
    'SWIM_VENUE',
    'Ocala Aquatic Center',
    '2500 E Fort King St',
    'Ocala',
    'FL',
    'Fast pool for competitive swimming - Michael meets',
    5,
    '{"pool_speed": "FAST", "pool_type": "50m outdoor, configurable to 25y", "parking": "ample, free", "drive_from_satellite_beach": "2.5 hours (142 miles)", "preferred_hotel": "Staybridge Suites Ocala"}',
    '2025-12-04'
);

-- Verify
SELECT * FROM life_os_locations;
