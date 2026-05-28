#!/usr/bin/env python3
"""
Life OS Knowledge Base - Location Query Helper
Query hotels, swim venues, and other locations from Supabase.

Usage:
    python query_locations.py --type HOTEL --city Ocala
    python query_locations.py --type SWIM_VENUE
    python query_locations.py --search "Michael"
"""

import httpx
import json
import argparse
import os

SUPABASE_URL = "https://mocerqjnksmhcjzxrewo.supabase.co"
# Service key - use environment variable or hardcode for autonomous operation
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", 
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1vY2VycWpua3NtaGNqenhyZXdvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDUzMjUyNiwiZXhwIjoyMDgwMTA4NTI2fQ.fL255mO0V8-rrU0Il3L41cIdQXUau-HRQXiamTqp9nE")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def query_locations(insight_type=None, city=None, search=None):
    """Query locations from insights table."""
    url = f"{SUPABASE_URL}/rest/v1/insights?"
    
    params = []
    if insight_type:
        if "," in insight_type:
            types = insight_type.split(",")
            params.append(f"insight_type=in.({','.join(types)})")
        else:
            params.append(f"insight_type=eq.{insight_type}")
    else:
        params.append("insight_type=in.(HOTEL,SWIM_VENUE,RESTAURANT,SERVICE_PROVIDER,TRAVEL_ROUTE)")
    
    if city:
        params.append(f"description=cs.{city}")
    
    if search:
        params.append(f"or=(title.ilike.*{search}*,description.cs.{search})")
    
    params.append("order=confidence.desc")
    
    url += "&".join(params)
    
    with httpx.Client(verify=False) as client:
        r = client.get(url, headers=HEADERS)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"Error: {r.status_code} - {r.text}")
            return []

def insert_location(insight_type, title, details, rating=5, related_date=None):
    """Insert a new location."""
    from datetime import date
    
    data = {
        "insight_type": insight_type,
        "title": title,
        "description": json.dumps(details),
        "related_date": related_date or str(date.today()),
        "priority": "medium",
        "status": "active",
        "source": "life_os_knowledge",
        "confidence": rating
    }
    
    with httpx.Client(verify=False) as client:
        r = client.post(
            f"{SUPABASE_URL}/rest/v1/insights",
            headers={**HEADERS, "Prefer": "return=representation"},
            json=data
        )
        if r.status_code in [200, 201]:
            return r.json()
        else:
            print(f"Error: {r.status_code} - {r.text}")
            return None

def display_location(loc):
    """Pretty print a location."""
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📍 {loc['insight_type']}: {loc['title']}")
    rating = int(loc['confidence']) if loc['confidence'] else 0
    print(f"   Rating: {'⭐' * rating} ({rating}/5)")
    print(f"   Last visited: {loc['related_date']}")
    
    try:
        details = json.loads(loc['description'])
        if details.get('address'):
            print(f"   Address: {details.get('address')}, {details.get('city')}, {details.get('state')}")
        if details.get('context'):
            print(f"   Context: {details.get('context')}")
        if details.get('room_type'):
            print(f"   Room: {details.get('room_type')}")
            print(f"   Value: {details.get('value')}")
        if details.get('pool_speed'):
            print(f"   Pool: {details.get('pool_speed')} - {details.get('pool_type')}")
        if details.get('preferred_hotel'):
            print(f"   Preferred hotel: {details.get('preferred_hotel')}")
    except:
        print(f"   Details: {loc['description'][:100]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Life OS locations")
    parser.add_argument("--type", help="Location type: HOTEL, SWIM_VENUE, RESTAURANT, etc.")
    parser.add_argument("--city", help="Filter by city")
    parser.add_argument("--search", help="Search in title and description")
    
    args = parser.parse_args()
    
    locations = query_locations(
        insight_type=args.type,
        city=args.city,
        search=args.search
    )
    
    if locations:
        print(f"\n🗺️  Found {len(locations)} location(s):\n")
        for loc in locations:
            display_location(loc)
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    else:
        print("No locations found.")
