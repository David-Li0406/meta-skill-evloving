# Targets Reference

Complete reference for CHT targets.js configuration.

## Overview

Targets are key performance indicators displayed on the Targets/Analytics tab. All targets are defined in `targets.js` as an array of objects. Each object corresponds to a widget that shows in the app.

**Widget Types:**
- **Count**: Shows current totals, updates as reports are created
- **Percent**: Shows progress bars with numerator/denominator

## Complete Schema

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `id` | string | Unique identifier for the target. | Yes, unique |
| `icon` | string | Icon to show. Must match key in `resources.json`. | No |
| `translation_key` | translation key | Title of the target widget. | Yes |
| `subtitle_translation_key` | translation key | Subtitle (e.g., "This month", "All time"). | No |
| `percentage_count_translation_key` | translation key | Text below percent bar. Has `pass` and `total` variables. Default: `targets.count.default`. | No |
| `context` | string | JavaScript expression. Widget shows only if evaluates to true. `user` variable available. | No |
| `type` | 'count' or 'percent' | Widget type. | Yes |
| `goal` | integer | For percent: 0-100. For count: any positive number. Use -1 for no goal. | Yes |
| `appliesTo` | 'contacts' or 'reports' | Count reports or contacts. | Yes |
| `appliesToType` | string[] | Filter types. For reports: form codes. For contacts: contact types. | No |
| `appliesIf` | function(contact, report) | Return true to count document. For percent, controls denominator. | No |
| `passesIf` | function(contact, report) | For percent type: return true to increment numerator. | Yes for percent* |
| `date` | 'reported', 'now', or function | 'reported': current month only. 'now': all time. Function for custom. Default: 'now'. | No |
| `idType` | 'report', 'contact', or function | Controls counting. 'contact': count unique contacts. 'report': count all reports. Function returns array of IDs. | No |
| `groupBy` | function(contact, report) | Returns string to aggregate targets in groups. | No |
| `passesIfGroupCount` | object | Criteria for group passing. | Yes if groupBy defined |
| `passesIfGroupCount.gte` | number | Group passes if count >= this value. | Yes if groupBy defined |
| `dhis` | object or object[] | DHIS2 integration settings. | No |
| `visible` | boolean | Whether visible on targets page. Default: true. | No |
| `aggregate` | boolean | Display on TargetAggregates page (3.9+). | No |

*`passesIf` is forbidden when `groupBy` is defined.

## Code Examples

### Count Target - This Month

```javascript
{
  id: 'births-this-month',
  type: 'count',
  icon: 'infant',
  goal: -1,
  translation_key: 'targets.births.title',
  subtitle_translation_key: 'targets.this_month.subtitle',
  appliesTo: 'reports',
  appliesToType: ['delivery'],
  date: 'reported'
}
```

### Count Target - All Time with Goal

```javascript
{
  id: 'pregnancies-registered',
  type: 'count',
  icon: 'pregnancy',
  goal: 20,
  translation_key: 'targets.pregnancies.title',
  subtitle_translation_key: 'targets.all_time.subtitle',
  appliesTo: 'reports',
  appliesToType: ['pregnancy'],
  date: 'now'
}
```

### Percentage Target - Basic

```javascript
{
  id: 'delivery-with-visit',
  type: 'percent',
  icon: 'nurse',
  goal: 100,
  translation_key: 'targets.delivery_visit.title',
  appliesTo: 'reports',
  appliesToType: ['delivery'],
  appliesIf: function(contact, report) {
    return report.fields && report.fields.pregnancy_outcome === 'healthy';
  },
  passesIf: function(contact, report) {
    const ancForms = ['anc_visit', 'anc_followup'];
    const MAX_DAYS = 280;
    const visits = contact.reports.filter(r =>
      ancForms.includes(r.form) &&
      r.reported_date >= (report.reported_date - MAX_DAYS * 86400000) &&
      r.reported_date <= report.reported_date
    );
    return visits.length > 0;
  },
  date: 'now'
}
```

### Percentage Target with Context Filter

```javascript
{
  id: 'home-visits-chw',
  type: 'percent',
  icon: 'home-visit',
  goal: 100,
  translation_key: 'targets.home_visits.title',
  context: 'user.role === "chw"',
  appliesTo: 'contacts',
  appliesToType: ['person'],
  date: 'reported',
  passesIf: function(contact, report) {
    return contact.reports.some(r => r.form === 'home_visit');
  }
}
```

### Target with GroupBy (Families with 2+ Visits)

```javascript
{
  id: '2-home-visits-per-family',
  icon: 'home-visit',
  type: 'percent',
  goal: 100,
  translation_key: 'target.2-home-visits-per-family',
  context: 'user.role === "chw"',
  date: 'reported',
  appliesTo: 'contacts',
  appliesToType: ['person'],
  idType: function(contact) {
    // Create unique ID per family + date
    const householdVisitDates = new Set(
      contact.reports.map(report => toDateString(report.reported_date))
    );
    const familyId = contact.contact.parent._id;
    return Array.from(householdVisitDates).map(date => `${familyId}~${date}`);
  },
  groupBy: function(contact) {
    return contact.contact.parent._id;
  },
  passesIfGroupCount: { gte: 2 }
}
```

## Extras File Pattern

```javascript
// targets-extras.js
module.exports = {
  isHealthyDelivery: function(contact, report) {
    return report.form === 'D' ||
           (report.form === 'delivery' && report.fields.pregnancy_outcome === 'healthy');
  },

  countReportsSubmittedInWindow: function(reports, forms, start, end) {
    return reports.filter(r =>
      forms.includes(r.form) &&
      r.reported_date >= start &&
      r.reported_date <= end
    ).length;
  }
};
```

```javascript
// targets.js
const { isHealthyDelivery, countReportsSubmittedInWindow } = require('./targets-extras');

module.exports = [
  {
    id: 'healthy-deliveries',
    type: 'count',
    appliesTo: 'reports',
    appliesIf: isHealthyDelivery,
    // ...
  }
];
```

## Date Filter Behavior

| Value | Description |
|-------|-------------|
| `'reported'` | Only count documents with `reported_date` in current month |
| `'now'` | Count all documents regardless of date |
| `function(contact, report)` | Custom function returns Date to determine when document should count |

## Build Command

```bash
cht --local compile-app-settings backup-app-settings upload-app-settings
```
