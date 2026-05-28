---
name: firebase-cost-optimization
description: Firebase cost optimization patterns for Firestore, Storage, and Cloud Functions. Maximizes profit margin by minimizing unnecessary billing operations. Use when writing Firebase code, Firestore queries, Storage uploads, or Cloud Functions.
---

# Firebase Cost Optimization & Efficiency

> **Context**: This skill is triggered when the agent is writing code that interacts with Firebase Firestore, Storage, or Cloud Functions. The goal is to maximize profit margin by minimizing unnecessary billing operations.

---

## 1. Firestore Read Optimization

### Strategy: Local-First (Cache-Aside)

**Pattern**: Check `SwiftData` or `UserDefaults` for a cached version of a document before calling Firestore.

```swift
func getStory(id: String) async -> Story? {
    // Always check local cache first
    if let cached = localStore.fetch(id: id) { return cached }

    // Only hit Firestore if cache miss
    let remote = try await db.collection("stories").document(id).getDocument()

    // Save to local cache immediately after fetch
    localStore.save(remote.toStory())
    return remote.toStory()
}
```

> [!IMPORTANT]
> Every Firestore read costs money. Local cache reads are free.

---

### Strategy: Pagination

**Pattern**: Never fetch an entire collection. Always use `limit()` and `start(after:)`.

```swift
// ❌ BAD: Fetches entire collection
let allStories = try await db.collection("stories").getDocuments()

// ✅ GOOD: Paginated with limit
let firstPage = try await db.collection("stories")
    .order(by: "createdAt", descending: true)
    .limit(to: 20)
    .getDocuments()
```

> [!CAUTION]
> **Rule**: Max limit for any list view is **20 items**. No exceptions without explicit approval.

---

## 2. Firestore Write Optimization

### Strategy: Field-Level Updates

**Pattern**: Use `updateData()` for specific fields instead of `setData()` for the whole document.

```swift
// ❌ BAD: Rewrites entire document (bandwidth + potential trigger costs)
try await docRef.setData(user.toDictionary())

// ✅ GOOD: Updates only changed fields
try await docRef.updateData([
    "lastLogin": FieldValue.serverTimestamp(),
    "sessionCount": FieldValue.increment(Int64(1))
])
```

---

### Strategy: Batching

**Pattern**: If updating more than 2 related documents, use `writeBatch()`.

```swift
// ✅ GOOD: Single network round-trip for multiple writes
let batch = db.batch()
batch.updateData(["status": "completed"], forDocument: questRef)
batch.updateData(["xp": FieldValue.increment(Int64(50))], forDocument: userRef)
batch.setData(achievementData, forDocument: achievementRef)
try await batch.commit()
```

> [!TIP]
> Batches are atomic and count as a single operation for billing purposes.

---

## 3. Storage & AI Image Optimization

### Strategy: Semantic Asset Deduplication

**Logic**: Before generating an image, check the `generated_assets` collection for existing tags matching the prompt.

```swift
func getOrGenerateImage(prompt: String, tags: [String]) async -> URL {
    // Check for existing asset with matching tags
    let existing = try await db.collection("generated_assets")
        .whereField("tags", arrayContainsAny: tags)
        .limit(to: 1)
        .getDocuments()

    if let match = existing.documents.first {
        return URL(string: match.data()["storageURL"] as! String)!
    }

    // Only generate if no match exists
    let newImageURL = try await generateWithImagen(prompt: prompt)

    // Cache for future reuse
    try await db.collection("generated_assets").addDocument(data: [
        "tags": tags,
        "prompt": prompt,
        "storageURL": newImageURL.absoluteString,
        "createdAt": FieldValue.serverTimestamp()
    ])

    return newImageURL
}
```

> [!IMPORTANT]
> **Rule**: If a "Forest" image exists and matches the prompt's vibe, return the existing `storageURL`. Never regenerate similar images.

---

## 4. Cloud Function Execution

### Strategy: Request Validation (Rate Limiting)

**Rule**: Every expensive AI function must check the user's `usage_tier` and `current_month_count` before executing the Gemini or Imagen API call.

```typescript
export const generateStory = onCall(async (request) => {
  const userId = request.auth?.uid;
  if (!userId) throw new HttpsError("unauthenticated", "Must be logged in");

  // Check usage limits BEFORE expensive operations
  const userDoc = await db.collection("users").doc(userId).get();
  const userData = userDoc.data();

  const tierLimits = { free: 5, basic: 50, premium: 500 };
  const limit = tierLimits[userData.usage_tier] || 5;

  if (userData.current_month_count >= limit) {
    throw new HttpsError("resource-exhausted", "Monthly limit reached", {
      code: 429,
      limit: limit,
      current: userData.current_month_count,
    });
  }

  // Proceed with expensive AI call only after validation
  const story = await callGeminiAPI(request.data.prompt);

  // Increment usage counter
  await db
    .collection("users")
    .doc(userId)
    .update({
      current_month_count: FieldValue.increment(1),
    });

  return story;
});
```

> [!CAUTION]
> **Implementation**: Return a custom error `429 (Too Many Requests)` if the user has hit their tier limit. Never let unbounded AI calls execute.

---

## 5. Network Efficiency

### Strategy: JSON vs. Documents

**Pattern**: For large, static data (like a pre-written "Starter Pack" of stories), store a single compressed JSON file in Firebase Storage rather than individual documents in Firestore.

| Approach               | Cost for 100 items   |
| ---------------------- | -------------------- |
| 100 Firestore docs     | 100 read operations  |
| 1 JSON file in Storage | 1 download operation |

```swift
// ✅ GOOD: Single file download for static content
func loadStarterPack() async -> [Story] {
    let storageRef = Storage.storage().reference(withPath: "static/starter_pack.json")
    let data = try await storageRef.data(maxSize: 5 * 1024 * 1024)
    return try JSONDecoder().decode([Story].self, from: data)
}
```

> [!TIP]
> Reading 1 file is significantly cheaper than 100 document reads. Use this for any static content that changes infrequently.

---

## Quick Reference Checklist

Before submitting any Firebase-related code, verify:

- [ ] **Reads**: Local cache checked before Firestore?
- [ ] **Pagination**: Using `limit()` with max 20 items?
- [ ] **Writes**: Using `updateData()` instead of `setData()` where possible?
- [ ] **Batching**: Multiple related writes using `writeBatch()`?
- [ ] **AI Calls**: Usage tier validated before expensive operations?
- [ ] **Images**: Checked for existing similar assets before generation?
- [ ] **Static Data**: Using Storage JSON instead of many Firestore docs?
