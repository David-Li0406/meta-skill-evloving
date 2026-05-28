# ADR 0030: Custom User Supplements

## Status
Proposed

## Context
Users want the ability to track medications or supplements that are not present in our curated global database. These items should be private to the individual user and must not be visible to others. However, they should integrate seamlessly into the existing Library, Search, and daily routine (Stack) features.

## Decision
We will implement a multi-tenancy model for supplements by:
1.  **Updating the `Supplement` Domain Entity**: Adding `userId` (String?) and `isCustom` (bool) fields. `userId` will be null for global database items and populated with the owner's ID for custom items.
2.  **Infrastructure Storage (Firestore)**:
    -   Global supplements remain in the root `/supplements` collection.
    -   Custom supplements will be stored in a private sub-collection: `/users/{userId}/custom_supplements`.
3.  **Repository Aggregation**: The `SupplementRepository.getAllSupplements` and `searchSupplements` methods will now accept an optional `userId`. When provided, the repository will perform two parallel reads (Global + User-specific) and merge the results before returning them to the ViewModel.
4.  **UI Identification**: Custom supplements will be visually distinguished in the UI using a "CUSTOM" badge to inform users that these are their private entries.

## Consequences
-   **Privacy**: Strong isolation is maintained as custom supplements are stored within the user's document path.
-   **Complexity**: Repository logic becomes slightly more complex due to data merging and parallel fetching.
-   **Performance**: The startup load for the Library involves an additional Firestore collection read, though this is mitigated by parallel execution and caching.
-   **Consistency**: Custom items can be added to Stacks just like global items because they share the same base `Supplement` model, ensuring full compatibility with the existing logging and notification systems.
