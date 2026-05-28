/**
 * CHT Tasks Configuration Template
 *
 * This file defines tasks that appear in the Tasks tab.
 * Tasks are reminders or follow-ups for health workers.
 */

const extras = require('./nools-extras');

module.exports = [
  // Example: Report-based task
  {
    name: 'postnatal-followup',
    icon: 'mother-child',
    title: 'task.postnatal_followup',
    appliesTo: 'reports',
    appliesToType: ['delivery'],
    appliesIf: function(contact, report) {
      // Only show if delivery was successful
      return report.fields &&
             report.fields.delivery_outcome === 'live_birth';
    },
    actions: [{
      form: 'postnatal_visit',
      modifyContent: function(content, contact, report, event) {
        // Pass data to the form
        content.delivery_date = report.fields.delivery_date;
        content.visit_number = event.id;
      }
    }],
    events: [
      { id: 'pnc-day3', days: 3, start: 1, end: 2 },
      { id: 'pnc-day7', days: 7, start: 2, end: 2 },
      { id: 'pnc-day14', days: 14, start: 2, end: 3 }
    ],
    priority: function(contact, report) {
      if (report.fields.risk_factors && report.fields.risk_factors.length > 0) {
        return {
          level: 'high',
          label: 'task.priority.high_risk'
        };
      }
      return null;
    },
    resolvedIf: function(contact, report, event, dueDate) {
      return Utils.isFormSubmittedInWindow(
        contact.reports,
        'postnatal_visit',
        Utils.addDate(dueDate, -event.start).getTime(),
        Utils.addDate(dueDate, event.end + 1).getTime()
      );
    }
  },

  // Example: Contact-based task
  {
    name: 'household-visit',
    icon: 'home',
    title: 'task.household_visit',
    appliesTo: 'contacts',
    appliesToType: ['clinic'],
    appliesIf: function(contact) {
      // Check if household needs a visit
      return extras.needsHouseholdVisit(contact);
    },
    actions: [{ form: 'household_visit' }],
    events: [{
      id: 'household-visit',
      start: 0,
      end: 7,
      dueDate: function(event, contact) {
        // Due 30 days after last visit
        return extras.getNextHouseholdVisitDate(contact);
      }
    }],
    resolvedIf: function(contact, report, event, dueDate) {
      return Utils.isFormSubmittedInWindow(
        contact.reports,
        'household_visit',
        Utils.addDate(dueDate, -event.start).getTime(),
        Utils.addDate(dueDate, event.end + 1).getTime()
      );
    }
  }
];
