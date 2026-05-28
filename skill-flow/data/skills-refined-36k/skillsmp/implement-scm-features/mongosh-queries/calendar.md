# Calendar & Scheduling Queries

## Unit Schedules

```bash
# List all unit schedules
mongosh "$DATABASE_URL" --eval "
db['unit-schedules'].find({}).forEach(printjson);
"

# Schedules for a school year
mongosh "$DATABASE_URL" --eval "
db['unit-schedules'].find({ schoolYear: '2024-2025' }).forEach(printjson);
"

# Schedules for a section
mongosh "$DATABASE_URL" --eval "
db['unit-schedules'].find({
  school: 'IS313',
  classSection: '802'
}).forEach(printjson);
"

# Current/active units
mongosh "$DATABASE_URL" --eval "
const today = new Date();
db['unit-schedules'].find({
  startDate: { \$lte: today },
  endDate: { \$gte: today }
}).forEach(printjson);
"

# Upcoming units
mongosh "$DATABASE_URL" --eval "
const today = new Date();
db['unit-schedules'].find({
  startDate: { \$gt: today }
}).sort({ startDate: 1 }).limit(10).forEach(printjson);
"
```

## Days Off

```bash
# List days off for a school year
mongosh "$DATABASE_URL" --eval "
db['days-off'].find({ schoolYear: '2024-2025' }).forEach(printjson);
"

# Upcoming days off
mongosh "$DATABASE_URL" --eval "
const today = new Date();
db['days-off'].find({
  date: { \$gte: today }
}).sort({ date: 1 }).forEach(printjson);
"
```

## Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `school` | string | School code |
| `classSection` | string | Section identifier |
| `schoolYear` | string | School year (e.g., "2024-2025") |
| `unitNumber` | number | Unit number |
| `startDate` | Date | Unit start date |
| `endDate` | Date | Unit end date |
