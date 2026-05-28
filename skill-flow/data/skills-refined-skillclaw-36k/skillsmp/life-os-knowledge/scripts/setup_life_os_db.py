#!/usr/bin/env python3
"""
Life OS Knowledge Base - Supabase Setup
Creates the life_os_locations table and inserts initial data.

Usage: python setup_life_os_db.py
"""

import os
import json
from datetime import date
from supabase import create_client, Client

# Supabase connection
SUPABASE_URL = "https://mocerqjnksmhcjzxrewo.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_client() -> Client:
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_KEY environment variable required")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_location(client: Client, data: dict):
    """Insert a new location record."""
    result = client.table("life_os_locations").insert(data).execute()
    return result

def query_locations(client: Client, category: str = None, city: str = None, context_search: str = None):
    """Query locations with optional filters."""
    query = client.table("life_os_locations").select("*")
    
    if category:
        query = query.eq("category", category)
    if city:
        query = query.eq("city", city)
    if context_search:
        query = query.ilike("context", f"%{context_search}%")
    
    return query.execute()

# Initial data - Staybridge Suites Ocala
INITIAL_HOTELS = [
    {
        "category": "HOTEL",
        "name": "Staybridge Suites Ocala",
        "address": "4627 NW Blitchton Rd",
        "city": "Ocala",
        "state": "FL",
        "context": "Michael swim meets at Ocala Aquatic Center (fast pool)",
        "rating": 5,
        "notes": {
            "room_type": "studio with queen beds",
            "amenities": ["full kitchen", "free breakfast", "spacious rooms"],
            "value": "excellent",
            "tips": "Great value for money, good for multi-night swim meet stays"
        },
        "last_visited": "2025-12-04"
    }
]

INITIAL_VENUES = [
    {
        "category": "SWIM_VENUE",
        "name": "Ocala Aquatic Center",
        "address": "2500 E Fort King St",
        "city": "Ocala",
        "state": "FL",
        "context": "Fast pool for competitive swimming",
        "rating": 5,
        "notes": {
            "pool_speed": "FAST",
            "pool_type": "50m outdoor, configurable to 25y",
            "parking": "ample, free",
            "drive_from_satellite_beach": "2.5 hours (142 miles)",
            "preferred_hotel": "Staybridge Suites Ocala"
        },
        "last_visited": "2025-12-04"
    }
]

if __name__ == "__main__":
    client = get_client()
    
    print("Inserting initial hotel data...")
    for hotel in INITIAL_HOTELS:
        try:
            result = insert_location(client, hotel)
            print(f"✅ Added: {hotel['name']}")
        except Exception as e:
            print(f"⚠️ {hotel['name']}: {e}")
    
    print("\nInserting initial venue data...")
    for venue in INITIAL_VENUES:
        try:
            result = insert_location(client, venue)
            print(f"✅ Added: {venue['name']}")
        except Exception as e:
            print(f"⚠️ {venue['name']}: {e}")
    
    print("\nDone!")
