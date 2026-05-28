# Contacts Reference

## Command: contacts-search

Search contacts by name, email, phone, or company.

```bash
contacts-search "Marie"          # Quick search
contacts-search -v "Brandon"     # Verbose (all details incl. birthday)
contacts-search -a               # List all contacts
contacts-search -l 5 "Smith"     # Limit to 5 results
contacts-search -j               # JSON output
```

Searches: First name, last name, email, phone, company (case-insensitive)

## Examples

**"What's Brandon's phone number?"**
```bash
contacts-search "Brandon"
```

**"When is Eileen's birthday?"**
```bash
contacts-search -v "Eileen"
```
Look for "Birthday:" in output.

**"Find someone at Best Buy"**
```bash
contacts-search "Best Buy"
```

## Limitations

- ~700 contacts can be slow to enumerate
- Use specific searches rather than `-a` when possible
