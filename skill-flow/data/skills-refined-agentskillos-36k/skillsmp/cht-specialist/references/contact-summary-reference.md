# Contact Summary Reference

Complete reference for CHT contact-summary.templated.js configuration.

## Overview

Contact profile pages display basic information, history, and upcoming tasks. The profile is defined by:
- **Fields**: Basic information shown on the profile
- **Cards**: Condition cards (e.g., pregnancy, active treatment)
- **Context**: Data passed to forms opened from the profile

## Available Variables

| Variable | Description |
|----------|-------------|
| `contact` | Currently selected contact. Has minimal stubs for `contact.parent`. |
| `reports` | Array of reports for contact or person children. Max 500 reports (50 before v4.7.0). |
| `lineage` | Array of contact's parents. `lineage[0]` is parent, `lineage[1]` is grandparent, etc. |
| `targetDoc` | Target document for the contact, hydrated with config. May be undefined. (3.9.0+) |
| `uhcStats` | UHC statistics object. (3.12.0+) |
| `uhcStats.uhcInterval` | Object with `start` and `end` timestamps of UHC reporting period. |
| `uhcStats.homeVisits` | Home visit stats including `lastVisitedDate`, `count`, `countGoal`. |
| `cht` | CHT API object for contact summary, targets, and tasks. (3.12.0+) |

## Fields Schema

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `label` | string | Translation key for field label. | Yes |
| `icon` | string | Icon name from Configuration > Icons. | No |
| `value` | string | Value to display. | Yes |
| `filter` | string | Display filter (see below). | No |
| `width` | integer | Horizontal space: 12 (full), 6 (half), 3 (quarter). Default: 12. | No |
| `translate` | boolean | Whether to translate the value. Default: false. | No |
| `context` | object | Translation variables when `translate: true`. | No |
| `appliesIf` | function() | Return true to show field. Default: true. | No |
| `appliesToType` | string[] | Filter contact types. Default: all types. | No |

### Available Filters

| Filter | Description |
|--------|-------------|
| `age` | Formats date as age (e.g., "11 years") |
| `phone` | Formats phone number |
| `weeksPregnant` | Weeks of pregnancy |
| `relativeDate` | Relative date (e.g., "3 days ago") |
| `relativeDay` | Relative day |
| `fullDate` | Full date format |
| `simpleDate` | Simple date format |
| `simpleDateTime` | Simple date and time |
| `lineage` | Displays hierarchy lineage |
| `resourceIcon` | Shows resource icon |
| `translate` | Translates value |

## Cards Schema

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `label` | translation key | Label on top of card. | Yes |
| `appliesToType` | string[] | Filter types. Use `['report']` for report cards. Default: all types. | No |
| `appliesIf` | function(report) or boolean | Return true to show card. | No |
| `modifyContext` | function(context, report) | Modify data passed to forms. | No |
| `fields` | array | Card field definitions. | Yes |
| `fields[n].appliesIf` | boolean or function(report) | Show/hide field. | No |
| `fields[n].label` | string or function(report) | Field label. | Yes |
| `fields[n].icon` | string or function(report) | Field icon. | No |
| `fields[n].value` | string or function(report) | Field value. | Yes |
| `fields[n].filter` | string or function(report) | Display filter. | No |
| `fields[n].width` | integer or function(report) | Horizontal space. | No |
| `fields[n].translate` | boolean or function(report) | Translate value. | No |
| `fields[n].context` | object | Translation variables. Only `count` and `total` supported on cards. | No |

## Complete Example

```javascript
// contact-summary.templated.js
const extras = require('./contact-summary-extras');

module.exports = {
  context: {
    use_cases: {
      anc: extras.isCoveredByUseCaseInLineage(lineage, 'anc'),
      pnc: extras.isCoveredByUseCaseInLineage(lineage, 'pnc'),
    },
    pregnant: extras.isActivePregnancy(contact, reports),
  },

  fields: [
    {
      appliesToType: 'person',
      label: 'patient_id',
      value: contact.patient_id,
      width: 4
    },
    {
      appliesToType: 'person',
      label: 'contact.age',
      value: contact.date_of_birth,
      width: 4,
      filter: 'age'
    },
    {
      appliesToType: 'person',
      label: 'contact.parent',
      value: lineage,
      filter: 'lineage'
    },
    {
      appliesToType: '!person',
      appliesIf: function() {
        return contact.parent && lineage[0];
      },
      label: 'contact.parent',
      value: lineage,
      filter: 'lineage'
    }
  ],

  cards: [
    {
      label: 'contact.profile.pregnancy',
      appliesToType: 'report',
      appliesIf: extras.isActivePregnancy,
      fields: [
        {
          label: 'contact.profile.edd',
          value: function(report) {
            return report.fields.edd_8601;
          },
          filter: 'relativeDay',
          width: 12
        },
        {
          label: 'contact.profile.visit',
          value: 'contact.profile.visits.of',
          translate: true,
          context: {
            count: function(report) {
              return extras.getSubsequentVisits(report).length;
            },
            total: 4,
          },
          width: 6
        },
        {
          label: 'contact.profile.risk.title',
          value: function(report) {
            return extras.isHighRiskPregnancy(report) ? 'high' : 'normal';
          },
          translate: true,
          width: 5,
          icon: function(report) {
            return extras.isHighRiskPregnancy(report) ? 'risk' : '';
          }
        }
      ],
      modifyContext: function(ctx) {
        ctx.pregnant = true;
      }
    }
  ]
};
```

## Extras File

```javascript
// contact-summary-extras.js
module.exports = {
  isActivePregnancy: function(report) {
    return report.form === 'pregnancy' &&
           !report.fields.delivered &&
           report.fields.edd > Date.now();
  },

  isCoveredByUseCaseInLineage: function(lineage, usecase) {
    return lineage.some(l => l.use_cases && l.use_cases.includes(usecase));
  },

  isHighRiskPregnancy: function(report) {
    return report.fields.risk_factors &&
           report.fields.risk_factors.length > 0;
  },

  getSubsequentVisits: function(report) {
    // Return visits after pregnancy registration
  }
};
```

## Care Guides (Context)

Data in the `context` object is available to forms opened from the profile:
- In form properties: `summary.pregnant`
- In XForm calculations: `instance('contact-summary')/context/pregnant`

**Note:** Context data is not available when editing previously completed forms or accessing forms outside the profile page.

## Build Command

```bash
cht --local compile-app-settings backup-app-settings upload-app-settings
```
