# CPV Codes and Keywords for Police Procurement

## Primary CPV Codes

Common Procurement Vocabulary (CPV) codes used in police investigation and staffing procurements.

### Investigation Services

| CPV Code | Description | Relevance |
|----------|-------------|-----------|
| **79720000** | Investigation services | Core investigator teams |
| **79620000** | Supply services of personnel including temporary staff | Contingent labour, managed teams |
| **79600000** | Recruitment services | Permanent and temporary recruitment |
| **79411000** | General management consultancy services | Advisory, process improvement |
| **75241100** | Police services | Policing support services |

### Related Services

| CPV Code | Description | Relevance |
|----------|-------------|-----------|
| 79700000 | Investigation and security services | Broader security category |
| 79710000 | Security services | Custody, detention support |
| 72000000 | IT services | Digital forensics, case management |
| 80500000 | Training services | Investigator training |
| 79100000 | Legal services | Disclosure, prosecution support |

---

## Two-Layer Classification

### Layer A: Rule-Based Filters

Apply these filters to any procurement feed:

**Buyer Name Contains:**
```
police, constabulary, PCC, OPCC, BlueLight, MOPAC, 
NCA, British Transport Police, Commissioner
```

**CPV in Staffing/Resourcing Neighborhood:**
- Start with codes above
- Expand empirically from historical awards

**Keywords:**
```
investigation, investigator, casework, disclosure, review,
intel, detective, economic crime, financial investigation,
digital forensics
```

### Layer B: Learned Expansion

From historical awards ingested:
1. Extract top CPVs used in police "investigation support" procurements
2. Add to watchlist automatically
3. Avoids guessing CPVs incorrectly
4. Adapts to policing's varied language

---

## Keyword Taxonomies

### Role-Based Keywords

```
PIP2, PIP3, Investigator, Statement Taker, Review Officer,
Holmes Indexer, HOLMES, Analyst, Intelligence Officer,
Disclosure Officer, Case File Builder, Exhibits Officer,
Crime Scene Manager, SOCO, CSI, Detective, DC, DS, DI
```

### Operation-Based Keywords

```
Major Crime, Cold Case, Rape and Serious Sexual Offences, RASSO,
Safeguarding, Historic Abuse, Operation Stovewood, IICSA,
County Lines, Economic Crime, Fraud, Financial Investigation,
Cyber Crime, Digital Forensics, Serious Organised Crime, ROCU
```

### Administrative Keywords

```
Managed Service, Contingent Labour, Resourcing Partner,
Augmentation, Outsourcing, Staff Augmentation, Team Deployment,
Resource Pool, Flexible Resource, Investigation Team,
Backlog Reduction, Case Review
```

### Framework Keywords

```
BlueLight Commercial, Contingent Labour Framework,
Adecco, Master Vendor, Call-off, Mini-competition,
Further Competition, Direct Award, Framework Agreement,
Crown Commercial Service, CCS, RM6277, RM6160, RM6288
```

---

## Light Touch Regime

Investigation Services (CPV 79720000) typically classified under Light Touch Regime (Social and Other Specific Services).

**Threshold: £663,540**

**Strategic Advantage:** Forces can spend up to £663,540 without full rigid timescales of standard procedure. They have more flexibility to negotiate and can use shorter advertising periods.

This favors agile suppliers who can demonstrate capability practically rather than through lengthy tender essays.

---

## Search Query Examples

### Contracts Finder Search Body

```json
{
  "searchCriteria": {
    "types": ["Contract", "Pipeline"],
    "statuses": ["Open"],
    "keyword": "investigation OR investigator OR disclosure OR casework",
    "cpvCodes": ["79720000", "79620000", "79600000", "79411000"]
  },
  "size": 100
}
```

### FTS OCDS Filter

After ingestion, filter where:
```python
buyer_keywords = ["police", "constabulary", "pcc", "opcc", 
                  "bluelight", "mopac", "nca"]
target_cpvs = ["79720000", "79620000", "79411000", "75241100"]

def is_relevant(release):
    buyer_name = release.buyer.name.lower()
    cpv_codes = release.tender.items[*].classification.id
    
    buyer_match = any(kw in buyer_name for kw in buyer_keywords)
    cpv_match = any(cpv in cpv_codes for cpv in target_cpvs)
    
    return buyer_match and cpv_match
```

---

## Alert Priority by Keyword

| Keyword Pattern | Priority | Rationale |
|-----------------|----------|-----------|
| "investigation team" + police buyer | Very High | Direct match |
| "managed service" + CPV 79720000 | Very High | Core service |
| "disclosure" + police | High | Often outsourced |
| "backlog" + investigation | High | Urgent need signal |
| "contingent labour" + BlueLight | High | Framework activity |
| "RASSO" or "safeguarding" | High | Specialist need |
| "digital forensics" | Medium-High | Growing area |
| "temporary staff" + police | Medium | Broad category |
| "professional services" + police | Low | Too generic |

---

## Competitor Name Patterns

Track awards to these known competitors:

```
Adecco, Reed Talent Solutions, Reed Specialist Recruitment,
G4S, Serco, Mitie, Sodexo, Capita, ISS, Kroll, 
Hays, Brook Street, Manpower, Randstad, SThree,
Peel Recruitment & Training Solutions, Peel Solutions
```

Query: `SELECT * FROM awards WHERE supplier_name LIKE '%{competitor}%'`
