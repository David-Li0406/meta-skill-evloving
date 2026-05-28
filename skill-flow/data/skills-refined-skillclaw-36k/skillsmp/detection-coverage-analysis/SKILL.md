---
name: detection-coverage-analysis  
description: Analyzes detection coverage using Sigma, Splunk, and Elastic rules. Use when checking coverage for techniques, tactics, threat actors, or generating Navigator layers from detections.
---

# Detection Coverage Analysis

## Efficient Tools (Use These!)

### Get Coverage Stats
```
analyze_coverage(source_type: "elastic")
```
Returns coverage % by tactic, top techniques, weak spots.

### Find Gaps by Threat Profile
```
identify_gaps(threat_profile: "ransomware")
identify_gaps(threat_profile: "apt")
identify_gaps(threat_profile: "persistence")
```
Returns prioritized P0/P1/P2 gaps with recommendations.

### Get Detection Suggestions
```
suggest_detections(technique_id: "T1059.001")
```
Returns existing detections, data sources needed, detection ideas.

### Generate Navigator Layer
```
generate_navigator_layer(
  name: "Elastic Initial Access",
  source_type: "elastic",
  tactic: "initial-access"
)
```
Returns ready-to-import Navigator JSON.

### Get Just Technique IDs
```
get_technique_ids(source_type: "elastic", tactic: "persistence")
```
Returns ~200 bytes instead of ~50KB.

## Threat Profiles Available

| Profile | Key Techniques |
|---------|----------------|
| ransomware | T1486, T1490, T1027, T1547 |
| apt | T1003, T1021, T1053, T1071 |
| initial-access | T1566, T1190, T1078 |
| persistence | T1547, T1543, T1053 |
| credential-access | T1003.*, T1555, T1552 |
| defense-evasion | T1027, T1070, T1055 |

## DON'T (burns tokens)
```
# BAD - returns 200+ full detection objects
list_by_mitre_tactic(tactic: "execution")
```

## DO (efficient)
```
# GOOD - returns stats only
analyze_coverage(source_type: "elastic")
```

## Token Comparison

| Old Approach | New Approach |
|--------------|--------------|
| list_by_mitre_tactic → ~50KB | analyze_coverage → ~2KB |
| Parse in context | Done server-side |
| 25x more tokens | Efficient |
