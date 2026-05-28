/**
 * CHT Targets Configuration Template
 *
 * This file defines targets (KPIs) shown on the Analytics tab.
 * Targets can be counts or percentages.
 */

const extras = require('./targets-extras');

module.exports = [
  // Example: Count target - This month
  {
    id: 'pregnancies-registered',
    type: 'count',
    icon: 'pregnancy',
    goal: 10,
    translation_key: 'targets.pregnancies.title',
    subtitle_translation_key: 'targets.this_month.subtitle',
    appliesTo: 'reports',
    appliesToType: ['pregnancy'],
    date: 'reported'
  },

  // Example: Count target - All time, no goal
  {
    id: 'total-patients',
    type: 'count',
    icon: 'person',
    goal: -1,
    translation_key: 'targets.total_patients.title',
    subtitle_translation_key: 'targets.all_time.subtitle',
    appliesTo: 'contacts',
    appliesToType: ['person'],
    date: 'now'
  },

  // Example: Percentage target
  {
    id: 'deliveries-with-anc',
    type: 'percent',
    icon: 'anc',
    goal: 100,
    translation_key: 'targets.deliveries_with_anc.title',
    subtitle_translation_key: 'targets.all_time.subtitle',
    appliesTo: 'reports',
    appliesToType: ['delivery'],
    appliesIf: function(contact, report) {
      return report.fields.delivery_outcome === 'live_birth';
    },
    passesIf: function(contact, report) {
      // Count ANC visits before delivery
      const ancVisits = contact.reports.filter(r =>
        r.form === 'anc_visit' &&
        r.reported_date < report.reported_date
      );
      return ancVisits.length >= 4;
    },
    date: 'now'
  },

  // Example: Percentage with role-based visibility
  {
    id: 'home-visits-completed',
    type: 'percent',
    icon: 'home-visit',
    goal: 80,
    translation_key: 'targets.home_visits.title',
    subtitle_translation_key: 'targets.this_month.subtitle',
    context: 'user.role === "chw"',
    appliesTo: 'contacts',
    appliesToType: ['clinic'],
    date: 'reported',
    passesIf: function(contact) {
      return contact.reports.some(r => r.form === 'household_visit');
    }
  },

  // Example: Group-based target
  {
    id: 'families-with-multiple-visits',
    type: 'percent',
    icon: 'family',
    goal: 100,
    translation_key: 'targets.family_visits.title',
    appliesTo: 'contacts',
    appliesToType: ['person'],
    date: 'reported',
    idType: function(contact) {
      // Create IDs for each visit date per family
      const familyId = contact.contact.parent._id;
      const visitDates = contact.reports
        .filter(r => r.form === 'home_visit')
        .map(r => new Date(r.reported_date).toISOString().split('T')[0]);
      return visitDates.map(date => `${familyId}~${date}`);
    },
    groupBy: function(contact) {
      return contact.contact.parent._id;
    },
    passesIfGroupCount: { gte: 2 }
  }
];
