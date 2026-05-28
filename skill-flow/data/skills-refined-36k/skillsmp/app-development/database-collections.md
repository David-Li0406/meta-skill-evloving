# Database Collections Quick Reference

Practical mongosh commands for querying MongoDB collections in the AI Coaching Platform.

## Connection

```bash
# Always use the environment variable
mongosh "$DATABASE_URL" --eval "YOUR_COMMAND_HERE"
```

## Essential Commands

```bash
# List all collections
mongosh "$DATABASE_URL" --eval "db.getCollectionNames().forEach(print);"

# View documents (replace 'collection-name' with actual collection)
mongosh "$DATABASE_URL" --eval "db['collection-name'].find({}).limit(5).forEach(printjson);"

# Count documents
mongosh "$DATABASE_URL" --eval "print(db['collection-name'].countDocuments());"

# Find by field
mongosh "$DATABASE_URL" --eval "db['collection-name'].findOne({ field: 'value' });"

# Aggregation example
mongosh "$DATABASE_URL" --eval "
  db['collection-name'].aggregate([
    { \$group: { _id: '\$field', count: { \$sum: 1 } } }
  ]).forEach(printjson);
"
```

## Key Collections

| Collection | Purpose | Key Field |
|------------|---------|-----------|
| **students** | Student records | `studentID` (number) |
| **student_roster** | Class assignments | - |
| **roadmaps-student-data** | Assessment progress | `studentId` (string) ⚠️ |
| **roadmaps-skills** | Skill definitions | - |
| **roadmaps-units** | Unit definitions | - |
| **roadmaps-lesson** | Lesson content | - |
| **scope-and-sequence** | Skill progression | - |
| **section-configs** | Section settings | - |
| **activity-type-configs** | Activity types (max 10) | - |
| **student-activities** | Activity records | - |
| **classroomobservations_v2** | Observation records | - |
| **visits** | Coaching visits | - |
| **coachinglogs** | Session logs | - |
| **staffmembers** | Staff records | - |
| **schools** | School info | - |
| **page-views** | Analytics | `timestamp` |

⚠️ **ID Mismatch**: `students.studentID` (number) ≠ `roadmaps-student-data.studentId` (string)

## Common Queries

```bash
# Students
mongosh "$DATABASE_URL" --eval "db.students.find({}).limit(5).forEach(printjson);"
mongosh "$DATABASE_URL" --eval "db.students.findOne({ studentID: 123 });"

# Student progress
mongosh "$DATABASE_URL" --eval "db['roadmaps-student-data'].findOne({ studentId: 'john-doe' });"

# Skills
mongosh "$DATABASE_URL" --eval "db['roadmaps-skills'].find({}).forEach(printjson);"

# Activity types
mongosh "$DATABASE_URL" --eval "db['activity-type-configs'].find({}).forEach(printjson);"

# Recent page views
mongosh "$DATABASE_URL" --eval "db['page-views'].find({}).sort({ timestamp: -1 }).limit(10).forEach(printjson);"
```

## Pro Tips

- Use `.limit(N)` to test queries on small datasets
- Escape `$` as `\$` in shell commands
- Use aggregation for complex queries with `$group`, `$match`, `$sort`
- Check Mongoose models in `src/lib/schema/mongoose-schema/` for schema details
