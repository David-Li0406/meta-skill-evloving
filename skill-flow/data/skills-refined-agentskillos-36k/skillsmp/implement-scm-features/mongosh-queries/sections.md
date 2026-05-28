# Section Configs Queries

## Basic Queries

```bash
# List all section configs
mongosh "$DATABASE_URL" --eval "
db['section-configs'].find({}).forEach(printjson);
"

# Find section config by class section
mongosh "$DATABASE_URL" --eval "
db['section-configs'].findOne({ classSection: '802' });
"

# Sections by school
mongosh "$DATABASE_URL" --eval "
db['section-configs'].find({ school: 'IS313' }).forEach(printjson);
"

# Sections by grade level
mongosh "$DATABASE_URL" --eval "
db['section-configs'].find({ gradeLevel: '8' }).forEach(printjson);
"

# Sections with Podsie group IDs
mongosh "$DATABASE_URL" --eval "
db['section-configs'].find(
  { groupId: { \$exists: true, \$ne: null } },
  { classSection: 1, school: 1, groupId: 1 }
).forEach(printjson);
"

# Sections by scope and sequence tag
mongosh "$DATABASE_URL" --eval "
db['section-configs'].find({ scopeSequenceTag: 'Grade 8' }).forEach(printjson);
"
```

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `school` | string | School code |
| `classSection` | string | Section identifier (e.g., "802") |
| `teacher` | string | Teacher name |
| `gradeLevel` | string | Grade level |
| `scopeSequenceTag` | string | Links to scope-and-sequence (e.g., "Grade 8") |
| `groupId` | string | Podsie group ID for API sync |
| `specialPopulations` | string[] | Special populations |
| `assignmentContent` | array | Assignment configurations |
| `youtubeLinks` | array | Smartboard YouTube links |
