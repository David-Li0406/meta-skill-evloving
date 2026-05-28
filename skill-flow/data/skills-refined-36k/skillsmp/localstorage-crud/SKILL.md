---
name: localstorage-crud
description: Handle localStorage CRUD operations in React apps. Use when building features that persist data to browser storage, manage client-side state, or need offline-capable storage.
---

## localStorage CRUD Pattern

I help with client-side persistence using localStorage.

## Standard Pattern

1.Define TypeScript interface for data
2.Create storage utility with get/add/update/delete
3.Add Zod validation
4.Build custom hook for React integration
5.Handle serialization/deserialization

## Code Template

Storage utility structure:
-STORAGE_KEY constant
-getAll() returns parsed array
-add() pushes and saves
-remove() filters and saves
-search() filters by criteria

## Best Practices

-Always wrap in try-catch for JSON.parse errors
-Validate data with Zod before saving
-Use UUID for IDs (uuid package)
-Handle SSR: check typeof window !== 'undefined'
-Store dates as ISO strings, not Date objects
