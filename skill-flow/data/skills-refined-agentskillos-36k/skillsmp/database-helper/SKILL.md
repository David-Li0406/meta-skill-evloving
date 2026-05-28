---
name: database-helper
description: Assist with IndexedDB/Dexie.js database operations, migrations, and data management
---

# Database Operations Guide

## Schema Location

- `src/services/db.ts` - Dexie database definition
- Tables: `jobs`, `settings`, `memories`, `careerProjects`, `learningTasks`

## Common Operations

```typescript
import { db } from './db';

// Get all jobs
const jobs = await db.jobs.toArray();

// Get single job by ID
const job = await db.jobs.get(id);

// Add new job
const newId = await db.jobs.add(jobData);

// Update job (full replace)
await db.jobs.put({ ...job, ...updates });

// Partial update
await db.jobs.update(id, { status: 'Applied' });

// Delete job
await db.jobs.delete(id);

// Query with filters
const remoteJobs = await db.jobs
  .where('summary.jobType')
  .equals('remote')
  .toArray();

// Bulk operations
await db.jobs.bulkPut(jobsArray);
await db.jobs.bulkDelete(idArray);
```

## Settings Access

```typescript
// Get app settings
const settings = await db.settings.get('app-settings');

// Update settings
await db.settings.put({ id: 'app-settings', ...updates });

// Access outside React
import { useAppStore } from './stores/appStore';
const { settings } = useAppStore.getState();
```

## Migration Notes

- Version changes require schema migration in `db.ts`
- Always preserve existing data during migrations
- Test with existing data before deploying
- Dexie auto-upgrades when version number increases

## Key Types

```typescript
interface Job {
  id: string;
  company: string;
  title: string;
  jdText: string;
  status: string;
  dateAdded: Date;
  lastUpdated: Date;
  summary: JobSummary | null;
  resumeAnalysis: ResumeAnalysis | null;
  coverLetter: string | null;
  // ... see src/types/index.ts for full definition
}
```

## Export/Import

```typescript
// Export all data
const exportData = {
  jobs: await db.jobs.toArray(),
  settings: await db.settings.get('app-settings'),
  memories: await db.memories.toArray(),
};

// Import data
await db.jobs.bulkPut(importedJobs);
```
