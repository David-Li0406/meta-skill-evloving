# Solano County 2008 General Plan Reference

Quick reference for navigating and using the General Plan document collection. The General Plan is the county's "constitution" for land use and development policy.

## What is the General Plan?

The General Plan is a long-range policy document required by California law (Government Code §65300+) that guides:
- Land use and development decisions
- Infrastructure and public facility planning
- Environmental protection
- Housing policy
- Economic development

**Key Principle**: The General Plan sets policy goals. The County Code (especially Chapter 28 - Zoning) implements those goals through specific regulations.

## Document Structure

### Main Chapters (455 chunks total)

| Chapter | Title | Chunks | Key Topics |
|---------|-------|--------|------------|
| 0 | Title Page & TOC | 9 | Navigation |
| 1 | Introduction | 12 | Vision, planning process |
| 2 | Land Use | 31 | Land use designations, community separators |
| 3 | Agriculture | 16 | Ag preservation, farmland mitigation, agritourism |
| 4 | Resources | 33 | Water, habitat, open space, cultural resources |
| 5 | Public Health & Safety | 46 | Flood, fire, seismic, noise, hazmat |
| 6 | Economic Development | 10 | Job growth, opportunity sites, Travis AFB |
| 7 | Transportation | 13 | Roads, transit, airports, goods movement |
| 8 | Public Facilities | 17 | Water, sewer, schools, parks |
| 9 | Housing Element | 233 | Housing needs, sites, programs (updated 2023-2031) |
| 10 | Parks & Recreation | 22 | Park standards, trails, recreation |
| 11 | Tri-City & County Plan | 1 | Fairfield-Suisun-Vacaville coordination |
| 12 | Suisun Marsh LPP | 12 | Marsh protection policies |

### Supporting Documents

| Type | Count | Content |
|------|-------|---------|
| EIR | 638 chunks | Environmental Impact Report (DEIR, Volumes II-III) |
| Appendices | 42 chunks | Acronyms, Guiding Principles, MMRP, Ordinance |
| Resolutions | 20 chunks | Amendments (Housing Element 2024, Wind Turbine 2023, Suisun Marsh 2018) |
| Diagram | 1 chunk | Land Use Diagram reference |

### Content Types

| Type | Count | Description |
|------|-------|-------------|
| Narrative | 715 | Background text, descriptions, analysis |
| Table | 340 | Data tables, matrices, statistics |
| Policy | 282 | Goals, policies, implementation programs |
| TOC | 8 | Table of contents entries |

## How to Use General Plan Tools

### Finding Relevant Policies

**Best tool**: `search_general_plan_policies`
```
Use when: User asks about county policy goals, allowed uses, or "what does the county want"
Example: search_general_plan_policies("agricultural tourism")
```

**Returns**: Only policy/goal chunks, ranked by relevance

### General Search

**Best tool**: `search_general_plan`
```
Use when: Broader research, background info, or specific terms
Filters available:
- chapter: "3" (Agriculture)
- document_type: "chapter", "eir", "appendix", "resolution"
- chunk_type: "narrative", "table", "policy"
```

### Getting Full Context

**Tool**: `get_general_plan_chunk`
```
Use when: Search result preview isn't enough
Input: chunk_id from search results (e.g., "chapter-3---agriculture--0005")
```

### Reading Entire Chapters

**Tool**: `get_general_plan_chapter`
```
Use when: Need comprehensive understanding of a topic
Example: get_general_plan_chapter("6") for Economic Development
```

## Key Chapters by Use Case

### Property/Zoning Questions → Chapter 2 (Land Use)
- Land use designations and what they mean
- Community separators between cities
- Urban/rural boundary policies

### Agricultural Questions → Chapter 3 (Agriculture)
- Farmland preservation programs
- Right-to-farm ordinance
- Agricultural Reserve Overlay
- Agritourism policies
- Williamson Act references

### Development Constraints → Chapter 5 (Public Health & Safety)
- Flood hazard policies
- Fire hazard policies
- Seismic safety
- Noise standards
- Hazardous materials

### Housing Projects → Chapter 9 (Housing Element)
- RHNA requirements
- Housing sites inventory
- ADU policies
- Affordability requirements
- **Note**: This is the largest chapter (233 chunks) and was updated in 2023-2031 cycle

### Economic Development → Chapter 6
- Opportunity sites (Collinsville, Lambie Road, North Vacaville)
- Travis AFB protection
- Interior valleys tourism potential
- Workforce development

## Policy Naming Convention

General Plan policies follow this pattern:
- **Goals**: `XX.G-#` (e.g., AG.G-1 = Agriculture Goal 1)
- **Policies**: `XX.P-#` (e.g., AG.P-5 = Agriculture Policy 5)
- **Implementation**: `XX.I-#` (e.g., AG.I-3 = Agriculture Implementation Program 3)

**Chapter Prefixes**:
| Prefix | Chapter |
|--------|---------|
| LU | Land Use |
| AG | Agriculture |
| RS | Resources |
| HS | Health & Safety |
| ED | Economic Development |
| TC | Transportation/Circulation |
| PF | Public Facilities |
| HS | Housing (also uses H-) |
| PR | Parks & Recreation |

## Connecting General Plan to County Code

| General Plan Chapter | Primary County Code Chapter |
|---------------------|---------------------------|
| Land Use (Ch 2) | Chapter 28 - Zoning |
| Agriculture (Ch 3) | Chapter 28, Article II (28.21.x, 28.22.x, 28.23.x) |
| Public Health & Safety (Ch 5) | Chapter 31 - Grading; Chapter 28 hazard overlays |
| Transportation (Ch 7) | Chapter 24 - Roads |
| Public Facilities (Ch 8) | Various utility chapters |
| Housing (Ch 9) | Chapter 28 residential districts, ADU provisions |
| Parks (Ch 10) | Chapter 19 - Parks & Recreation |

## Common Queries and Which Tool to Use

| Question Type | Tool | Example |
|--------------|------|---------|
| "What's the policy on X?" | `search_general_plan_policies` | "agricultural preservation" |
| "What did the EIR say about X?" | `search_general_plan` with `document_type: "eir"` | "traffic impacts" |
| "What are the goals for X?" | `search_general_plan_policies` + `get_general_plan_chunk` | "economic development goals" |
| "Show me everything about X chapter" | `get_general_plan_chapter` | Chapter 6 |
| "What recent changes were made?" | `list_general_plan_documents` then search resolutions | Housing Element update |

## Important Context

### Orderly Growth Initiative
The General Plan operates alongside the voter-approved Orderly Growth Initiative (1994, renewed 2008), which requires voter approval to redesignate agricultural or open space land for urban uses.

### Housing Element Cycle
The Housing Element (Chapter 9) is updated on an 8-year cycle per state law. The current certified element covers 2023-2031 and includes specific housing sites and programs to meet RHNA requirements.

### Suisun Marsh Protection
Chapter 12 implements the Suisun Marsh Local Protection Program per state law. These policies have additional weight due to Suisun Marsh Preservation Act requirements.

### EIR Mitigation
The EIR documents (638 chunks) contain mitigation measures that may apply to specific projects. When a project triggers CEQA review, these measures become enforceable conditions.

## Contacts

**General Plan Questions**:
- Solano County Planning Services: (707) 784-6765
- Address: 675 Texas Street, Suite 5500, Fairfield, CA 94533

**Housing Element Questions**:
- Housing Program staff via Planning Services

**Suisun Marsh Questions**:
- May also involve BCDC (Bay Conservation & Development Commission)
