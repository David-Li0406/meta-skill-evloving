# QA Steps Writing Style Guide for AI Agents

This guide defines the exact writing style to use when creating QA steps for Jira tickets. Follow these rules strictly to maintain consistency.

---

## Core Principles

1. **Language**: German with English technical terms
2. **Grammar**: Use infinitive verb forms (no subjects, no personal pronouns)
3. **Tone**: Direct, imperative, minimal
4. **Format**: Structured with bullets, code formatting, and semantic emojis
5. **Length**: Concise - aim for ~250-350 characters per ticket

---

## Document Structure

Every QA step document MUST follow this exact structure:

```markdown
[GitLab MR Link if applicable]

[Optional: Bold context note]

**Steps:**
- [Setup/branch action]
- [Preparation steps]
- [Main action steps]
- [Verification with 🔍]

**Nach QA:**
- [Code Review. 🌟] (if needed)
- Nach `target-branch` mergen. ↪️
- [Nach `production` deployen. 🚀] (if applicable)
- [Production verification] (if applicable)
- Ticket schließen. 📕
```

---

## Handling Missing Information

If required information is missing, use placeholders instead of guessing. Stick to the standard markers and replace them as soon as the data is available.

- MR-Link: `[[MR-LINK]]`
- Branch: `[[BRANCH-NAME]]`
- Environment/URL: `[[ENV-URL]]`

Placeholders must still follow the required formatting (e.g., emojis, backticks). Example:
```
[[MR-LINK]]

**Steps:**
- Auf `[[BRANCH-NAME]]` wechseln.
- Konfigurator öffnen.
- Die Änderungen werden angezeigt. 🔍

**Nach QA:**
- Nach `main` mergen. ↪️
- Ticket schließen. 📕
```

---

## Grammar Rules

### ✅ ALWAYS Use Infinitive Form

```
✅ "Auf `branch-name` wechseln."
❌ "Wechsle auf `branch-name`."
❌ "Man wechselt auf `branch-name`."

✅ "Konfigurator öffnen."
❌ "Öffne den Konfigurator."
❌ "Der Konfigurator wird geöffnet."

✅ "Daten migrieren:"
❌ "Migriere die Daten:"
```

### ✅ Use Passive Voice for Verification

```
✅ "Es wird zur Seite weitergeleitet. 🔍"
✅ "Der Name wird angezeigt. 🔍"
✅ "Die Änderungen sind sichtbar. 🔍"

❌ "Die Seite leitet weiter."
❌ "Du siehst den Namen."
```

### ✅ Use "Man kann..." for Capability Checks

```
✅ "Man kann die Einstellung ändern. 🔍"
✅ "Man kann Aktionen auflisten, ansehen und löschen. 🔍"
```

---

## Technical Terminology

### Use Germanized English Tech Verbs

| ✅ Use This | ❌ Not This |
|-------------|-------------|
| deployen | bereitstellen |
| mergen | zusammenführen |
| committen | festschreiben |
| pushen | hochladen |
| releasen | veröffentlichen |

### Use English Terms Directly

Keep these in English:
- Branch names
- Code/command terms
- File names
- API endpoints
- Database operations

### Backtick Formatting

ALWAYS wrap these in backticks:
- Branch names: `CON-1038-package-boxes`
- Environment names: `main`, `production`, `staging`, `development`
- Commands: `docker-compose restart`
- File names: `config.yml`, `database.rb`
- Code terms: `external_view_url`, `db:migrate:primary`
- Variable names: `user_id`, `partner_name`

---

## Emoji Usage (Semantic Markers)

Emojis are NOT decorative - each has a specific meaning.

| Emoji | Meaning | Usage | Example |
|-------|---------|-------|---------|
| 🔍 | **Verification checkpoint** | After expected results | "Der Name wird angezeigt. 🔍" |
| 📕 | **Close ticket** | ALWAYS with "Ticket schließen" | "Ticket schließen. 📕" |
| ↪️ | **Merge action** | With "mergen" commands | "Nach `main` mergen. ↪️" |
| 🚀 | **Deploy action** | With "deployen" commands | "Nach `production` deployen. 🚀" |
| 🌟 | **Code review** | With "Code Review" | "Code Review. 🌟" |
| 🗣️ | **Communication needed** | For discussion/coordination | "Mit Team absprechen. 🗣️" |
| 🛠️ | **Technical operation** | For system/tool operations | "`db:seed` ausführen. 🛠️" |
| 🕵️‍♂️ | **Production verification** | For prod checks | "Konfigurator in Prod prüfen. 🕵️‍♂️" |
| ✍️ | **Manual editing** | For manual changes | "Werte manuell anpassen. ✍️" |
| 👀 | **Visual inspection** | For UI/design checks | "Mit Design abgleichen. 👀" |

### Emoji Placement Rules

1. Place emoji at END of sentence
2. Include space before emoji
3. Period comes BEFORE emoji
4. Only ONE emoji per sentence

```
✅ "Der Name wird angezeigt. 🔍"
❌ "🔍 Der Name wird angezeigt."
❌ "Der Name wird angezeigt 🔍."
❌ "Der Name wird angezeigt.🔍"
```

---

## Common Sentence Patterns

### Branch Switching

```
Pattern: "Auf `TICKET-###-description` wechseln."

✅ "Auf `CON-1038-package-boxes` wechseln."
✅ "Auf `EX-715-show-users` wechseln."

❌ "Branch `CON-1038-package-boxes` auschecken."
❌ "Wechsel zu `CON-1038-package-boxes`."
```

### Opening Interfaces

```
Pattern: "[Interface] öffnen."

✅ "Konfigurator öffnen."
✅ "Admin-Board öffnen."
✅ "Bewerbungen öffnen."

Link pattern: "In der [Übersicht](URL) ..."

✅ "In der [Übersicht](https://core.example.com/jobpostings) eine Anzeige bearbeiten."
```

### Executing Commands

```
Pattern: "[Command] ausführen:"

✅ "Migrationen ausführen:"
✅ "Daten migrieren:"
✅ "Container neustarten:"

Followed by code block:
```
docker-compose run --rm core rails db:migrate:primary
```
```

### Verification Statements

```
Pattern: "[Result] [modal verb/passive]. 🔍"

✅ "Der Name wird angezeigt. 🔍"
✅ "Die Änderungen sind sichtbar. 🔍"
✅ "Man wird weitergeleitet. 🔍"
✅ "Es ist ein neuer Record zu finden. 🔍"
✅ "Oben stehen Name und Email. 🔍"

❌ "Check dass der Name angezeigt wird."
❌ "Prüfe die Anzeige."
```

### Merging

```
Pattern: "Nach `target` mergen. ↪️"

✅ "Nach `main` mergen. ↪️"
✅ "Nach `production` mergen. ↪️"
✅ "Nach `redesign` mergen. ↪️"

❌ "In `main` mergen. ↪️"
❌ "Merge zu `main`. ↪️"
```

### Deploying

```
Pattern: "Nach `environment` deployen. 🚀"

✅ "Nach `production` deployen. 🚀"
✅ "Nach `staging` deployen. 🚀"

❌ "Auf `production` deployen. 🚀"
❌ "Deploy auf Production. 🚀"
```

### Closing Ticket

```
Pattern: "Ticket schließen. 📕"

ALWAYS this exact phrase, ALWAYS with 📕
ALWAYS as the LAST step

✅ "Ticket schließen. 📕"

❌ "Ticket schliessen. 📕" (Swiss spelling - use ß)
❌ "Task schließen. 📕"
❌ "Ticket abschließen. 📕"
❌ "Close ticket. 📕"
```

---

## Required Sections

### 1. Steps Section

MUST start with:
```
**Steps:**
```

First item is usually branch switching:
```
- Auf `TICKET-###-description` wechseln.
```

### 2. Nach QA Section

MUST be included. MUST start with:
```
**Nach QA:**
```

Standard closing sequence (adjust as needed):
```
- Code Review. 🌟
- Nach `main` mergen. ↪️
- Nach `production` deployen. 🚀
- [Production check if needed]. 🕵️‍♂️
- Ticket schließen. 📕
```

Minimum required:
```
- Nach `target-branch` mergen. ↪️
- Ticket schließen. 📕
```

---

## Code Block Formatting

### Shell Commands

Use plain code blocks (no language specified):

````markdown
```
docker-compose run --rm core rails db:migrate:primary
docker-compose restart
```
````

### Ruby Code

Specify language:

````markdown
```ruby
User.all
Partners::Stepstone::ExportFeedbackProcessingJob.perform_now(...)
```
````

---

## Complete Examples

### Example 1: Simple Feature Test

```markdown
https://gitlab.com/example/project/-/merge_requests/1234

**Steps:**
- Auf `CON-1197-rename-package` wechseln.
- Konfigurator öffnen.
- Mindestens ein Paket konfigurieren.
- Auf der Startseite das Paket umbenennen.
- Der Paket-Name wird in der Zusammenfassung sofort aktualisiert. 🔍

**Nach QA:**
- Nach `redesign` mergen. ↪️
- Ticket schließen. 📕
```

### Example 2: With Database Migration

```markdown
https://gitlab.com/example/project/-/merge_requests/5678

**Steps:**
- Auf `EX-715-show-users` wechseln.
- Migrationen ausführen und Container neustarten:

```
docker-compose run --rm core rails db:migrate:primary
docker-compose restart
```

- Im [Admin-Board](https://core.example.com/admin) anmelden.
- Oben links stehen Name, Email und Rolle. 🔍
- In der Rails-Konsole ist ein neuer Record zu finden:

```ruby
User.all
```

**Nach QA:**
- Nach `main` mergen. ↪️
- Ticket schließen. 📕
```

### Example 3: Production Deployment

```markdown
https://gitlab.com/example/project/-/merge_requests/9012

**Es wurde erstmal nur die Paket-Box umgesetzt. Follow-Ups folgen.**

**Steps:**
- Konfigurator: Auf `CON-1038-package-boxes` wechseln.
- Core: Auf `CON-1066-process-configuration-string` wechseln.
- [Konfiguration](https://konfigurator.example.com/produkte) öffnen.
- Ein paar Produkte hinzufügen.
- Oben auf den `DEV`-Link klicken.
- Paket-Box aufklappen.
- Die Produkte werden korrekt angezeigt. 🔍
- Mit Design abgleichen. 👀

**Nach QA:**
- Code Review. 🌟
- Nach `main` mergen. ↪️
- Nach `production` deployen. 🚀
- Konfigurator in [`production`](https://konfigurator.example.de) prüfen. 🕵️‍♂️
- Ticket schließen. 📕
```

---

## Common Action Verbs

Use these exact forms:

| Action | Infinitive Form |
|--------|-----------------|
| Switch branch | wechseln |
| Open | öffnen |
| Execute | ausführen |
| Merge | mergen |
| Deploy | deployen |
| Check/Verify | prüfen |
| Edit | bearbeiten |
| Click | klicken |
| Save | speichern |
| Create | erstellen |
| Delete | löschen |
| Restart | neustarten |
| Login | anmelden |
| Change | ändern |
| Add | hinzufügen |
| Apply | anwenden |
| Compare | abgleichen |

---

## Checklist for Generated QA Steps

Before finalizing, verify:

- [ ] Document starts with `**Steps:**`
- [ ] All actions use infinitive form (no subjects)
- [ ] All code elements wrapped in backticks
- [ ] Branch names follow pattern: `TICKET-###-description`
- [ ] Verification statements end with 🔍
- [ ] Includes `**Nach QA:**` section
- [ ] Ends with "Ticket schließen. 📕"
- [ ] Merge actions use ↪️ emoji
- [ ] Deploy actions use 🚀 emoji
- [ ] Code Review uses 🌟 emoji
- [ ] All emojis placed at end of sentence with space before
- [ ] No English/German mixing in same sentence (except tech terms)
- [ ] Average length ~250-350 characters

---

## Common Mistakes to Avoid

### ❌ DON'T Use Imperative Forms

```
❌ "Wechsle auf den Branch"
❌ "Öffne den Konfigurator"
❌ "Führe die Migration aus"
```

### ❌ DON'T Use Personal Pronouns

```
❌ "Du solltest den Branch wechseln"
❌ "Wir mergen nach main"
❌ "Man sollte prüfen"
```

### ❌ DON'T Mix Languages Unnecessarily

```
❌ "Open Konfigurator"
❌ "Switch to `branch-name`"
❌ "Close Ticket"
```

### ❌ DON'T Forget Emojis on Standard Actions

```
❌ "Der Name wird angezeigt." (missing 🔍)
❌ "Nach `main` mergen." (missing ↪️)
❌ "Ticket schließen." (missing 📕)
```

### ❌ DON'T Over-Explain

```
❌ "Auf den Branch `CON-1038` wechseln, um die neuen Änderungen zu testen"
✅ "Auf `CON-1038-package-boxes` wechseln."

❌ "Den Konfigurator im Browser öffnen, damit wir die UI sehen können"
✅ "Konfigurator öffnen."
```

---

## Final Notes

- **Be concise**: Every word should add value
- **Be consistent**: Use the same phrase for the same action
- **Be clear**: Technical context assumed, but steps must be unambiguous
- **Be structured**: Follow the template religiously
- **Be semantic**: Emojis are functional, not decorative

This style optimizes for:
- Scannability (bullets + emojis)
- Executability (clear actions)
- Consistency (patterns)
- Brevity (no fluff)
