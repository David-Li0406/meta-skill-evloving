---
name: booking-management
description: Guide for managing train bookings, IRCTC accounts, and booking records in the TrainTrack application
---

This skill provides guidance for working with the booking management system in TrainTrack, including booking CRUD operations, IRCTC account management, and booking completion records.

## Booking Management

### Core Concepts

**Booking Status Types:**
- `pending` - Bookings that are not yet completed
- `completed` - Bookings that have been successfully completed
- `cancelled` - Bookings that were cancelled

**Train Classes:** `sleeper`, `3ac`, `2ac`, `1ac`

**Booking Data Structure:**
- Source and destination stations
- Journey date (stored as Firestore Timestamp, convert to ISO string)
- Passenger details array (name, age, gender, berth preference)
- Train number and class
- IRCTC account reference
- Status tracking with reasons

### Working with Bookings

When implementing booking-related features:

1. **Type Definitions:** Use types from [src/types/booking.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/types/booking.ts)
   - `BookingStatus`, `TrainClass`, `Passenger`, `Booking` interfaces

2. **Custom Hooks:** Use existing hooks in [src/hooks/useBookings.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/hooks/useBookings.ts)
   - React Query for data fetching and caching
   - Real-time updates with Firestore listeners
   - Infinite scroll for completed bookings

3. **Date Handling:** Always convert Firestore Timestamps to ISO strings:
   ```typescript
   journeyDate: booking.journeyDate?.toDate?.()?.toISOString() || booking.journeyDate
   ```

4. **Form Handling:** Use React Hook Form + Zod validation
   - See [BookingForm.tsx](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/components/bookings/BookingForm.tsx) for patterns
   - Dynamic passenger array management
   - Status badge components for visual feedback

### IRCTC Account Management

**Account Features:**
- Store IRCTC credentials and wallet information
- Track account status and balance
- Link accounts to bookings

**Working with Accounts:**
- Use [src/hooks/useAccounts.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/hooks/useAccounts.ts)
- Account components in [src/components/accounts/](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/components/accounts/)
- AccountSelect component for booking forms

### Booking Records (Completion Tracking)

**Purpose:** Record successful booking completions with payment details

**Payment Methods:** `upi`, `net_banking`, `credit_card`, `debit_card`, `wallet`

**Implementation:**
- Use [src/hooks/useBookingRecords.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/hooks/useBookingRecords.ts)
- BookingRecordForm for completion entry
- Link to original booking via booking ID

## Common Patterns

### Creating a New Booking

1. Define form schema with Zod
2. Use useForm with zodResolver
3. On submit, call Firestore addDoc
4. Invalidate React Query cache
5. Show toast notification

### Editing an Existing Booking

1. Use query parameter routing (?id= for static export compatibility)
2. Pre-fill form with booking data
3. Convert Timestamps to strings for form fields
4. On submit, call Firestore updateDoc
5. Invalidate cache and navigate back

### Updating Booking Status

1. Use StatusBadge component for display
2. StatusReasonDialog for status changes with reasons
3. Update Firestore document with new status
4. Invalidate relevant queries

## Component Locations

**Booking Components:** [src/components/bookings/](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/components/bookings/)
- BookingCard, BookingForm, BookingList, BookingsView
- StatusBadge, StatusReasonDialog, DateGroupHeading

**Account Components:** [src/components/accounts/](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/components/accounts/)
- AccountSelect, AccountsTab, RefundsManager

## Firestore Operations

**Collection Names:**
- `bookings/` - Main booking records
- `irctcAccounts/` - IRCTC credentials
- `bookingRecords/` - Completion records
- `handlers/` - Handler/agent names

**Client SDK Methods:**
- `collection()`, `doc()`, `getDocs()`, `getDoc()`
- `addDoc()`, `updateDoc()`, `deleteDoc()`
- `onSnapshot()` for real-time listeners

## UI Patterns

**Tabbed Interface:** Separate 'Pending' and 'Completed' tabs with 'Pending' as default

**Card-based Layout:** Use Card components for organizing booking information

**Date Grouping:** Completed bookings grouped by date with DateGroupHeading

**Infinite Scroll:** Use intersection observer pattern for loading more bookings

## Styling Guidelines

Follow the design system:
- Primary: #64B5F6 (calm blue)
- Background: #F0F4F7 (light gray)
- Accent: #4DB6AC (muted teal)
- Clean, sans-serif fonts (Open Sans)
- Simple, minimalist icons

## Key Files to Reference

- [src/hooks/useBookings.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/hooks/useBookings.ts) - Booking data management
- [src/hooks/useAccounts.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/hooks/useAccounts.ts) - Account management
- [src/components/bookings/BookingForm.tsx](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/components/bookings/BookingForm.tsx) - Complex form patterns
- [src/types/booking.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/types/booking.ts) - Type definitions
