# Frameworks and Central Bodies

## BlueLight Commercial (BLC)

Established 2020 by Home Office and NPCC. The national commercial body for policing, driving efficiency and standardization across all 43 forces.

### How Forces Buy

1. **Framework call-off** (most common for repeatable services)
   - Direct award (if framework rules allow)
   - Further competition / mini-competition among framework suppliers

2. **Open market tender** (FTS tender notice) for larger/complex requirements

3. **Below-threshold competition** (increasingly visible on FTS post-2025)

4. **Dynamic Purchasing System (DPS)**

### Key Frameworks

| Framework | Holder | Use Case |
|-----------|--------|----------|
| Contingent Labour | Adecco | Temporary staffing, admin, some investigators. Master Vendor model — supply via sub-contractor to Adecco |
| Covert Management (BLC0224) | Various | Covert operations software and support |
| Workforce Solutions RM6288 (CCS) | Various | Managed contingent labour across public sector |

### Framework Characteristics

- **Duration:** Typically 4 years (can extend in exceptional cases)
- **Structure:** Multi-supplier, routes via Direct Award and Further Competition
- **Renewal signal:** Watch for Prior Information Notices 12-18 months before expiry

### Portals

**BlueLight eTendering (EU Supply)**
- Used by most UK Police forces and Fire & Rescue services
- Operational tendering portal (not the official notice repository)
- Monitor "New Tender Opportunities" and register for account alerts
- No official open API

**BlueLight Commercial e-procurement hub (InTend)**
- Register on InTend hub for alerts
- View latest opportunities

---

## Crown Commercial Service (CCS)

Forces frequently use CCS for broader categories outside police-specific needs.

### Relevant Frameworks

| Framework | Reference | Use Case |
|-----------|-----------|----------|
| Non-Clinical Staffing | RM6277 | Professional services, interim management |
| Non-Clinical Temporary Staff | RM6160 | Fixed-term staffing |
| Workforce Solutions | RM6288 | Managed contingent labour |

### Detection Strategy

Mini-competitions under CCS frameworks are often distributed only to on-framework suppliers. Monitor CCS contract award notices where buyer is a police force to identify when forces choose CCS route over BLC route.

---

## Regional Procurement Hubs

Forces aggregate into regional alliances functioning as single procurement units. A tender from a "Lead Force" represents access to multiple constabularies.

### Major Hubs

| Hub | Member Forces | Behavior |
|-----|---------------|----------|
| **7 Forces Commercial (7FC)** | Bedfordshire, Cambridgeshire, Essex, Hertfordshire, Kent, Norfolk, Suffolk | Highly centralized. Single Director of Commercial Services. Tenders issued once for whole bloc. Often led by Essex or Kent Police |
| **South West Police Procurement Dept (SWPPD)** | Devon & Cornwall, Dorset, Gloucestershire, Wiltshire, Avon & Somerset | Collaborative but retains local autonomy. Often leads national fleet/aviation tenders |
| **South East (Collaborative)** | Surrey, Sussex, Thames Valley, Hampshire | Bilateral partnerships: Surrey & Sussex share joint commercial function; Thames Valley & Hampshire often procure jointly |
| **North West (NWROCU)** | Greater Manchester, Merseyside, Lancashire, Cumbria, Cheshire, North Wales | Less centralized but collaborates heavily on Serious & Organised Crime (ROCU) tenders |
| **Metropolitan Police (MPS)** | Met Police | Independent due to scale (£262m agency spend). Own Commercial Services directorate. Often establishes own frameworks |

### Detection Logic

Rather than maintaining a manual collaboration matrix, infer from notices:
- Multiple "participant" authorities in tender documents
- "Available to all UK Police Forces" language (common in BLC frameworks)
- Central body as contracting authority (BlueLight Commercial)
- Lead Force pattern (one force as contracting authority for regional group)

---

## Police and Crime Commissioners (PCCs)

PCCs own the budget and legal entity of contracts. Chief Constable delivers operational service.

### Schemes of Delegation

Each PCC publishes financial thresholds:
- **<£25,000:** Budget holders (e.g., Detective Superintendent) using "3 quotes"
- **£25,000-£100,000:** Head of Procurement sign-off, may not require open tender if framework available
- **>£500,000:** Formal decision note signed by PCC or Chief Executive

### Decision Logs as Signals

PCC decisions often published on PCC websites *weeks* before tender notice appears on FTS. Monitor these logs for "pre-notification" signals that major procurement has been authorized.

### Governance Change Warning

November 2025: Government announced plans to abolish PCCs by 2028, shifting responsibilities to mayors/council leaders. Treat PCC as *one possible buyer pattern*, not permanent institutional anchor.

Build buyer registry by identifiers (PPON/Companies House) with a governance layer that can adapt to structural change.

---

## Buyer Name Patterns

Expect contracting authority names like:
- "[Force] Police" / "[Force] Constabulary"
- "Chief Constable of [Force]"
- "Police and Crime Commissioner for [Area]"
- "Office of the Police and Crime Commissioner for [Area]" (OPCC)
- "Mayor's Office for Policing and Crime" (MOPAC — London)
- National/sector bodies: BlueLight Commercial, College of Policing, NCA

**System requirement:** Build canonical `buyer_entity` table mapping all name variants to stable identifiers. Use FTS organisation identifiers (Public Procurement Organisation Number) when present.

---

## Large vs Small Force Behavior

**Large forces:**
- More likely to run bespoke multi-lot tenders
- More frequent market engagement notices
- Higher use of long-term managed service contracts

**Smaller forces:**
- More frequent use of frameworks/call-offs (faster procurement overhead)
- Higher probability of joint procurement via lead force or central body
