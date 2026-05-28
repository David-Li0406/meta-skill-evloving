#!/usr/bin/env python3
"""
Life OS Knowledge Base - Insert Location Helper
Add new locations to Supabase insights table.

Usage:
  python insert_location.py hotel "Marriott Tampa" "123 Main St" "Tampa" "FL" "Business trips" 4
"""

import httpx
import json
import sys
from datetime import date

SUPABASE_URL = "https://mocerqjnksmhcjzxrewo.supabase.co"
SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1vY2VycWpua3NtaGNqenhyZXdvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDUzMjUyNiwiZXhwIjoyMDgwMTA4NTI2fQ.fL255mO0V8-rrU0Il3L41cIdQXUau-HRQXiamTqp9nE"

HEADERS = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

TYPE_MAP = {
    "hotel": "HOTEL",
    "venue": "SWIM_VENUE",
    "restaurant": "RESTAURANT",
    "service": "SERVICE_PROVIDER",
    "route": "TRAVEL_ROUTE"
}

def insert_location(loc_type, name, address, city, state, context, rating, extra_notes=None):
    """Insert a new location."""
    insight_type = TYPE_MAP.get(loc_type.lower(), loc_type.upper())
    
    description = {
        "address": address,
        "city": city,
        "state": state,
        "context": context
    }
    
    if extra_notes:
        description.update(extra_notes)
    
    data = {
        "insight_type": insight_type,
        "title": name,
        "description": json.dumps(description),
        "related_date": str(date.today()),
        "priority": "medium",
        "status": "active",
        "source": "life_os_knowledge",
        "confidence": int(rating)
    }
    
    with httpx.Client(verify=False, timeout=30) as client:
        r = client.post(f"{SUPABASE_URL}/rest/v1/insights", headers=HEADERS, json=data)
        if r.status_code in [200, 201]:
            result = r.json()
            print(f"✅ Added: {name}")
            print(f"   Type: {insight_type}")
            print(f"   Rating: {'⭐' * int(rating)}")
            print(f"   ID: {result[0].get('id', 'N/A')}")
            return True
        else:
            print(f"❌ Error: {r.status_code} - {r.text}")
            return False

def main():
    if len(sys.argv) < 8:
        print("Usage: python insert_location.py <type> <name> <address> <city> <state> <context> <rating>")
        print("Types: hotel, venue, restaurant, service, route")
        print('Example: python insert_location.py hotel "Marriott Tampa" "123 Main St" "Tampa" "FL" "Business trips" 4')
        return
    
    loc_type, name, address, city, state, context, rating = sys.argv[1:8]
    insert_location(loc_type, name, address, city, state, context, rating)

if __name__ == "__main__":
    main()
