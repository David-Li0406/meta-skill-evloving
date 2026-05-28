# Tag Taxonomy Architecture

## Hierarchical Structure

```
[Project/Campaign] Tag Architecture

Base Tags:
- [project-name] (all contacts)
- [sub-project] (specific program)

Engagement Level:
- engagement:lead
- engagement:prospect
- engagement:customer
- engagement:alumni

Category Tags:
- category:[type]
- interest:[area]
- program:[name]

Behavioral Tags:
- action:[behavior]
- attended:[event]
- completed:[milestone]

Priority Tags:
- priority:high (VIPs)
- priority:urgent (needs immediate attention)
```

## The Harvest Tags

Base: `the-harvest`
Sub-projects: `csa`, `events`, `therapeutic`, `tenant`

Categories:
- `interest:volunteering`
- `interest:csa`
- `interest:events`
- `interest:therapeutic`
- `category:tenant`
- `category:vendor`

Behavioral:
- `attended_orientation`
- `attended_event`
- `completed_training`
- `active_volunteer`

## ACT Farm Tags

Base: `act-farm`
Sub-projects: `residency`, `workshop`, `junes-patch`

Categories:
- `residency:rd` (R&D)
- `residency:creative`
- `residency:wellbeing`
- `workshop:attended`
- `junes-patch:patient`

Behavioral:
- `completed_residency`
- `repeat_visitor`
- `research_published`

## Empathy Ledger Tags

Base: `empathy-ledger`
Sub-projects: `storyteller`, `organization`, `research`

Categories:
- `role:storyteller`
- `role:organization`
- `role:researcher`
- `consent:full`
- `consent:limited`
- `cultural:elder`

## JusticeHub Tags

Base: `justicehub`
Sub-projects: `family`, `provider`, `contained`, `story`

Categories:
- `contained:nominee`
- `contained:leader`
- `contained:advocate`
- `category:service-provider`
- `category:family-support`

## Cross-Project Example

Contact "Mary Smith" (Elder, multi-project):
```
empathy-ledger
act-farm
the-harvest
role:elder
engagement:active
priority:high
cultural:kabi-kabi
consent:full
```
