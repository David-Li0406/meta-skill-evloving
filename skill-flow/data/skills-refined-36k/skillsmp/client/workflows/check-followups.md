# Check Client Follow-ups

## Steps

1. **Find clients with next_action set**
   
   ```bash
   grep -l "next_action:" Clients/*.md
   ```

2. **Check each client's follow-up date**
   
   For each file, read the frontmatter:
   - `next_action` - the date
   - `next_action_note` - what needs to be done
   - `name` - client name
   - `company` - their company

3. **Filter for today or overdue**
   
   Compare `next_action` date to today's date.
   Show clients where next_action <= today.

4. **Present the list**
   
   For each client needing attention:
   - Name (Company)
   - What action is needed
   - How overdue (if applicable)

5. **Offer next steps**
   
   Ask: "Want me to draft a follow-up email to any of them?"

## Example Output

```
Clients needing follow-up:

1. Sarah Chen (TechStartup Inc)
   Action: Follow up on proposal
   Due: Jan 8 (today)

2. Marcus Johnson (DesignCo)
   Action: Send intro email
   Due: Jan 9 (tomorrow)

Want me to draft a follow-up email to any of them?
```
