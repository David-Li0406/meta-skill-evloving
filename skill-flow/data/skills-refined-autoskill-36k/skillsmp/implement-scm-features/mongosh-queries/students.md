# Students Collection Queries

## Basic Queries

```bash
# List all students (limited)
mongosh "$DATABASE_URL" --eval "
db.students.find({}).limit(10).forEach(printjson);
"

# Find student by ID
mongosh "$DATABASE_URL" --eval "
db.students.findOne({ studentID: 12345 });
"

# Students by section
mongosh "$DATABASE_URL" --eval "
db.students.find({ section: '802', active: true }).forEach(printjson);
"

# Students by school
mongosh "$DATABASE_URL" --eval "
db.students.find({ school: 'IS313', active: true }).forEach(printjson);
"

# Search student by name
mongosh "$DATABASE_URL" --eval "
db.students.find({
  \$or: [
    { firstName: { \$regex: 'John', \$options: 'i' } },
    { lastName: { \$regex: 'Smith', \$options: 'i' } }
  ]
}).forEach(printjson);
"
```

## Aggregations

```bash
# Count students per section
mongosh "$DATABASE_URL" --eval "
db.students.aggregate([
  { \$match: { active: true } },
  { \$group: { _id: { school: '\$school', section: '\$section' }, count: { \$sum: 1 } } },
  { \$sort: { '_id.school': 1, '_id.section': 1 } }
]).forEach(printjson);
"

# Students with mastered skills
mongosh "$DATABASE_URL" --eval "
db.students.find(
  { masteredSkills: { \$exists: true, \$ne: [] } },
  { studentID: 1, firstName: 1, lastName: 1, masteredSkills: 1 }
).limit(5).forEach(printjson);
"
```

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `studentID` | number | Unique identifier |
| `firstName` | string | First name |
| `lastName` | string | Last name |
| `school` | string | School code (IS313, PS19, X644) |
| `section` | string | Class section (e.g., "802") |
| `gradeLevel` | string | Grade level |
| `email` | string | Student email |
| `active` | boolean | Active status |
| `masteredSkills` | string[] | Skill numbers mastered |
| `skillPerformances` | array | Assessment attempts |
| `podsieProgress` | array | Podsie assignment progress |
