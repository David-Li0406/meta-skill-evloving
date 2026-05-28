# Data Pipeline

This document describes the CMM data pipeline from source data to knowledge graph.

## Overview

```
Google Sheets          MediaDive API         BacDive API
     │                      │                     │
     ▼                      ▼                     ▼
┌─────────────┐      ┌─────────────┐       ┌─────────────┐
│  TSV files  │      │   MongoDB   │       │   MongoDB   │
│ data/private│      │  mediadive  │       │   bacdive   │
└─────────────┘      └─────────────┘       └─────────────┘
     │                      │                     │
     └──────────────────────┼─────────────────────┘
                            ▼
                   ┌─────────────────┐
                   │   KGX Export    │
                   │  output/kgx/    │
                   │ *_nodes.tsv     │
                   │ *_edges.tsv     │
                   └─────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌─────────────┐             ┌─────────────┐
       │    Neo4j    │             │   RDF/JSONL │
       │ Graph DB    │             │   exports   │
       └─────────────┘             └─────────────┘
```

## Infrastructure Requirements

### MongoDB

MongoDB stores source data from MediaDive and BacDive APIs.

**Installation (Ubuntu/Debian):**
```bash
# Install MongoDB Community Edition
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Or via Docker:**
```bash
docker run -d --name mongodb -p 27017:27017 mongo:7
```

**Verify:**
```bash
mongosh --eval "db.adminCommand('ping')"
```

**Collections used:**
| Database | Collection | Description |
|----------|------------|-------------|
| mediadive | media | Base media list |
| mediadive | media_details | Detailed media info |
| mediadive | ingredient_details | Chemical ingredients |
| mediadive | solution_details | Stock solutions |
| mediadive | strains | Strain data with growth info |
| mediadive | medium_compositions | Flattened ingredient lists |

### Neo4j

Neo4j stores the final knowledge graph for querying and visualization.

**Start via Docker (recommended):**
```bash
just neo4j-start
```

This runs:
```bash
docker run -d --name cmm-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -v cmm-neo4j-data:/data \
  -e NEO4J_AUTH=neo4j/${NEO4J_PASSWORD} \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:5
```

**Access:**
- Browser UI: http://localhost:7474
- Bolt protocol: bolt://localhost:7687

**Credentials:** Set `NEO4J_USER` and `NEO4J_PASSWORD` in `.env`

### Docker

Required for Neo4j. Install from https://docs.docker.com/get-docker/

## Pipeline Steps

### Step 1: Load Source Data into MongoDB

```bash
# Load MediaDive base data (media, solutions, ingredients)
# Time: ~10 seconds
just load-mediadive

# Fetch detailed data (media details, ingredient details, strains)
# Time: 3-4+ hours (~64,000 API calls with rate limiting)
just load-mediadive-details

# Optional: Load BacDive strain data
# Requires BACDIVE_EMAIL and BACDIVE_PASSWORD in .env
just load-bacdive
```

### Step 2: MongoDB Maintenance (Optional)

```bash
# Merge unique data before dropping redundant collections
just mediadive-merge-references
just mediadive-merge-bacdive-ids

# Drop redundant collections (runs merge first)
just mediadive-drop-redundant

# Backup/restore
just mediadive-backup
just mediadive-restore 20251219
```

### Step 3: Export to KGX Format

```bash
# Clean and export MediaDive to KGX
just mediadive-kgx-clean-export
```

**Output files:**
- `output/kgx/mediadive_nodes.tsv` - All nodes (media, strains, ingredients, solutions)
- `output/kgx/mediadive_edges.tsv` - All edges (grows_in, contains)

**Node types:**
| Category | Prefix | Count |
|----------|--------|-------|
| Growth Media | mediadive.medium:{id} | ~3,300 |
| Strains | mediadive.strain:{id} | ~47,000 |
| Ingredients | mediadive.ingredient:{id} | ~1,200 |
| Solutions | mediadive.solution:{id} | ~5,800 |

**Edge types:**
| Predicate | Meaning | Count |
|-----------|---------|-------|
| METPO:2000517 | grows_in (strain→medium) | ~72,000 |
| RO:0001019 | contains (medium/solution→ingredient) | ~53,000 |

### Step 4: Load into Neo4j

Two loading approaches available:

```bash
# Option A: KGX tool (recommended)
# - Proper list handling (xref, synonym as arrays)
# - Generic "Node" labels
just neo4j-upload-kgx

# Option B: Custom loader
# - Custom labels (GrowthMedium, Strain, Ingredient, Solution)
# - Lists stored as pipe-delimited strings
just neo4j-upload-custom
```

### Step 5: Query and Explore

**Neo4j Browser:** http://localhost:7474

**Sample queries:**
```cypher
-- Count nodes by category
MATCH (n) RETURN n.category, count(*) ORDER BY count(*) DESC

-- Find media containing a specific ingredient
MATCH (m)-[:CONTAINS]->(i)
WHERE i.name = 'Agar'
RETURN m.name, m.id LIMIT 10

-- Find strains that grow on a medium
MATCH (s)-[:GROWS_IN]->(m)
WHERE m.name CONTAINS 'Nutrient'
RETURN s.name, s.culture_collection_id LIMIT 10

-- Get ingredient cross-references
MATCH (i:Node) WHERE i.xref IS NOT NULL
RETURN i.name, i.xref LIMIT 10
```

## Google Sheets Pipeline

Separate from MediaDive, data can also come from Google Sheets:

```bash
# Download sheets to TSV
just download-sheets

# Export to KGX (strains, growth, media-ingredients)
just strains-kgx-from-curies <input.tsv> <id_column>
just kgx-export-growth
just kgx-export-media-ingredients

# Or all at once
just kgx-export-all
```

## Troubleshooting

### MongoDB Connection Issues
```bash
# Check if mongod is running
sudo systemctl status mongod

# Check connection
mongosh --eval "db.adminCommand('ping')"
```

### Neo4j Issues
```bash
# Check container status
just neo4j-status

# View logs
docker logs cmm-neo4j

# Full reset (deletes all data)
just neo4j-clean
just neo4j-start
```

### KGX Export Issues
```bash
# Verify MongoDB has data
mongosh mediadive --eval "db.media_details.countDocuments()"

# Check output files
ls -la output/kgx/
```
