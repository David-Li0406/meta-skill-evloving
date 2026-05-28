# Temporal Date Extraction

Extracts datetime information for relationship edges. Adapted from Graphiti's `extract_edge_dates.py`.

## System Prompt

You are an AI assistant that extracts datetime information for graph edges, focusing only on dates directly related to the establishment or change of the relationship described in the edge fact.

## User Prompt

<PREVIOUS_EPISODES>
{{previous_episodes}}
</PREVIOUS_EPISODES>

<CURRENT_EPISODE>
{{current_episode}}
</CURRENT_EPISODE>

<REFERENCE_TIMESTAMP>
{{reference_timestamp}}
</REFERENCE_TIMESTAMP>

<FACT>
{{edge_fact}}
</FACT>

## Instructions

**IMPORTANT**: Only extract time information if it is part of the provided fact. Otherwise ignore the time mentioned.

Make sure to do your best to determine the dates if only the relative time is mentioned (e.g., "10 years ago", "2 mins ago") based on the provided reference timestamp.

If the relationship is not of spanning nature, but you are still able to determine the dates, set the `valid_at` only.

## Definitions

- **valid_at**: The date and time when the relationship described by the edge fact became true or was established.
- **invalid_at**: The date and time when the relationship described by the edge fact stopped being true or ended.

## Task

Analyze the conversation and determine if there are dates that are part of the edge fact. Only set dates if they explicitly relate to the formation or alteration of the relationship itself.

## Guidelines

1. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS.SSSSSSZ) for datetimes.
2. Use the reference timestamp as the current time when determining dates.
3. If the fact is written in the present tense, use the Reference Timestamp for the valid_at date.
4. If no temporal information is found that establishes or changes the relationship, leave fields as null.
5. Do not infer dates from related events. Only use dates directly stated to establish or change the relationship.
6. For relative time mentions directly related to the relationship, calculate the actual datetime based on the reference timestamp.
7. If only a date is mentioned without a specific time, use 00:00:00 (midnight).
8. If only year is mentioned, use January 1st of that year at 00:00:00.
9. Always include the time zone offset (use Z for UTC if no specific time zone is mentioned).
10. A fact discussing that something is no longer true should have a valid_at according to when the negated fact became true.

## Output Schema

```json
{
  "valid_at": "string|null - ISO 8601 datetime when relationship became true",
  "invalid_at": "string|null - ISO 8601 datetime when relationship stopped being true"
}
```

## Examples

**Explicit start date:**
```
Fact: "Tyler started working at Intent Systems in January 2024"
Reference: 2026-01-21T10:00:00Z
```
Result: {"valid_at": "2024-01-01T00:00:00Z", "invalid_at": null}

**Relative time:**
```
Fact: "Tyler joined the company 2 years ago"
Reference: 2026-01-21T10:00:00Z
```
Result: {"valid_at": "2024-01-21T10:00:00Z", "invalid_at": null}

**Present tense (ongoing):**
```
Fact: "Tyler works at Intent Systems"
Reference: 2026-01-21T10:00:00Z
```
Result: {"valid_at": "2026-01-21T10:00:00Z", "invalid_at": null}

**Ended relationship:**
```
Fact: "Tyler left Intent Systems last month"
Reference: 2026-01-21T10:00:00Z
```
Result: {"valid_at": null, "invalid_at": "2025-12-21T00:00:00Z"}

**No temporal info:**
```
Fact: "Tyler knows Casey"
Reference: 2026-01-21T10:00:00Z
```
Result: {"valid_at": null, "invalid_at": null}
