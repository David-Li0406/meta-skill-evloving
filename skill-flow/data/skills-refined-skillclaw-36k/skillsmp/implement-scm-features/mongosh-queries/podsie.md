# Podsie Queries

## Podsie Completions

```bash
# Recent Podsie completions
mongosh "$DATABASE_URL" --eval "
db['podsie-completions'].find({}).sort({ createdAt: -1 }).limit(10).forEach(printjson);
"

# Completions for a student
mongosh "$DATABASE_URL" --eval "
db['podsie-completions'].find({ podsieStudentId: 'student-slug' }).forEach(printjson);
"

# Completions by assignment
mongosh "$DATABASE_URL" --eval "
db['podsie-completions'].find({ podsieAssignmentId: 'assignment-id' }).forEach(printjson);
"

# Completions in date range
mongosh "$DATABASE_URL" --eval "
const startDate = new Date('2024-01-01');
const endDate = new Date('2024-01-31');
db['podsie-completions'].find({
  createdAt: { \$gte: startDate, \$lte: endDate }
}).forEach(printjson);
"
```

## Aggregations

```bash
# Count completions per assignment
mongosh "$DATABASE_URL" --eval "
db['podsie-completions'].aggregate([
  { \$group: { _id: '\$assignmentName', count: { \$sum: 1 } } },
  { \$sort: { count: -1 } }
]).limit(20).forEach(printjson);
"

# Completions by date
mongosh "$DATABASE_URL" --eval "
db['podsie-completions'].aggregate([
  { \$group: {
    _id: { \$dateToString: { format: '%Y-%m-%d', date: '\$createdAt' } },
    count: { \$sum: 1 }
  }},
  { \$sort: { _id: -1 } },
  { \$limit: 14 }
]).forEach(printjson);
"
```

## Podsie Question Maps

```bash
# List question mappings
mongosh "$DATABASE_URL" --eval "
db['podsie-question-maps'].find({}).limit(10).forEach(printjson);
"

# Questions for a skill
mongosh "$DATABASE_URL" --eval "
db['podsie-question-maps'].find({ skillNumber: 'G8.01' }).forEach(printjson);
"
```

## Key Fields - Completions

| Field | Type | Description |
|-------|------|-------------|
| `podsieStudentId` | string | Podsie student identifier |
| `podsieAssignmentId` | string | Podsie assignment ID |
| `assignmentName` | string | Assignment name |
| `createdAt` | Date | Completion timestamp |
| `score` | number | Score achieved |
| `totalQuestions` | number | Total questions |
| `correctAnswers` | number | Correct answers |
