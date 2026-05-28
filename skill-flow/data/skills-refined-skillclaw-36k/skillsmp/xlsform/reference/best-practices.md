# Best Practices Reference

Guidelines for designing high-quality XLSForms that work well on mobile devices and provide good user experience.

## Form Design

### Question Ordering

**Do:**
- Group related questions together (demographics, then health, then income)
- Ask easier questions first (build rapport)
- Ask sensitive questions later (build trust)
- Use skip logic to shorten perceived length
- Progress from simple to complex

**Example Order:**
```
1. Demographics (name, age, gender)
2. Health history
3. Current conditions
4. Treatment received
5. Sensitive questions (income, beliefs)
```

### Clear Language

**Do:**
- Use simple, active voice
- Ask one thing per question
- Be specific: "How many days?" not "How often?"
- Use local language/idioms for translation
- Define technical terms if necessary

**Don't:**
- Use double negatives: "Have you not had?"
- Ask compound questions: "Do you have fever AND cough?"
- Use vague timeframes: "Recently", "Sometimes"
- Assume technical knowledge

**Good Example:**
```
"In the past 7 days, how many days did you have a fever?"
```

**Poor Example:**
```
"Have you not been without fever symptoms?"
```

### Instruction and Clarity

**Do:**
- Use hints for examples and clarification
- Add notes for section headers
- Provide context for required fields
- Explain unusual questions

**Use hints for:**
```
| type | name | label | hint |
| date | visit_date | Date of visit | Format: YYYY-MM-DD |
| decimal | weight | Weight in kg | Example: 65.5 |
| select_one | source | Where did you hear about us? | (radio, TV, word of mouth, etc.) |
```

### Required vs Optional

**Be clear:**
```
✓ required: yes      (user must answer)
✓ required: no       (user can skip)
✓ (leave empty)      (optional)
```

**Avoid:**
```
✗ "Please answer" in label (too subtle)
✗ Silently requiring without indicating
```

### Question Types

**Select right type:**
- Numeric input → `integer` or `decimal` (not text)
- Yes/No → `select_one` with 2 options (not text)
- Multiple pick → `select_multiple` (not checkboxes)
- Date → `date` type (not text "YYYY-MM-DD")
- Location → `geopoint` (not text "lat,lon")

---

## Mobile Usability

### Screen Size

Forms display on phones (4-6" screens):

**Do:**
- Keep labels short (under 50 chars ideal)
- Use concise hints
- Avoid narrow columns/long text
- Test on actual small devices
- Use text wrapping wisely

**Don't:**
- Assume desktop-sized screens
- Use tiny font sizes
- Create very long labels
- Ignore readability on phone

### Text Input

**Limit text input:**
- For descriptive: use `text` with `multiline`
- For structured: use `select_one` (multiple choice instead)
- Avoid long free-text fields on mobile

### Selection Efficiency

**For yes/no:** Use `horizontal` appearance (side-by-side)
```
| appearance |
| horizontal |
```

**For many options:** Use `search` appearance (searchable dropdown)
```
| appearance |
| search |
```

**For ratings:** Use `likert` appearance
```
| appearance |
| likert |
```

### Date/Time Entry

- Use `date` type (date picker, not text entry)
- Use `time` type (time picker, not text entry)
- Test that pickers are accessible

---

## Offline Functionality

### Forms Work Offline
XLSForms designed for offline data collection:

**Do:**
- Assume no internet during survey
- Don't require server lookups
- Keep forms under 5MB
- Assume weak mobile signal

**Don't:**
- Expect real-time validation from server
- Assume always-online scenarios
- Use complex server expressions
- Assume GPS always available (may take time)

### Data Submission
- Submissions queue automatically
- Sync when internet available
- No data lost if offline
- Timestamp captured when submitted

---

## Performance Optimization

### Form Size

**Ideal:** < 2MB
**Acceptable:** 2-5MB
**Problematic:** > 5MB

**Reduce size:**
- Use `select_one_from_file` for large lists (1000+)
- Remove unused columns from worksheet
- Avoid embedding media (store separately)
- Keep choice lists in separate files

### Calculation Performance

**Do:**
- Use simple formulas for common calculations
- Break complex logic into steps
- Cache intermediate results

**Avoid:**
- Very deeply nested calculations (10+ levels)
- Repeated calculations on same data
- Complex regex patterns in constraints
- Circular calculation dependencies

### Response Time

Test on actual devices:
- Entry → Next question: should be <1 second
- Selection change → Skip logic update: should be <1 second
- Form load: should be <5 seconds

---

## Skip Logic and Branching

### Minimal Branching

**Do:**
- 2-3 logical branches at most
- Clear paths through form
- Obvious why questions appear/disappear

**Don't:**
- Create deeply nested conditions (5+ levels)
- Have circular dependencies
- Make skip logic path unclear to users

### Visible Skip Logic

```
| type | name | label | relevant |
| select_one | has_illness | Have you been ill in past month? | |
| text | illness_desc | Describe illness | ${has_illness} = 'yes' |
```

Users see question appear/disappear. They understand "Because I said yes."

---

## Validation and Constraints

### Clear Constraints

**Do:**
- Always include `constraint_message`
- Make message helpful, not cryptic
- Explain why constraint exists
- Use specific ranges

**Example:**
```
| constraint | constraint_message |
| . >= 0 and . <= 150 | Age must be 0-150 years |
| regex(., '^[0-9]{10}$') | Phone must be 10 digits |
```

### Practical Constraints

- Avoid overly strict validation
- Allow reasonable variation
- Don't validate away legitimate data
- Test constraints with real users

**Good constraint:**
```
. >= 0 and . <= 100
(0-100 range for percentage)
```

**Poor constraint:**
```
. = 50
(Only allow exactly 50?)
```

---

## Multilingual Forms

### Consider Languages

**Do:**
- Test all languages on device
- Use professional translators
- Keep translations concise
- Test RTL (Arabic, Hebrew) separately

**Don't:**
- Use Google Translate without review
- Translate English directly (lose context)
- Ignore cultural differences
- Assume default language is sufficient

### Design for Translation

- Leave extra space for longer translations
- Use short labels (expand in hints)
- Use consistent terminology
- Use notes for culturally-specific guidance

---

## Data Quality

### Input Validation

**Do:**
- Validate format (email, phone)
- Validate range (age 0-150)
- Validate required fields
- Add `constraint_message` for all constraints

**Don't:**
- Over-validate (discourage legitimate data)
- Validate without telling user why
- Require data that may not exist

### Calculated Fields

**Do:**
- Auto-calculate totals/sums
- Add audit fields (timestamp, enumerator)
- Verify calculated results against input

**Don't:**
- Require manual calculation error-prone
- Hide calculations user should verify
- Allow calculated field override

---

## Testing

### Pre-Deployment Checklist

**Structure:**
- [ ] Validate with: `python scripts/validate_xlsform.py form.xlsx`
- [ ] Convert with: `python scripts/convert_to_xform.py form.xlsx`
- [ ] No parse errors reported

**Content:**
- [ ] All questions have clear labels
- [ ] Hints provided where needed
- [ ] Skip logic makes sense
- [ ] Constraints have messages

**Mobile Testing:**
- [ ] Test on actual Android phone
- [ ] Test on actual iOS phone (if applicable)
- [ ] All questions visible and readable
- [ ] Skip logic works correctly
- [ ] Constraints trigger correctly
- [ ] Media capture works (if using)
- [ ] GPS works (if using)

**User Testing:**
- [ ] Non-technical user can complete form
- [ ] Questions understood correctly
- [ ] No confusion about skip logic
- [ ] Time to complete reasonable (< 20 min typical)

**Data Quality:**
- [ ] Required fields enforced
- [ ] Constraints prevent invalid data
- [ ] No obvious data quality issues

### Common Issues to Check

- Typos in question names (affects formulas)
- Choice `list_name` mismatches
- Skip logic references non-existent questions
- Constraints too strict/loose
- Text truncation on small screens
- GPS/media features not working offline

---

## Specific Use Cases

### Health Surveys

**Best Practices:**
- Clinical terms defined in hints
- Anatomical diagrams in notes if needed
- Symptom questions clear and specific
- Privacy considerations for sensitive data
- Consent obtained at start

### Census/Household Surveys

**Best Practices:**
- Clear household definition
- Member roster as repeat group
- Relationships validated
- No duplicate entry detection
- Household numbering/identification

### Market/Agricultural Surveys

**Best Practices:**
- Clear product definitions
- Prices validated against reasonable ranges
- Quantities clearly specified (units)
- Avoid assumptions about practices
- Photos/GPS for verification

---

## Deployment Checklist

**Before Going Live:**
- [ ] Form tested on device
- [ ] Skip logic validated
- [ ] Constraints working
- [ ] Media capture tested (if used)
- [ ] Offline function tested
- [ ] Data quality acceptable
- [ ] Users trained on form
- [ ] Server configured (if applicable)
- [ ] Backup/recovery plan in place
- [ ] Rollback plan documented

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Too long | Users abandon | Limit to 20 minutes, use skip logic |
| Unclear questions | Bad data | Test with actual users, simplify |
| Too many languages | Maintenance burden | Start with 1-2 languages |
| Complex calculations | Confusing to verify | Use visible calculated fields |
| No hints | Confusion | Add hints liberally |
| Strict constraints | User frustration | Test with real data, relax if needed |
| No skip logic | Long perceived form | Use relevant to hide optional paths |
| Untested on device | Doesn't work in field | Always test on actual phone |

---

## See Also

- [examples.md](../examples.md) - Working form examples
- [skip-logic.md](skip-logic.md) - Designing skip logic
- [constraints.md](constraints.md) - Validation best practices
- [question-types.md](question-types.md) - Choosing right question type
