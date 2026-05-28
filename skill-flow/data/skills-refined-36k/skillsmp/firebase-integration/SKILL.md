---
name: firebase-integration
description: Guide for Firebase setup, Firestore operations, and client-side data management in TrainTrack
---

This skill provides comprehensive guidance for working with Firebase, including initialization, Firestore client SDK usage, security rules, and environment configuration.

## Firebase Initialization

**Singleton Pattern:** Firebase is initialized once using a singleton pattern to prevent multiple app instances.

**Configuration File:** [src/lib/firebase.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/lib/firebase.ts)
- Validates Firebase config on initialization
- Logs configuration status for debugging
- Exports initialized app and auth instances

**Environment Variables Required:**
```
NEXT_PUBLIC_FIREBASE_API_KEY=<key>
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=<domain>
NEXT_PUBLIC_FIREBASE_PROJECT_ID=<project_id>
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=<bucket>
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=<sender_id>
NEXT_PUBLIC_FIREBASE_APP_ID=<app_id>
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=<measurement_id>
NEXT_PUBLIC_FIREBASE_DATABASE_ID=<database_id> # Optional
```

Note: `NEXT_PUBLIC_` prefixed variables are exposed to the browser.

## Firestore Client SDK Usage

TrainTrack uses **Client-Side Rendering (CSR)** with direct Firestore access from the browser.

### Core Client Methods

**Collection Operations:**
```typescript
import { collection, getDocs, addDoc, query, where } from 'firebase/firestore';

// Get all documents
const snapshot = await getDocs(collection(db, 'bookings'));

// Query with filters
const q = query(collection(db, 'bookings'), where('status', '==', 'pending'));
const snapshot = await getDocs(q);
```

**Document Operations:**
```typescript
import { doc, getDoc, updateDoc, deleteDoc } from 'firebase/firestore';

// Get single document
const docRef = doc(db, 'bookings', bookingId);
const docSnap = await getDoc(docRef);

// Update document
await updateDoc(docRef, { status: 'completed' });

// Delete document
await deleteDoc(docRef);
```

**Real-time Updates:**
```typescript
import { onSnapshot } from 'firebase/firestore';

const unsubscribe = onSnapshot(collection(db, 'bookings'), (snapshot) => {
  snapshot.forEach((doc) => {
    console.log(doc.data());
  });
});

// Clean up on unmount
unsubscribe();
```

## Firestore Collections

### Bookings Collection (`bookings/`)
Stores main booking records with:
- Source and destination stations
- Journey date (Firestore Timestamp)
- Passenger details array
- Train number and class
- IRCTC account reference
- Status tracking

### IRCTC Accounts Collection (`irctcAccounts/`)
Stores IRCTC credentials and wallet information:
- Username and encrypted password
- Wallet balance tracking
- Account status
- Linked bookings

### Booking Records Collection (`bookingRecords/`)
Stores completion/payment records:
- Reference to original booking
- Payment method and amount
- Completion timestamp
- Handler information

### Handlers Collection (`handlers/`)
Stores handler/agent names for assignment.

## Date Handling

**Critical Pattern:** Firestore stores dates as Timestamp objects. Always convert to ISO strings for client compatibility:

```typescript
// When reading from Firestore
journeyDate: booking.journeyDate?.toDate?.()?.toISOString() || booking.journeyDate

// When writing to Firestore (optional, Firestore handles Dates)
journeyDate: new Date(journeyDateString)
```

## React Query Integration

**Custom Hooks Pattern:** Combine Firestore client SDK with React Query for caching and automatic refetching.

**Example Structure:**
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { collection, getDocs, addDoc, updateDoc } from 'firebase/firestore';

export function useBookings() {
  return useQuery({
    queryKey: ['bookings'],
    queryFn: async () => {
      const snapshot = await getDocs(collection(db, 'bookings'));
      return snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    },
    staleTime: 60000, // 60 seconds
  });
}

export function useUpdateBooking() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ id, data }) => {
      await updateDoc(doc(db, 'bookings', id), data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bookings'] });
    },
  });
}
```

**Key Hooks:** [src/hooks/](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/hooks/)
- useBookings.ts - Bookings data with infinite scroll
- useAccounts.ts - IRCTC account management
- useBookingRecords.ts - Completion records
- useHandlers.ts - Handler management

## Security Rules

**Current Status:** Rules allow unrestricted read/write for development.

**Production Requirements:** In production, add:
- Authentication checks (`request.auth != null`)
- User-specific access rules
- Data validation

**Configuration File:** [firestore.rules](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/firestore.rules)

Example production rules:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /bookings/{booking} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && 
        request.auth.uid == resource.data.userId;
    }
  }
}
```

## Firebase Configuration Files

**Project Config:** [.firebaserc](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/.firebaserc)
```json
{
  "projects": {
    "default": "your-project-id"
  }
}
```

**Hosting Config:** [firebase.json](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/firebase.json)
```json
{
  "hosting": {
    "public": "out",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

**Firestore Rules:** [firestore.rules](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/firestore.rules)

## Client SDK Setup

**Installation:** Dependencies in package.json
- `firebase` - Firebase client SDK
- `@tanstack/react-query` - Data fetching and caching

**Initialization:** [src/lib/firebase.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/lib/firebase.ts)
- Singleton pattern prevents multiple app instances
- Config validation on startup
- Exports db, auth, app instances

**Usage Pattern:**
```typescript
import { db } from '@/lib/firebase';
import { collection, getDocs } from 'firebase/firestore';

const snapshot = await getDocs(collection(db, 'bookings'));
```

## Common Patterns

### Adding a Document
```typescript
import { collection, addDoc } from 'firebase/firestore';
import { db } from '@/lib/firebase';

const docRef = await addDoc(collection(db, 'bookings'), {
  source: 'Station A',
  destination: 'Station B',
  status: 'pending',
  createdAt: new Date(),
});
```

### Updating a Document
```typescript
import { doc, updateDoc } from 'firebase/firestore';

await updateDoc(doc(db, 'bookings', bookingId), {
  status: 'completed',
  updatedAt: new Date(),
});
```

### Querying with Filters
```typescript
import { collection, query, where, getDocs } from 'firebase/firestore';

const q = query(
  collection(db, 'bookings'),
  where('status', '==', 'pending'),
  where('journeyDate', '>=', startDate)
);
const snapshot = await getDocs(q);
```

### Real-time Listener
```typescript
import { collection, onSnapshot } from 'firebase/firestore';

const unsubscribe = onSnapshot(
  query(collection(db, 'bookings'), where('status', '==', 'pending')),
  (snapshot) => {
    const bookings = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    // Update state or invalidate React Query
  }
);
```

## Troubleshooting

**Timestamp Conversion Errors:**
- Error: "Cannot serialize a BigInt" or similar
- Solution: Always convert Firestore Timestamps with `.toDate().toISOString()`

**Multiple App Instances:**
- Error: "Firebase: Firebase App named '[DEFAULT]' already exists"
- Solution: Use singleton pattern in firebase.ts

**Permission Denied Errors:**
- Check Firestore rules in firestore.rules
- Verify Firebase config in environment variables
- Ensure collection names match exactly

**Real-time Updates Not Working:**
- Verify onSnapshot is properly set up
- Check that query is valid
- Ensure component properly cleans up listeners

## Key Files Reference

- [src/lib/firebase.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/lib/firebase.ts) - Firebase initialization
- [src/hooks/useBookings.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/hooks/useBookings.ts) - Booking data hook
- [src/hooks/useAccounts.ts](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/src/hooks/useAccounts.ts) - Account data hook
- [firestore.rules](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/firestore.rules) - Security rules
- [firebase.json](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/firebase.json) - Hosting config
- [.firebaserc](file:///d:/WorkSpace/Learning/Cursor/TrainTrack/.firebaserc) - Project config
