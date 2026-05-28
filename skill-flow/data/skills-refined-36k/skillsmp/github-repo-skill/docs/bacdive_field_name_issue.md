# BacDive MongoDB Field Name Issue

## Problem

The BacDive MongoDB collection has a field with a **period in the field name**:
```
"External links" → "culture collection no."
```

Note the trailing period after "no"!

## Why This Breaks Standard Queries

MongoDB interprets periods in field paths as nested object separators. When you try to query:

```javascript
db.strains.findOne({
  "External links.culture collection no.": /DSM 1337/
})
```

MongoDB interprets this as:
1. Field "External links"
2. → Nested field "culture collection no"
3. → Nested field "" (empty string, from the trailing period)

This causes:
```
OperationFailure: FieldPath must not end with a '.'
```

## Evidence

```javascript
// This returns 99392 documents
db.strains.count({"External links": {$exists: true}})

// This returns 0 documents!
db.strains.count({"External links.culture collection no.": {$exists: true}})
```

## Solution: Use Aggregation Pipeline

Use `$getField` to access fields with special characters:

```javascript
db.strains.aggregate([
  {
    $match: {
      "External links": {$exists: true}
    }
  },
  {
    $addFields: {
      cc_field: {
        $getField: {
          field: "culture collection no.",
          input: "$External links"
        }
      }
    }
  },
  {
    $match: {
      cc_field: {$regex: "DSM 1337"}
    }
  }
])
```

## Python Implementation

```python
from pymongo import MongoClient

def search_culture_collection(collection, search_string):
    """Search for culture collection ID using aggregation."""
    pipeline = [
        {
            "$match": {
                "External links": {"$exists": True}
            }
        },
        {
            "$addFields": {
                "cc_field": {"$getField": {
                    "field": "culture collection no.",
                    "input": "$External links"
                }}
            }
        },
        {
            "$match": {
                "cc_field": {"$regex": search_string}
            }
        },
        {
            "$limit": 1
        },
        {
            "$project": {
                "BacDive-ID": "$General.BacDive-ID",
                "DSM-Number": "$General.DSM-Number",
                "culture_collection": "$cc_field"
            }
        }
    ]

    results = list(collection.aggregate(pipeline))
    return results[0] if results else None

# Usage
client = MongoClient("mongodb://localhost:27017")
collection = client["bacdive"]["strains"]

# Transform "DSM:1337" → "DSM 1337"
search_string = "DSM 1337"
doc = search_culture_collection(collection, search_string)
```

## Important: Word Boundary Matching

The simple regex above has a problem - "DSM 1337" will match "DSM 13378" as a substring!

Use word boundaries in regex:

```javascript
{
  $match: {
    cc_field: {
      $regexMatch: {
        input: "$cc_field",
        regex: "(^|,\\s*)DSM 1337(\\s*,|$)"
      }
    }
  }
}
```

Or in MongoDB aggregation 4.2+:

```javascript
{
  $match: {
    $expr: {
      $regexMatch: {
        input: "$cc_field",
        regex: "(^|,\\s*)DSM 1337(\\s*,|$)"
      }
    }
  }
}
```

## Alternative: Fetch Parent Object

Another approach is to fetch the entire "External links" object and search in Python:

```python
doc = collection.find_one({"General.DSM-Number": 1337})
if doc:
    external_links = doc.get("External links", {})
    cc_string = external_links.get("culture collection no.", "")

    if "DSM 1337" in cc_string:
        print("Found!")
```

This is less efficient but simpler for one-off queries.

## Recommendation for Reconciliation

For the strain reconciliation tool, use **two-stage search**:

1. **Primary search**: `General.DSM-Number` (integer field, fast, indexed)
2. **Fallback search**: Aggregation pipeline on "culture collection no." field

This provides the best of both worlds:
- Fast lookups for DSM strains
- Comprehensive coverage for other culture collections

```python
def find_strain(collection, culture_collection_id):
    # Parse the ID
    match = re.match(r"([A-Z]+)[:\s-]*(\d+)", culture_collection_id)
    if not match:
        return None

    prefix = match.group(1).upper()
    number = match.group(2)

    # Fast path: DSM number
    if prefix == "DSM":
        doc = collection.find_one({"General.DSM-Number": int(number)})
        if doc:
            return doc

    # Slow path: Search in culture collection string
    search_string = f"{prefix} {number}"
    return search_via_aggregation(collection, search_string)
```

## Test Results

Tested with 23 culture collection IDs from strains.tsv:
- **Standard query approach**: 0 found (all failed due to field name issue)
- **Aggregation approach**: 22 found, 1 not found (NCIMB:13946)
- **DSM-Number integer approach**: 10 found (all DSM IDs)

## Files

- Working search script: `/tmp/search_with_aggregation.py`
- Test script: `/tmp/test_regex.py`
