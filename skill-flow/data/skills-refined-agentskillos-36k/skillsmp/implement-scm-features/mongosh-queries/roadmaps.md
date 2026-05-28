# Roadmaps Queries

## Roadmap Units

```bash
# List all roadmap units
mongosh "$DATABASE_URL" --eval "
db['roadmaps-units'].find({}).forEach(printjson);
"

# Units by grade
mongosh "$DATABASE_URL" --eval "
db['roadmaps-units'].find({ grade: /7th Grade/i }).forEach(printjson);
"

# Unit by title
mongosh "$DATABASE_URL" --eval "
db['roadmaps-units'].findOne({ unitTitle: /Area and Surface Area/i });
"

# Count units per grade
mongosh "$DATABASE_URL" --eval "
db['roadmaps-units'].aggregate([
  { \$group: { _id: '\$grade', count: { \$sum: 1 } } },
  { \$sort: { count: -1 } }
]).forEach(printjson);
"
```

## Roadmap Skills

```bash
# List all skills
mongosh "$DATABASE_URL" --eval "
db['roadmaps-skills'].find({}).limit(20).forEach(printjson);
"

# Find skill by skill number
mongosh "$DATABASE_URL" --eval "
db['roadmaps-skills'].findOne({ skillNumber: 'G7.01' });
"

# Skills by grade
mongosh "$DATABASE_URL" --eval "
db['roadmaps-skills'].find({ grade: '7' }).forEach(printjson);
"

# Search skills by name
mongosh "$DATABASE_URL" --eval "
db['roadmaps-skills'].find({
  skillName: { \$regex: 'ratio', \$options: 'i' }
}).forEach(printjson);
"
```

## Roadmap Student Data

```bash
# Find student assessment data
mongosh "$DATABASE_URL" --eval "
db['roadmaps-student-data'].findOne({ studentId: 'john-doe' });
"

# Students with assessments
mongosh "$DATABASE_URL" --eval "
db['roadmaps-student-data'].find({
  'skillPerformances.0': { \$exists: true }
}).limit(5).forEach(printjson);
"

# Count students with data
mongosh "$DATABASE_URL" --eval "
print('Total:', db['roadmaps-student-data'].countDocuments());
"
```

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `grade` | string | Grade level |
| `unitTitle` | string | Unit name |
| `skillNumber` | string | Skill identifier (e.g., "G7.01") |
| `skillName` | string | Skill description |
| `targetSkills` | string[] | Primary skill numbers |

**ID Warning:** `students.studentID` (number) vs `roadmaps-student-data.studentId` (string slug)
