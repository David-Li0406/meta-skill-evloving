# BacDive MongoDB Reconciliation Queries

Reference guide for querying the local BacDive MongoDB database for strain reconciliation.

## Important Fields for Reconciliation - Deep Dive

### 1. **DSM Number** (`General.DSM-Number`)
**Why critical**: Primary identifier for DSMZ strains, most reliable lookup
**Data type**: Integer (NOT string)

**MongoDB queries**:
```javascript
// Exact match (fastest, indexed)
db.strains.findOne({"General.DSM-Number": 1338})

// IMPORTANT: This will FAIL - DSM-Number is an integer, not a string
// db.strains.findOne({"General.DSM-Number": "1338"})  // ❌ WRONG

// Find all DSM strains in a range
db.strains.find({"General.DSM-Number": {$gte: 1330, $lte: 1340}})

// Convert string input to integer for search
// In JavaScript
let dsmInput = "1338";
db.strains.findOne({"General.DSM-Number": parseInt(dsmInput)})

// In Python
dsm_input = "1338"
collection.find_one({"General.DSM-Number": int(dsm_input)})
```

### 2. **BacDive ID** (`General.BacDive-ID` or `_id`)
**Why critical**: Unique identifier across entire BacDive database

```javascript
// By BacDive ID
db.strains.findOne({"General.BacDive-ID": 7143})

// By MongoDB _id (usually same as BacDive-ID)
db.strains.findOne({"_id": 7143})

// Find multiple BacDive IDs at once
db.strains.find({"General.BacDive-ID": {$in: [7143, 7144, 7145]}})
```

### 3. **NCBI Taxonomy ID** (`General.NCBI tax id.NCBI tax id`)
**Why critical**: Links to NCBI Taxonomy, but **NOT unique** - many strains can share same species-level taxon

```javascript
// By NCBI taxon ID
db.strains.find({"General.NCBI tax id.NCBI tax id": 408})

// With matching level filter (species vs strain)
db.strains.find({
  "General.NCBI tax id.NCBI tax id": 408,
  "General.NCBI tax id.Matching level": "species"
})

// Find strain-level taxon matches (more specific)
db.strains.find({
  "General.NCBI tax id.Matching level": "strain"
})

// Alternative path if structure differs
db.strains.find({"NCBI tax id": 408})
```

### 4. **Culture Collection IDs** (`External links.culture collection no.`)
**Why critical**: Cross-references to other culture collections - **STRING FIELD** with comma-separated list

```javascript
// Exact substring match for ATCC 14718
db.strains.findOne({
  "External links.culture collection no.": /ATCC 14718/
})

// Word boundary regex (prevents "DSM 1" from matching "DSM 11")
db.strains.findOne({
  "External links.culture collection no.": {
    $regex: /(^|,\s*)ATCC 14718(\s*,|$)/
  }
})

// Case-insensitive search for any NCIMB entry
db.strains.find({
  "External links.culture collection no.": {
    $regex: /NCIMB/i
  }
})

// Find strains in multiple collections
db.strains.find({
  "External links.culture collection no.": {
    $regex: /DSM 1338|JCM 2805/
  }
})

// All strains with ATCC numbers
db.strains.find({
  "External links.culture collection no.": {
    $regex: /\bATCC\s+\d+/
  }
})
```

### 5. **Strain Designation** (`Name and taxonomic classification.strain designation`)
**Why critical**: Human-readable strain identifier (e.g., "AM1", "KT2440"), but can have **multiple comma-separated values**

```javascript
// Exact match for single designation
db.strains.findOne({
  "Name and taxonomic classification.strain designation": "AM1"
})

// Partial match (handles "0355, D355, AM1")
db.strains.find({
  "Name and taxonomic classification.strain designation": /AM1/
})

// Word boundary match (prevents "AM1" from matching "AM10")
db.strains.find({
  "Name and taxonomic classification.strain designation": {
    $regex: /\bAM1\b/
  }
})

// Case-insensitive
db.strains.find({
  "Name and taxonomic classification.strain designation": {
    $regex: /am-1/i
  }
})

// Alternative field path
db.strains.find({"strain designation": /KT2440/})
```

### 6. **Species Name** (`Name and taxonomic classification.species`)
**Why critical**: Binomial name, but **NOT unique** - returns ALL strains of that species

```javascript
// Exact species match
db.strains.find({
  "Name and taxonomic classification.species": "Methylorubrum extorquens"
})

// Case-insensitive
db.strains.find({
  "Name and taxonomic classification.species": {
    $regex: /^Methylorubrum extorquens$/i
  }
})

// Genus-level search
db.strains.find({
  "Name and taxonomic classification.genus": "Methylorubrum"
})

// Partial species name
db.strains.find({
  "Name and taxonomic classification.species": {
    $regex: /Methylo.*extorquens/i
  }
})

// Alternative paths (older records)
db.strains.find({"species": "Methylorubrum extorquens"})
db.strains.find({"Name and taxonomic classification.LPSN.species": "Methylorubrum extorquens"})
```

### 7. **Synonyms** (`Name and taxonomic classification.LPSN.synonyms`)
**Why critical**: Finds strains by old/alternative scientific names, **ARRAY field**

```javascript
// Find by synonym (exact match in array)
db.strains.find({
  "Name and taxonomic classification.LPSN.synonyms.synonym": "Methylobacterium extorquens"
})

// Case-insensitive synonym search
db.strains.find({
  "Name and taxonomic classification.LPSN.synonyms.synonym": {
    $regex: /Protomonas extorquens/i
  }
})

// Find any strain with "Methylobacterium" synonym
db.strains.find({
  "Name and taxonomic classification.LPSN.synonyms.synonym": {
    $regex: /Methylobacterium/
  }
})

// Check if synonyms array exists and is not empty
db.strains.find({
  "Name and taxonomic classification.LPSN.synonyms": {
    $exists: true,
    $ne: []
  }
})
```

### 8. **Genome Accession** (`Sequence information.Genome sequences.accession`)
**Why critical**: Links to NCBI GenBank genome assembly, **unique identifier**

```javascript
// Exact genome accession
db.strains.findOne({
  "Sequence information.Genome sequences.accession": "GCA_000022685"
})

// Partial accession (GCA_ or GCF_)
db.strains.find({
  "Sequence information.Genome sequences.accession": {
    $regex: /^GCA_000022/
  }
})

// All strains with genomes
db.strains.find({
  "Sequence information.Genome sequences": {
    $exists: true
  }
})

// Alternative path for arrays
db.strains.findOne({
  "Sequence information.Genome sequences.0.accession": "GCA_000022685"
})
```

### 9. **16S rRNA Sequences** (`Sequence information.16S sequences`)
**Why critical**: Links to NCBI nucleotide sequences, **ARRAY field**

```javascript
// By 16S accession
db.strains.find({
  "Sequence information.16S sequences.accession": "AF293375"
})

// Find strains with 16S sequences
db.strains.find({
  "Sequence information.16S sequences": {
    $exists: true,
    $ne: []
  }
})

// By 16S sequence NCBI tax ID
db.strains.find({
  "Sequence information.16S sequences.NCBI tax ID": 408
})
```

### 10. **Full Scientific Name** (`Name and taxonomic classification.full scientific name`)
**Why critical**: Complete name with author/year, good for disambiguation

```javascript
// Exact match
db.strains.find({
  "Name and taxonomic classification.full scientific name":
    "Methylorubrum extorquens (Urakami and Komagata 1984) Green and Ardley 2018"
})

// Partial match (ignore author/year)
db.strains.find({
  "Name and taxonomic classification.full scientific name": {
    $regex: /^Methylorubrum extorquens/
  }
})

// Also check LPSN full name (may differ)
db.strains.find({
  "Name and taxonomic classification.LPSN.full scientific name": {
    $regex: /Methylorubrum extorquens/
  }
})
```

### 11. **Type Strain Status** (`Name and taxonomic classification.type strain`)
**Why critical**: Identifies authoritative reference strains

```javascript
// Find type strains only
db.strains.find({
  "Name and taxonomic classification.type strain": "yes"
})

// Find non-type strains
db.strains.find({
  "Name and taxonomic classification.type strain": "no"
})

// Type strains of specific species
db.strains.find({
  "Name and taxonomic classification.species": "Methylorubrum extorquens",
  "Name and taxonomic classification.type strain": "yes"
})
```

### 12. **Strain History** (`General.strain history`)
**Why critical**: Tracks strain provenance, may mention alternative designations

```javascript
// Search in strain history text
db.strains.find({
  "General.strain history.history": {
    $regex: /NCIB 9133/i
  }
})

// Find strains with provenance from specific source
db.strains.find({
  "General.strain history.history": {
    $regex: /Quayle/
  }
})
```

### 13. **StrainInfo Links** (`External links.straininfo link.straininfo`)
**Why critical**: Cross-reference to StrainInfo database

```javascript
// By StrainInfo ID
db.strains.findOne({
  "External links.straininfo link.straininfo": 45565
})

// All strains with StrainInfo entries
db.strains.find({
  "External links.straininfo link": {
    $exists: true
  }
})
```

---

## **Multi-field Reconciliation Query**
Combine multiple fields for comprehensive search:

```javascript
// Find strain by ANY identifier
db.strains.find({
  $or: [
    {"General.DSM-Number": 1338},
    {"General.BacDive-ID": 7143},
    {"General.NCBI tax id.NCBI tax id": 408},
    {"External links.culture collection no.": /ATCC 14718/},
    {"Name and taxonomic classification.strain designation": /AM1/},
    {"Sequence information.Genome sequences.accession": "GCA_000022685"}
  ]
})

// Score matches by number of fields matched (pseudo-confidence)
db.strains.aggregate([
  {
    $match: {
      $or: [
        {"General.DSM-Number": 1338},
        {"External links.culture collection no.": /JCM 2805/},
        {"Name and taxonomic classification.strain designation": /AM1/}
      ]
    }
  },
  {
    $addFields: {
      matchScore: {
        $add: [
          {$cond: [{$eq: ["$General.DSM-Number", 1338]}, 1, 0]},
          {$cond: [{$regexMatch: {input: "$External links.culture collection no.", regex: "JCM 2805"}}, 1, 0]},
          {$cond: [{$regexMatch: {input: "$Name and taxonomic classification.strain designation", regex: "AM1"}}, 1, 0]}
        ]
      }
    }
  },
  {$sort: {matchScore: -1}}
])
```

---

## **Important Caveats**

1. **Culture collection string is comma-separated** - always use regex with word boundaries
2. **NCBI taxon ID is NOT unique** - one species can have 100s of strains
3. **Strain designation can have multiple values** - "0355, D355, AM1"
4. **Synonyms are in nested arrays** - need to query the `synonym` field within array
5. **Some records may use different field paths** - always check alternate locations

---

## Example: Comprehensive Search for DSM:1338

```javascript
// Search by all available identifiers
db.strains.find({
  $or: [
    // Primary DSM number
    {"General.DSM-Number": 1338},

    // BacDive ID
    {"General.BacDive-ID": 7143},

    // NCBI taxonomy
    {"General.NCBI tax id.NCBI tax id": 408},

    // Culture collection IDs
    {"External links.culture collection no.": /(^|,\s*)DSM 1338(\s*,|$)/},
    {"External links.culture collection no.": /(^|,\s*)ATCC 14718(\s*,|$)/},
    {"External links.culture collection no.": /(^|,\s*)NCIB 9133(\s*,|$)/},
    {"External links.culture collection no.": /(^|,\s*)JCM 2805(\s*,|$)/},

    // Strain designation
    {"Name and taxonomic classification.strain designation": /\b(0355|D355|AM1)\b/i},

    // Species name
    {"Name and taxonomic classification.species": "Methylorubrum extorquens"},

    // Synonyms
    {"Name and taxonomic classification.LPSN.synonyms.synonym": "Methylobacterium extorquens"},

    // Genome accession
    {"Sequence information.Genome sequences.accession": "GCA_000022685"}
  ]
})
```

---

## Python Wrapper Function Template

```python
def search_bacdive_comprehensive(
    collection,
    dsm_number=None,
    bacdive_id=None,
    ncbi_taxon=None,
    culture_collection_ids=None,
    strain_designation=None,
    species_name=None,
    genome_accession=None
):
    """Comprehensive BacDive search by any identifier."""

    query_parts = []

    if dsm_number:
        # DSM-Number is stored as integer, not string
        query_parts.append({"General.DSM-Number": int(dsm_number)})

    if bacdive_id:
        query_parts.append({"General.BacDive-ID": bacdive_id})

    if ncbi_taxon:
        query_parts.append({"General.NCBI tax id.NCBI tax id": ncbi_taxon})

    if culture_collection_ids:
        for cc_id in culture_collection_ids:
            pattern = rf"(^|,\s*){re.escape(cc_id)}(\s*,|$)"
            query_parts.append({
                "External links.culture collection no.": {"$regex": pattern}
            })

    if strain_designation:
        query_parts.append({
            "Name and taxonomic classification.strain designation": {
                "$regex": rf"\b{re.escape(strain_designation)}\b",
                "$options": "i"
            }
        })

    if species_name:
        query_parts.append({
            "Name and taxonomic classification.species": species_name
        })

    if genome_accession:
        query_parts.append({
            "Sequence information.Genome sequences.accession": genome_accession
        })

    if not query_parts:
        return []

    query = {"$or": query_parts} if len(query_parts) > 1 else query_parts[0]

    return list(collection.find(query))
```
