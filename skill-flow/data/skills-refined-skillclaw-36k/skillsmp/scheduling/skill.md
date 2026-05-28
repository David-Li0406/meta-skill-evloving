---
name: scheduling
description: Handles appointment scheduling and availability with Cal.com integration
---

# Scheduling Skill

Manage customer appointments for HMLS Mobile Mechanic.

## Available Tools

- `get_availability` - Check available time slots for the next 7 days
- `create_booking` - Create a new appointment

## Workflow

1. **Gather Requirements**
   - Vehicle details (make, model, year)
   - Service needed
   - Customer location (must be in Orange County)
   - Preferred date/time

2. **Check Availability**
   - Use `get_availability` to show open slots
   - Present options to customer

3. **Create Booking**
   - Confirm all details with customer
   - Use `create_booking` with:
     - Customer name, email, phone
     - Start time (ISO 8601 format)
     - Duration based on service type
     - Service location address
     - Any notes about the service

## Service Durations

Estimate duration based on service type:
- Oil change: 30-45 minutes
- Brake service: 1-2 hours
- Diagnostic: 30-60 minutes
- Battery replacement: 30 minutes
- AC service: 1-2 hours
- Multiple services: Sum individual times + 15 min buffer

## Business Hours

Monday - Saturday: 8:00 AM - 12:00 AM (midnight)

## Service Area

Orange County only: Irvine, Newport Beach, Anaheim, Santa Ana, Costa Mesa, Fullerton, Huntington Beach, Lake Forest, Mission Viejo
