# Utils Functions Reference

The `Utils` object is available globally in `tasks.js` and `targets.js` files. It provides helper functions for common operations.

## Function Reference

| Function | Description |
|----------|-------------|
| `Utils.addDate(date, days)` | Add days to date, returns new Date |
| `Utils.isFormSubmittedInWindow(reports, form, start, end)` | Check if form was submitted in time window |
| `Utils.getMostRecentReport(reports, form)` | Get latest report of specified form |
| `Utils.getMostRecentTimestamp(reports, form)` | Get latest reported_date for form |
| `Utils.getField(report, fieldPath)` | Get nested field value from report |
| `Utils.isTimely(date, event)` | Check if date falls within event window |
| `Utils.getLmpDate(doc)` | Extract LMP date from document |
| `Utils.isDateValid(date)` | Validate date object |
| `Utils.now()` | Get current date |
| `Utils.MS_IN_DAY` | Constant: milliseconds in a day (86400000) |

## Detailed Function Descriptions

### Utils.addDate(date, days)

Adds a number of days to a date and returns a new Date object.

```javascript
const dueDate = Utils.addDate(report.reported_date, 7);  // 7 days after report
const startWindow = Utils.addDate(dueDate, -2);          // 2 days before due
```

### Utils.isFormSubmittedInWindow(reports, form, start, end)

Checks if a specific form was submitted within a time window. Returns boolean.

```javascript
// Check if postnatal_visit was submitted between start and end timestamps
const completed = Utils.isFormSubmittedInWindow(
  contact.reports,
  'postnatal_visit',
  Utils.addDate(dueDate, -event.start).getTime(),
  Utils.addDate(dueDate, event.end + 1).getTime()
);
```

### Utils.getMostRecentReport(reports, form)

Returns the most recent report matching the specified form code, or undefined if none found.

```javascript
const lastPregnancy = Utils.getMostRecentReport(contact.reports, 'pregnancy');
if (lastPregnancy) {
  const edd = lastPregnancy.fields.edd;
}
```

### Utils.getMostRecentTimestamp(reports, form)

Returns the `reported_date` timestamp of the most recent matching report, or 0 if none found.

```javascript
const lastVisitTime = Utils.getMostRecentTimestamp(contact.reports, 'home_visit');
const daysSinceVisit = (Utils.now().getTime() - lastVisitTime) / Utils.MS_IN_DAY;
```

### Utils.getField(report, fieldPath)

Safely retrieves a nested field value from a report using dot notation. Returns undefined if path doesn't exist.

```javascript
const hasCough = Utils.getField(report, 'symptoms.cough') === 'yes';
const weight = Utils.getField(report, 'vitals.weight_kg');
const referralReason = Utils.getField(report, 'referral.reason.primary');
```

### Utils.isTimely(date, event)

Checks if a date falls within the event's start/end window. Used internally by task resolution.

```javascript
// Check if submission date is within the event window
const onTime = Utils.isTimely(submissionDate, event);
```

### Utils.getLmpDate(doc)

Extracts the Last Menstrual Period (LMP) date from a pregnancy-related document. Handles various field locations.

```javascript
const lmpDate = Utils.getLmpDate(pregnancyReport);
if (lmpDate) {
  const weeksPregnant = Math.floor((Utils.now() - lmpDate) / (7 * Utils.MS_IN_DAY));
}
```

### Utils.isDateValid(date)

Validates that a value is a valid Date object. Returns boolean.

```javascript
const birthDate = new Date(contact.date_of_birth);
if (Utils.isDateValid(birthDate)) {
  // Safe to use birthDate
}
```

### Utils.now()

Returns the current date. Use this instead of `new Date()` for testability.

```javascript
const today = Utils.now();
const age = Math.floor((today - birthDate) / (365.25 * Utils.MS_IN_DAY));
```

### Utils.MS_IN_DAY

Constant representing the number of milliseconds in a day (86400000).

```javascript
const daysDiff = (date2 - date1) / Utils.MS_IN_DAY;
const weeksDiff = daysDiff / 7;
```

## Common Patterns

### Check if follow-up is overdue

```javascript
appliesIf: function(contact, report) {
  const lastFollowup = Utils.getMostRecentTimestamp(contact.reports, 'followup');
  const daysSince = (Utils.now().getTime() - lastFollowup) / Utils.MS_IN_DAY;
  return daysSince > 30;  // Overdue if more than 30 days
}
```

### Calculate age from date of birth

```javascript
const birthDate = new Date(contact.date_of_birth);
if (Utils.isDateValid(birthDate)) {
  const ageInDays = (Utils.now() - birthDate) / Utils.MS_IN_DAY;
  const ageInYears = Math.floor(ageInDays / 365.25);
}
```

### Find reports within date range

```javascript
const reportsThisMonth = contact.reports.filter(r => {
  const startOfMonth = new Date();
  startOfMonth.setDate(1);
  startOfMonth.setHours(0, 0, 0, 0);
  return r.reported_date >= startOfMonth.getTime();
});
```
