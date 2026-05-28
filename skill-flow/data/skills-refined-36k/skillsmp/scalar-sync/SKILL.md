---
name: scalar-sync
description: "SCALAR hierarchy bidirectional sync patterns for Prometheus. Provides: (1) Canonical data store patterns, (2) Deterministic numbering (1.2.3 format), (3) LessonEditor ↔ ScalarDock sync, (4) Topic/Subtopic CRUD operations, (5) LO linking patterns. Triggers: SCALAR, hierarchy, sync, topic, subtopic, learning objective, LO, canonical, bidirectional, numbering."
---

# SCALAR Sync Skill

## Purpose

Document and enforce the bidirectional sync patterns between LessonEditor and ScalarDock in the Prometheus DESIGN section. This skill codifies the patterns implemented in the 2025-01-14 session.

## Architecture Overview

### Data Flow

```
┌─────────────────┐                    ┌─────────────────┐
│  LessonEditor   │ ←──────────────────│   ScalarDock    │
│  (Topics List)  │       SYNC         │  (SCALAR Tree)  │
└────────┬────────┘                    └────────┬────────┘
         │                                      │
         │         ┌──────────────┐             │
         └────────→│ DesignContext│←────────────┘
                   │ (Canonical)   │
                   └──────────────┘
```

### Single Source of Truth

**Canonical Data Store** (`canonicalData` in DesignContext):
```javascript
canonicalData: {
  modules: {},      // moduleId -> { id, name, order }
  los: {},          // loId -> { id, moduleId, verb, description, order }
  topics: {},       // topicId -> { id, loId, title, order }
  subtopics: {},    // subtopicId -> { id, topicId, title, order }
  pcs: {}           // pcId -> { id, description, color }
}
```

**Derived Data:**
- `scalarData` - Tree structure derived from canonical for ScalarDock rendering
- `lesson.topics` - Topic references stored on lessons

## Deterministic Numbering

### Serial Number Format

| Level | Format | Example |
|-------|--------|---------|
| LO | `{lo.order}` | 1, 2, 3 |
| Topic (linked) | `{lo.order}.{topic.orderWithinLO}` | 1.1, 1.2, 2.1 |
| Topic (unlinked) | `x.{orderWithinUnlinked}` | x.1, x.2 |
| Subtopic | `{topicSerial}.{subtopic.orderWithinTopic}` | 1.1.1, 1.2.3, x.1.2 |

### Computation Functions

```javascript
// Located in: src/contexts/DesignContext.jsx

/**
 * Compute topic serial number from canonical data
 * @returns {string} Serial like "1.2" or "x.3"
 */
function computeTopicSerial(topic, losMap, topicsMap) {
  if (!topic) return '?.?'

  if (!topic.loId) {
    // Unlinked topic: x.{orderWithinUnlinked}
    const unlinkedTopics = Object.values(topicsMap)
      .filter(t => t.loId === null)
      .sort((a, b) => (a.order || 0) - (b.order || 0))
    const idx = unlinkedTopics.findIndex(t => t.id === topic.id)
    return `x.${idx >= 0 ? idx + 1 : topic.order || 1}`
  }

  // Linked topic: {loOrder}.{orderWithinLO}
  const lo = losMap[topic.loId]
  if (!lo) return `?.${topic.order || 1}`

  const loTopics = Object.values(topicsMap)
    .filter(t => t.loId === topic.loId)
    .sort((a, b) => (a.order || 0) - (b.order || 0))
  const idx = loTopics.findIndex(t => t.id === topic.id)
  return `${lo.order}.${idx >= 0 ? idx + 1 : topic.order || 1}`
}

/**
 * Compute subtopic serial number
 * @returns {string} Serial like "1.2.3" or "x.1.2"
 */
function computeSubtopicSerial(subtopic, topicsMap, losMap, subtopicsMap) {
  if (!subtopic) return '?.?.?'

  const parentTopic = topicsMap[subtopic.topicId]
  if (!parentTopic) return `?.?.${subtopic.order || 1}`

  const topicSerial = computeTopicSerial(parentTopic, losMap, topicsMap)

  const siblingSubtopics = Object.values(subtopicsMap)
    .filter(s => s.topicId === subtopic.topicId)
    .sort((a, b) => (a.order || 0) - (b.order || 0))
  const idx = siblingSubtopics.findIndex(s => s.id === subtopic.id)

  return `${topicSerial}.${idx >= 0 ? idx + 1 : subtopic.order || 1}`
}
```

### Key Rule: Serial Numbers Are NEVER Stored

Serial numbers are always computed on-the-fly from the canonical structure. This ensures:
- No stale numbers
- Automatic recalculation on reorder
- Consistent display across all views

## Bidirectional Sync Matrix

### LessonEditor → ScalarDock

| LessonEditor Action | ScalarDock Effect |
|---------------------|-------------------|
| Add Topic | Topic appears in SCALAR tree under linked LO |
| Add Subtopic | Subtopic appears under parent Topic |
| Edit Topic title | SCALAR tree node title updates |
| Edit Subtopic title | SCALAR tree node title updates |
| Delete Topic | Topic removed from SCALAR tree |
| Delete Subtopic | Subtopic removed from SCALAR tree |

### ScalarDock → LessonEditor

| ScalarDock Action | LessonEditor Effect |
|-------------------|---------------------|
| Edit Topic title | Lesson topic reference title updates |
| Edit Subtopic title | Lesson subtopic reference title updates |
| Delete Topic | Topic removed from all lessons referencing it |
| Delete Subtopic | Subtopic removed from all lessons referencing it |
| Reorder Topic | Serial numbers recalculate in LessonEditor |
| Link/Unlink Topic | Serial numbers recalculate (x.n ↔ n.m) |

## Key Sync Functions

### 1. addTopicToLesson (LessonEditor → Canonical)

**Location:** `src/contexts/DesignContext.jsx:1211`

**Pattern:**
```javascript
const addTopicToLesson = useCallback((lessonId, topicTitle = 'New Topic') => {
  // 1. Generate IDs for both local and canonical
  const lessonTopicId = `topic-lesson-${timestamp}`
  const scalarTopicId = `topic-scalar-${timestamp}`

  // 2. Find lesson and get primary LO
  const lesson = lessons.find(l => l.id === lessonId)
  const primaryLOId = lesson.learningObjectives?.[0] || null

  // 3. Add to lesson.topics array
  setLessons(prev => prev.map(l => {
    if (l.id === lessonId) {
      return {
        ...l,
        topics: [...(l.topics || []), {
          id: lessonTopicId,
          scalarTopicId,
          title: topicTitle,
          number: computedSerial
        }]
      }
    }
    return l
  }))

  // 4. Add to canonical data store (CRITICAL for sync)
  setCanonicalData(prev => ({
    ...prev,
    topics: {
      ...prev.topics,
      [scalarTopicId]: {
        id: scalarTopicId,
        loId: primaryLOId,  // Links to LO for numbering
        title: topicTitle,
        order: nextOrder
      }
    }
  }))
})
```

### 2. updateScalarNode (ScalarDock → Lessons)

**Location:** `src/contexts/DesignContext.jsx`

**Pattern:**
```javascript
const updateScalarNode = useCallback((nodeId, updates) => {
  // 1. Update canonical store
  setCanonicalData(prev => {
    // Find which map contains the node
    if (prev.topics[nodeId]) {
      return {
        ...prev,
        topics: { ...prev.topics, [nodeId]: { ...prev.topics[nodeId], ...updates } }
      }
    }
    if (prev.subtopics[nodeId]) {
      return {
        ...prev,
        subtopics: { ...prev.subtopics, [nodeId]: { ...prev.subtopics[nodeId], ...updates } }
      }
    }
    return prev
  })

  // 2. Propagate to lessons referencing this node
  setLessons(prev => prev.map(lesson => ({
    ...lesson,
    topics: (lesson.topics || []).map(t => {
      if (t.scalarTopicId === nodeId) {
        return { ...t, title: updates.title ?? t.title }
      }
      return {
        ...t,
        subtopics: (t.subtopics || []).map(st =>
          st.scalarSubtopicId === nodeId
            ? { ...st, title: updates.title ?? st.title }
            : st
        )
      }
    })
  })))
})
```

### 3. deleteScalarNode (ScalarDock → Lessons)

**Pattern:**
```javascript
const deleteScalarNode = useCallback((nodeId) => {
  // 1. Remove from canonical store
  setCanonicalData(prev => {
    const { [nodeId]: removed, ...remainingTopics } = prev.topics
    const { [nodeId]: removedSub, ...remainingSubtopics } = prev.subtopics
    return {
      ...prev,
      topics: remainingTopics,
      subtopics: remainingSubtopics
    }
  })

  // 2. Remove from all lessons
  setLessons(prev => prev.map(lesson => ({
    ...lesson,
    topics: (lesson.topics || [])
      .filter(t => t.scalarTopicId !== nodeId)
      .map(t => ({
        ...t,
        subtopics: (t.subtopics || []).filter(st => st.scalarSubtopicId !== nodeId)
      }))
  })))

  // 3. Recalculate order numbers
  recalculateGroupOrders()
})
```

## ID Linking Pattern

Each topic/subtopic has TWO IDs:

| ID Type | Purpose | Format |
|---------|---------|--------|
| `lessonTopicId` | Local reference in lesson.topics | `topic-lesson-{timestamp}` |
| `scalarTopicId` | Canonical store key | `topic-scalar-{timestamp}` |

**Linking:**
```javascript
lesson.topics = [
  {
    id: 'topic-lesson-123',           // Local ID
    scalarTopicId: 'topic-scalar-123', // Canonical reference
    title: 'Topic Title',
    number: '1.2'
  }
]
```

## Order Recalculation

When topics are added, removed, or reordered:

```javascript
function recalculateCanonicalGroupOrders(topicsMap, loId) {
  // Get all topics in the group (same LO or unlinked)
  const groupTopics = Object.values(topicsMap)
    .filter(t => t.loId === loId)
    .sort((a, b) => (a.order || 0) - (b.order || 0))

  // Reassign sequential order numbers
  groupTopics.forEach((topic, idx) => {
    topicsMap[topic.id] = { ...topic, order: idx + 1 }
  })
}
```

## Debugging

Debug logging is enabled via:
```javascript
const DEBUG_HIERARCHY = true // src/contexts/DesignContext.jsx:42
```

Log format:
```
🔧 [HH:MM:SS.mmm] ACTION_NAME
  Data: { ... }
  Stack trace: ...
```

## Common Pitfalls

### 1. Data Store Mismatch
**Problem:** Writing to `lesson.topics` but not `canonicalData`
**Solution:** Always update BOTH stores in sync functions

### 2. Stale Serial Numbers
**Problem:** Storing serial numbers instead of computing
**Solution:** Always compute on render, never store

### 3. Missing Propagation
**Problem:** ScalarDock changes not reaching lessons
**Solution:** Ensure `updateScalarNode` propagates to `setLessons`

### 4. Orphaned References
**Problem:** Deleted canonical item still referenced in lessons
**Solution:** `deleteScalarNode` must clean both stores

## Testing Patterns

### Verify Sync

```javascript
// Test: Add topic in LessonEditor, verify in ScalarDock
test('topic added in editor appears in SCALAR', async ({ page }) => {
  // Add topic via LessonEditor
  await page.click('[data-testid="add-topic-btn"]')
  await page.fill('[data-testid="topic-title"]', 'Test Topic')
  await page.click('[data-testid="save-topic"]')

  // Verify in ScalarDock
  await expect(page.locator('[data-testid="scalar-tree"] >> text=Test Topic')).toBeVisible()
})

// Test: Edit in ScalarDock, verify in LessonEditor
test('scalar edit propagates to editor', async ({ page }) => {
  // Edit in ScalarDock
  await page.dblclick('[data-testid="scalar-topic-1"]')
  await page.fill('[data-testid="scalar-topic-input"]', 'Updated Title')
  await page.press('[data-testid="scalar-topic-input"]', 'Enter')

  // Verify in LessonEditor
  await expect(page.locator('[data-testid="lesson-topic-title"]')).toHaveText('Updated Title')
})
```

## File References

| File | Purpose |
|------|---------|
| `src/contexts/DesignContext.jsx` | Canonical store, sync functions |
| `src/components/design/LessonEditor.jsx` | Lesson-side topic editing |
| `src/components/design/ScalarDock.jsx` | SCALAR tree view |
| `src/utils/canonicalAdapter.js` | Canonical data utilities |

## See Also

- `/sat-courseware` - SCALAR hierarchy definitions
- `/prometheus-testing` - Testing patterns for sync verification
- `docs/STATUS.md` - Session notes on sync implementation
