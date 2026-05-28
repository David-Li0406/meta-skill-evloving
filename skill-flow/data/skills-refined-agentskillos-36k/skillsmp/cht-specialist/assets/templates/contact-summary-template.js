/**
 * CHT Contact Summary Configuration Template
 *
 * This file configures contact profile pages including:
 * - Fields: Basic information displayed on profiles
 * - Cards: Condition cards (pregnancy, treatment, etc.)
 * - Context: Data passed to forms opened from profile
 */

const extras = require('./contact-summary-extras');

module.exports = {
  // Context passed to forms
  context: {
    pregnant: extras.isPregnant(contact, reports),
    high_risk: extras.isHighRisk(contact, reports),
    last_visit_date: extras.getLastVisitDate(contact, reports),
    use_cases: {
      anc: extras.hasSupportFor(lineage, 'anc'),
      pnc: extras.hasSupportFor(lineage, 'pnc'),
      immunization: extras.hasSupportFor(lineage, 'immunization')
    }
  },

  // Profile fields
  fields: [
    // Person fields
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
      label: 'contact.sex',
      value: contact.sex,
      width: 4,
      translate: true
    },
    {
      appliesToType: 'person',
      label: 'contact.phone',
      value: contact.phone,
      width: 6,
      filter: 'phone'
    },
    {
      appliesToType: 'person',
      label: 'contact.parent',
      value: lineage,
      filter: 'lineage'
    },

    // Place fields
    {
      appliesToType: '!person',
      label: 'contact.parent',
      value: lineage,
      filter: 'lineage',
      appliesIf: function() {
        return contact.parent && lineage[0];
      }
    }
  ],

  // Condition cards
  cards: [
    // Active Pregnancy Card
    {
      label: 'contact.profile.pregnancy',
      appliesToType: 'report',
      appliesIf: function(report) {
        return report.form === 'pregnancy' &&
               extras.isActivePregnancy(report);
      },
      fields: [
        {
          label: 'contact.profile.edd',
          value: function(report) {
            return report.fields.edd;
          },
          filter: 'relativeDay',
          width: 6
        },
        {
          label: 'contact.profile.gestational_age',
          value: function(report) {
            return extras.getGestationalAge(report);
          },
          width: 6
        },
        {
          label: 'contact.profile.anc_visits',
          value: 'contact.profile.visits.of',
          translate: true,
          context: {
            count: function(report) {
              return extras.getANCVisitCount(report, reports);
            },
            total: 4
          },
          width: 6
        },
        {
          label: 'contact.profile.risk',
          value: function(report) {
            return extras.isHighRiskPregnancy(report) ? 'high' : 'normal';
          },
          translate: true,
          width: 6,
          icon: function(report) {
            return extras.isHighRiskPregnancy(report) ? 'risk' : '';
          }
        }
      ],
      modifyContext: function(ctx, report) {
        ctx.pregnant = true;
        ctx.edd = report.fields.edd;
        ctx.high_risk = extras.isHighRiskPregnancy(report);
      }
    },

    // Child Health Card
    {
      label: 'contact.profile.child_health',
      appliesToType: 'person',
      appliesIf: function() {
        return extras.isChild(contact);
      },
      fields: [
        {
          label: 'contact.profile.immunization_status',
          value: function() {
            return extras.getImmunizationStatus(contact, reports);
          },
          translate: true,
          width: 6
        },
        {
          label: 'contact.profile.growth_status',
          value: function() {
            return extras.getGrowthStatus(contact, reports);
          },
          translate: true,
          width: 6
        }
      ]
    },

    // Past Pregnancies Card
    {
      label: 'contact.profile.past_pregnancies',
      appliesToType: 'person',
      appliesIf: function() {
        return extras.hasPastPregnancies(contact, reports);
      },
      fields: [
        {
          label: 'contact.profile.total_pregnancies',
          value: function() {
            return extras.getPastPregnancyCount(reports);
          },
          width: 4
        },
        {
          label: 'contact.profile.live_births',
          value: function() {
            return extras.getLiveBirthCount(reports);
          },
          width: 4
        },
        {
          label: 'contact.profile.last_delivery',
          value: function() {
            return extras.getLastDeliveryDate(reports);
          },
          filter: 'relativeDay',
          width: 4
        }
      ]
    }
  ]
};
