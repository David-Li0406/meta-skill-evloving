# Procurement Thresholds and Rules

## Current Thresholds (1 Jan 2024 — 31 Dec 2025)

UK procurement thresholds for international obligations:

| Category | Threshold |
|----------|-----------|
| **Works** | £5,372,609 |
| **Supplies & Services (Central Government)** | £139,688 |
| **Supplies & Services (Sub-Central / Police Forces)** | £214,904 |
| **Defence & Security** | £553,550 |
| **Utilities** | £429,809 |
| **Light Touch Services** | £663,540 |
| **Concession Contracts** | £5,372,609 |

### Key Threshold for Police

**£214,904** — Above this, police force service contracts require full regulatory compliance and FTS publication.

**£663,540** — Light Touch Regime threshold. Investigation Services (CPV 79720000) typically classified here. More flexibility on process and timescales.

---

## Contracts Finder Publication Requirements

| Authority Type | Threshold |
|----------------|-----------|
| Central Government | >£12,000 |
| Sub-Central (Police) | >£25,000 |

Above these amounts, notices should be published on Contracts Finder (pre-Feb 2025) or Find a Tender (post-Feb 2025).

---

## Procurement Act 2023

Fully effective from **24 February 2025**. Replaces Public Contracts Regulations (PCR) 2015.

### Key Changes

**1. Competitive Flexible Procedure**

Abolishes rigid "Competitive Dialogue" and "Restricted" procedures. Introduces single "Competitive Flexible Procedure" allowing forces to design bespoke procurement processes.

*Impact:* Forces can design their own process — e.g., "Submit a CV and do an interview" — as long as it's advertised transparently. Favors agile suppliers who can demonstrate capability practically.

**2. Two Competitive Tendering Procedures**

- **Open Procedure** — Any supplier can submit a tender
- **Competitive Flexible Procedure** — Authority designs the process

Both commenced via publication of a **tender notice**.

**3. Enhanced Transparency**

FTS becomes single source of truth. Notices must be published for all steps including:
- Preliminary Market Engagement (PME)
- Contract modifications
- All award decisions

**4. Direct Award Rules**

Permitted only when conditions in sections 41-43 apply (and schedule 5 justifications where relevant). Transparency notice required.

Common justifications:
- Urgency
- Protecting Life
- Only one supplier capable

*Police often utilize these for operational necessities.*

---

## Below-Threshold Flexibility

Even below threshold:
- Transparency expectations remain
- Post-Feb 2025: Publication on FTS for new procurements
- Faster, more relationship-driven — non-notice signals carry more weight

### Internal Delegation Limits

Typical force standing orders:

| Value | Authority | Process |
|-------|-----------|---------|
| **<£25,000** | Budget holder (e.g., Det Supt) | 3 quotes (RFQ) |
| **£25,000-£100,000** | Head of Procurement | May not require open tender if framework available |
| **>£500,000** | PCC or Chief Executive | Formal decision note |

---

## Notice Type Sequences (Procurement Act)

```
UK1 Pipeline Notice (optional, >£2m)
        ↓
UK2 Preliminary Market Engagement (optional)
        ↓
UK3 Planned Procurement Notice (optional)
        ↓
UK4 Tender Notice (required for competitive)
        ↓
UK6 Contract Award Notice (required)
        ↓
UK12 Procurement Termination Notice (if cancelled)
```

UK1, UK2, UK3 can occur in any order. UK4 required before any award.

---

## Light Touch Regime (LTR)

**Threshold: £663,540**

Services classified under LTR have:
- Shorter advertising periods permitted
- More flexibility in process design
- Less rigid timescales

Investigation Services (CPV 79720000) typically qualify.

*Strategic Advantage:* Allows forces to negotiate more freely and move faster for specialist services.

---

## Framework Rules

**Maximum Duration:** 4 years (except exceptional cases)

**Call-off Routes:**
- Direct Award (if framework rules allow)
- Further Competition (mini-competition among framework suppliers)

**Framework holder as prime:** Master Vendor models (like Adecco's Contingent Labour) mean suppliers must often become sub-contractors rather than contracting directly with forces.

---

## Contract Intelligence from Awards

Award notices contain key competitive intelligence:

| OCDS Field | Intelligence Use |
|------------|------------------|
| `awards.status` | Filter for "active" |
| `awards.suppliers.name` | Competitor identification |
| `awards.value.amount` | Contract value for share-of-wallet analysis |
| `awards.contractPeriod.startDate` | When service began |
| `awards.contractPeriod.endDate` | **Critical:** Re-procurement window |

### Re-procurement Forecasting

**Rule:** Alert 9-12 months before contract end date (earlier for complex multi-lot services)

```python
reprocurement_alert_date = contract_end_date - timedelta(days=270)
```

---

## FOI as Gap-Filler

Freedom of Information Act 2000 requires forces to disclose spend data.

**Response time:** 20 working days

**Useful for:**
- Contract end dates not in public notices
- Extension decisions
- Incumbent supplier performance
- Spend-to-date under frameworks
- "Who else bid?" (often refused but sometimes partially disclosed)

**Tactical Request Template:**
```
Please provide a list of all current contracts for temporary agency 
staff and investigation services, including:
- Supplier name
- Start date
- End date
- Total contract value
```

Platforms like WhatDoTheyKnow can automate requests to all 43 forces. Responses often reveal "off-framework" spend not visible on Contracts Finder.
