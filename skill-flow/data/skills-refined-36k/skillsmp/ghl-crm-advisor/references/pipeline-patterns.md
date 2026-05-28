# Pipeline Design Patterns

## Template Structure

```
[Program Name] Pipeline - [Project Name]

Stages:
1. [Stage Name] - [Definition]
   - Entry criteria: [How contacts enter]
   - Actions: [What happens automatically]
   - Exit criteria: [When they move to next]

Automation Triggers:
- [Stage transition]: [Email/SMS sent, field updated]
- [Time-based]: [Reminders, follow-ups]
- [Condition-based]: [If X happens, do Y]

Custom Fields:
- [field_name] (type: text/number/date) - [Purpose]

Revenue Tracking:
- Average value per opportunity: $X
- Conversion rate targets: X%
```

## Example: CSA Subscription Pipeline (The Harvest)

Stages:
1. Interest Expressed
   - Entry: Website CSA form
   - Actions: Send CSA info pack
   - Exit: Box size selected

2. Box Size Selected
   - Entry: Chose weekly/fortnightly, small/medium/large
   - Actions: Send payment link
   - Exit: Payment processed

3. Payment Set Up
   - Entry: Stripe subscription active
   - Actions: Welcome pack, first box ETA, farm tour invite
   - Exit: First box delivered

4. Active Subscriber
   - Entry: Receiving boxes
   - Actions: Weekly SMS, monthly recipes, quarterly survey
   - Exit: Pauses or cancels

5. Paused
   - Entry: Temporarily suspended
   - Actions: Monthly "ready to resume?" check-in
   - Exit: Resumes or cancels

6. Cancelled
   - Entry: Subscription ended
   - Actions: Exit survey, wait 90 days, win-back campaign

Custom Fields:
- box_size (dropdown: small/medium/large)
- frequency (dropdown: weekly/fortnightly)
- pickup_location (dropdown)
- dietary_preferences (text)
- subscription_start_date (date)
- lifetime_value (number)

Revenue:
- Small: $35/week × 52 = $1,820/year
- Medium: $50/week × 52 = $2,600/year
- Large: $70/week × 52 = $3,640/year
- Target: 50 subscribers = ~$100K/year

## Example: Residency Pipeline (ACT Farm)

Stages:
1. Inquiry Received
2. Application Under Review
3. Approved - Awaiting Payment
4. Payment Received
5. Pre-Arrival
6. In Residence
7. Departed - Alumni

Custom Fields:
- residency_type (R&D/Creative/Wellbeing/Research)
- arrival_date, departure_date
- nights_booked, total_value
- dietary_requirements
- research_output_type

Revenue:
- R&D: $300-500/night
- Creative: $400/night
- Wellbeing: $350/night
