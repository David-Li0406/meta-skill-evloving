# Analytics & Aggregation Queries

## Student Progress Summary

```bash
# Students per section with mastery stats
mongosh "$DATABASE_URL" --eval "
db.students.aggregate([
  { \$match: { active: true } },
  { \$group: {
    _id: { school: '\$school', section: '\$section' },
    totalStudents: { \$sum: 1 },
    avgMasteredSkills: { \$avg: { \$size: { \$ifNull: ['\$masteredSkills', []] } } }
  }},
  { \$sort: { '_id.school': 1, '_id.section': 1 } }
]).forEach(printjson);
"

# Skills mastery distribution
mongosh "$DATABASE_URL" --eval "
db.students.aggregate([
  { \$match: { active: true, masteredSkills: { \$exists: true } } },
  { \$project: { masteredCount: { \$size: '\$masteredSkills' } } },
  { \$group: {
    _id: '\$masteredCount',
    studentCount: { \$sum: 1 }
  }},
  { \$sort: { _id: 1 } }
]).forEach(printjson);
"
```

## Podsie Activity

```bash
# Completions by date (last 2 weeks)
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

# Top assignments by completion count
mongosh "$DATABASE_URL" --eval "
db['podsie-completions'].aggregate([
  { \$group: { _id: '\$assignmentName', count: { \$sum: 1 } } },
  { \$sort: { count: -1 } },
  { \$limit: 10 }
]).forEach(printjson);
"
```

## Collection Stats

```bash
# Count documents in all SCM collections
mongosh "$DATABASE_URL" --eval "
const collections = [
  'students',
  'section-configs',
  'podsie-completions',
  'roadmaps-units',
  'roadmaps-skills',
  'scope-and-sequence',
  'learning-content',
  'unit-schedules'
];
collections.forEach(c => {
  print(c + ':', db[c].countDocuments());
});
"
```

## Cross-Collection Analysis

```bash
# Students without section config
mongosh "$DATABASE_URL" --eval "
const sections = db['section-configs'].distinct('classSection');
db.students.find({
  active: true,
  section: { \$nin: sections }
}, { studentID: 1, firstName: 1, lastName: 1, section: 1 }).forEach(printjson);
"
```
