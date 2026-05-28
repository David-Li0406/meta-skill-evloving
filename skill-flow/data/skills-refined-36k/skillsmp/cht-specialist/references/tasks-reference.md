# Tasks Reference

Complete reference for CHT tasks.js configuration.

## Overview

Tasks are reminders or follow-ups that appear in the Tasks tab. Task generation is configured in `tasks.js`, which defines an array of task objects. Tasks are generated client-side and create documents that track status over time.

**Important Limits:**
- Tasks only show for users of type "restricted to their place"
- Tasks are generated between 60 days in the past and 180 days in the future (4.0.0+)
- Be conscious of generating too many tasks to avoid performance issues

## Complete Schema

| Property | Type | Description | Required |
|----------|------|-------------|----------|
| `name` | string | Unique identifier for the task. Used for querying task completeness. | Yes, unique |
| `icon` | string | Icon to show alongside the task. Must match a key in `resources.json`. | No |
| `title` | translation key | The title of the task shown to users. | Yes |
| `appliesTo` | 'contacts' or 'reports' | Emit one task per contact or per report. | Yes |
| `appliesIf` | function(contact, report) | Return true if task should appear. If `appliesTo: 'contacts'`, report is undefined. | No |
| `appliesToType` | string[] | Filter contacts or reports. For reports: form codes like `['pregnancy']`. For contacts: types like `['person']` or `['clinic']`. | No |
| `contactLabel` | string or function(contact, report) | Label describing the task subject. Defaults to `contact.contact.name`. | No |
| `resolvedIf` | function(contact, report, event, dueDate) | Return true to mark task as resolved. | No* |
| `events` | object[] | Array of event objects defining task timing. | Yes |
| `events[n].id` | string | Descriptive identifier for the event. | Yes if multiple events |
| `events[n].days` | integer | Days after `reported_date` the event is due. | Yes* |
| `events[n].dueDate` | function(event, contact, report) | Returns Date object for due date. | Yes* |
| `events[n].start` | integer | Days before due date to show task. | Yes |
| `events[n].end` | integer | Days after due date to show task. | Yes |
| `actions` | object[] | Forms/actions available when task is clicked. | Yes |
| `actions[n].type` | 'report' or 'contact' | 'report' opens form, 'contact' opens profile or contact form. Default: 'report'. | No |
| `actions[n].form` | string | Form code to open when action selected. | Yes if type='report' |
| `actions[n].label` | translation key | Label on task summary if multiple actions. | No |
| `actions[n].modifyContent` | function(content, contact, report, event) | Set values to pass as form inputs. | No |
| `priority` | object or function | High risk indicator configuration. | No |
| `priority.level` | integer | Positive number for urgency. Higher = top of list. | No |
| `priority.label` | translation key | Text shown with risk indicator. | No |

*Either `days` or `dueDate` is required for events.
*`resolvedIf` is required if any action type is 'report'.

## Code Examples

### Basic Task with Multiple Events

```javascript
module.exports = [
  {
    name: 'postnatal-followup',
    icon: 'mother-child',
    title: 'task.postnatal_followup',
    appliesTo: 'reports',
    appliesToType: ['delivery'],
    actions: [{ form: 'postnatal_visit' }],
    events: [
      { id: 'pnc-1', days: 7, start: 2, end: 2 },
      { id: 'pnc-2', days: 14, start: 2, end: 2 }
    ],
    resolvedIf: function(contact, report, event, dueDate) {
      return Utils.isFormSubmittedInWindow(
        contact.reports,
        'postnatal_visit',
        Utils.addDate(dueDate, -event.start).getTime(),
        Utils.addDate(dueDate, event.end + 1).getTime()
      );
    }
  }
];
```

### Contact-Based Task

```javascript
{
  name: 'family-survey',
  icon: 'family',
  title: 'task.family_survey.title',
  appliesTo: 'contacts',
  appliesToType: ['clinic'],
  actions: [{ form: 'family_survey' }],
  events: [{
    id: 'family-survey',
    days: 0,
    start: 0,
    end: 14
  }],
  resolvedIf: function(contact, report, event, dueDate) {
    return Utils.isFormSubmittedInWindow(
      contact.reports,
      'family_survey',
      Utils.addDate(dueDate, -event.start).getTime(),
      Utils.addDate(dueDate, event.end + 1).getTime()
    );
  }
}
```

### Task with Conditional Logic and Priority

```javascript
{
  name: 'home-delivery-followup',
  icon: 'mother-child',
  title: 'task.postnatal_followup.title',
  appliesTo: 'reports',
  appliesToType: ['D', 'delivery'],
  appliesIf: function(contact, report) {
    return report.fields &&
           report.fields.delivery_code &&
           report.fields.delivery_code.toUpperCase() !== 'F';
  },
  actions: [{
    form: 'postnatal_visit',
    modifyContent: function(content, contact, report, event) {
      content.delivery_place = 'home';
      content.event_id = event.id;
    }
  }],
  events: [{
    id: 'postnatal-home',
    days: 0,
    start: 0,
    end: 4
  }],
  priority: {
    level: 'high',
    label: 'task.priority.label.home_birth'
  },
  resolvedIf: function(contact, report, event, dueDate) {
    return Utils.isFormSubmittedInWindow(
      contact.reports,
      'postnatal_visit',
      Utils.addDate(dueDate, -event.start).getTime(),
      Utils.addDate(dueDate, event.end + 1).getTime()
    );
  }
}
```

### Task with Custom Due Date Function

```javascript
{
  name: 'recurring-survey',
  icon: 'family',
  title: 'task.family_survey.title',
  appliesTo: 'contacts',
  appliesToType: ['clinic'],
  appliesIf: extras.needsFamilySurvey,
  actions: [{ form: 'family_survey' }],
  events: [{
    id: 'family-survey',
    start: 0,
    end: 14,
    dueDate: extras.getNextFamilySurveyDate
  }],
  resolvedIf: function(contact, report, event, dueDate) {
    return Utils.isFormSubmittedInWindow(
      contact.reports,
      'family_survey',
      Utils.addDate(dueDate, -event.start).getTime(),
      Utils.addDate(dueDate, event.end + 1).getTime()
    );
  }
}
```

## Default ResolvedIf Behavior

If `resolvedIf` is undefined for a 'report' type action, it defaults to checking if any report matching the action's form was submitted during the task window.

You can also combine with default:
```javascript
resolvedIf: function(contact, report, event, dueDate) {
  return this.definition.defaultResolvedIf(contact, report, event, dueDate) && otherConditions;
}
```

## Extras File Pattern

For complex logic, use a separate `nools-extras.js` file:

```javascript
// nools-extras.js
module.exports = {
  isCoveredByUseCase: function(contact, usecase) {
    // Custom logic
  },
  getNewestDeliveryTimestamp: function(contact) {
    // Return timestamp of newest delivery
  },
  postnatalForms: ['postnatal_visit', 'pnc_visit']
};
```

```javascript
// tasks.js
const extras = require('./nools-extras');

module.exports = [
  {
    // ... task config using extras.isCoveredByUseCase, etc.
  }
];
```

## Build Command

```bash
cht --local compile-app-settings backup-app-settings upload-app-settings
```
