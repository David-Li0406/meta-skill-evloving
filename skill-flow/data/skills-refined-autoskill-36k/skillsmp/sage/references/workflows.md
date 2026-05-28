# Cross-Tool Integration Patterns

This reference covers common workflows that combine multiple SAGE tools to answer complex questions.

---

## Pattern 1: Policy-to-Implementation Analysis

Connect high-level goals to concrete regulations and resources:

```
General Plan Policy → County Code Implementation → Budget/Staffing
```

**Example**: "How does the county implement agricultural preservation?"
1. `search_general_plan_policies` → "farmland mitigation" in Chapter 3
2. `get_county_code_sections` → Chapter 28 agricultural zoning (28.21.x)
3. `get_department_budget` → Agricultural Commissioner funding
4. Explain: Policy goal, implementing regulations, resources allocated

---

## Pattern 2: Development Feasibility

Comprehensive property analysis for development questions:

```
Location → Jurisdiction → Zoning → Hazards → Code Requirements → Contacts
```

**Example**: "Can I build an agritourism facility at [address]?"
1. `geocode_address` → Get APN and coordinates
2. `get_zoning` → Confirm A-40/A-SV zone, check if agritourism is AP/MUP/UP
3. `get_flood_zone` + `get_fire_hazard_zone` → Check hazard constraints
4. `search_general_plan` → Chapter 3 Agriculture policies on agritourism
5. `get_county_code_sections` → 28.75 (agritourism regulations)
6. Provide: Permit path, requirements, contacts

---

## Pattern 3: Budget-Staffing-Mission Alignment

Understand how departments are resourced:

```
Department → Budget → Staffing → Divisions → Positions
```

**Example**: "What resources does Resource Management have for planning?"
1. `get_department_budget` → "Resource Management"
2. `get_department` → code "2910" with divisions
3. `search_positions` → "planner" in Resource Management
4. Explain: Budget, FTEs, division structure, key positions

---

## Pattern 4: Subdivision/Land Division Questions

Navigate complex subdivision requirements:

1. `search_county_code` → "subdivision exemption" or "lot line adjustment"
2. `get_county_code_sections` → Chapter 26 relevant sections
3. `search_general_plan` → Land Use chapter on subdivision policies
4. `get_parcel_details` → Current parcel configuration
5. Explain: Exemption eligibility, process, fees, contacts

---

## Pattern 5: Create Derived Boundary Layers

Generate new GIS layers from parcel data:

```
Inspect Fields → Dissolve → GeoJSON URL → Add to AGOL
```

**Example**: "Create a school district boundaries layer"
1. `inspect_layer` → dataset: "parcels" to see available fields
2. `dissolve_layer` → dataset: "parcels", dissolve_field: "f_school", output_name: "school_districts"
3. Result: GeoJSON URL with 9 school district polygons
4. User can add to ArcGIS Online: Content → Add Item → URL → paste GeoJSON URL

**Example**: "Create fire district boundaries"
1. `dissolve_layer` → dataset: "parcels", dissolve_field: "desc_fire", output_name: "fire_districts"
2. Returns URL to simplified fire district polygons

---

## Pattern 6: Research Board Decisions

Track what the Board of Supervisors decided on a topic:

```
Search Minutes → Review Decisions → Link to Policy/Budget
```

**Example**: "What has the Board decided about housing?"
1. `search_meeting_minutes` → query: "housing", committee: "bos", document_type: "minutes"
2. `get_meeting_chunk` → Full text of relevant agenda items
3. `search_general_plan` → Housing Element policies
4. Explain: Board actions, policy context, implementation status

**Example**: "Track a specific resolution"
1. `search_meeting_minutes` → query: "resolution 2025-253"
2. `get_meeting` → Full meeting content for context
3. Link to related budget or code changes if applicable

---

## Quick Reference: Tool Combinations

| Question Type | Tools to Combine |
|---------------|------------------|
| "Can I build X at [address]?" | geocode → get_zoning → get_flood_zone → get_fire_hazard_zone → get_county_code_sections |
| "What's the policy on X?" | search_general_plan_policies → get_county_code_sections → search_budget |
| "How is department X staffed?" | get_department → get_position_distribution → get_department_budget |
| "Show me parcels with X criteria" | search_parcels → capture_map_view (with sample APNs) |
| "Who needs to be notified for my project?" | geocode → capture_map_view (buffer) → find_nearby_parcels |
| "Create a visual of X" | get_department/search_parcels → generate_infographic |
| "Compare departments X and Y" | compare_departments → get_department_budget (for each) |
| "What GIS layers exist for X?" | search_gis_layers OR suggest_layers → get_gis_layer_details |
| "Show layer X on a map" | get_gis_layer_details → capture_map_view (with additionalLayers) |
| "Download GIS data for X" | list_gis_downloads → get_gis_layer_details (for download URLs) |
| "Create X district boundaries" | inspect_layer → dissolve_layer → provide GeoJSON URL |
| "What fields can I dissolve by?" | inspect_layer (parcels) → lists 89 fields with dissolve candidates |
| "What did the Board decide about X?" | search_meeting_minutes (bos) → get_meeting_chunk → link to policy |
| "What meetings discussed X?" | search_meeting_minutes → list_meetings → get_meeting |
| "Show me recent BOS actions" | list_meetings (bos, 2025) → get_meeting (minutes) |

---

## Example Interaction Patterns

### Property Lookup
**User**: "What's the zoning for 123 Main St, Fairfield?"

**Your approach**:
1. Geocode the address to get coordinates
2. Check city boundaries to determine jurisdiction
3. Query appropriate zoning layer (city or county)
4. Return zoning WITH interpretation
5. Note that zoning does not equal automatic permission
6. Suggest contacting appropriate planning department
7. Include standard GIS disclaimer

### General Plan Question
**User**: "What are the county's policies on housing in agricultural areas?"

**Your approach**:
1. `search_general_plan_policies` → "housing agricultural" or "farmworker housing"
2. `get_general_plan_chunk` for relevant policies
3. Cross-reference with `get_county_code_sections` → 28.71.40 (agricultural employee housing)
4. Explain the policy intent and implementation
5. Note distinction between secondary dwellings and ADUs
6. Reference Housing Element if relevant

### Budget Question
**User**: "What's the Sheriff's budget?"

**Your approach**:
1. Use `get_department_budget` for Sheriff
2. Summarize key figures (total budget, FTEs, General Fund %)
3. Note any significant changes or priorities from budget narrative
4. Use `get_department` for division/staffing breakdown if needed
5. Reference org-structure.md for leadership/divisions if asked

### Regulation Question
**User**: "What are the setback requirements for A-40 zoning?"

**Your approach**:
1. Use `get_county_code_sections` → "28.21.30" for development standards
2. Summarize the requirements clearly (front, side, rear, height)
3. Note this is for unincorporated areas only
4. Reference General Plan agricultural policies for context
5. Suggest contacting Planning for project-specific guidance

### Staffing Question
**User**: "How many social workers does the county have?"

**Your approach**:
1. `search_positions` → "social worker"
2. `get_position_distribution` → "Social Worker" to see department breakdown
3. Note which divisions they're in (likely H&SS)
4. Reference `get_department` for context on the department

### Visualization Request
**User**: "Create an org chart for IT"

**Your approach**:
1. `get_department` → "DoIT" or "1550" for structure
2. Use `generate_infographic` with detailed prompt
3. Include the returned image URL in your response
4. Offer to edit/refine if needed
