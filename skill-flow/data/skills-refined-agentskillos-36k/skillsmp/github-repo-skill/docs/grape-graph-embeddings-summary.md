# GRAPE & Graph Embeddings Summary

> Generated: 2025-12-18

## What is GRAPE?

**GRAPE** (Graph Representation Learning library for Predictions and Evaluations) is a Rust/Python library developed by AnacletoLAB (University of Milan) in collaboration with LBNL/Monarch Initiative.

| Stat | Value |
|------|-------|
| GitHub | https://github.com/AnacletoLAB/grape |
| Stars | 615 |
| Paper | doi.org/10.1038/s43588-023-00465-8 |

**Two components:**
- **Ensmallen** - performant graph library (loading, manipulation, random walks)
- **Embiggen** - graph ML library (https://github.com/monarch-initiative/embiggen)

## Key Capabilities

1. **Performance** - Loads billion-node graphs in minutes on commodity hardware (~1 order of magnitude faster than alternatives)
2. **80 embedding models** - Node2Vec, LINE, etc.
3. **59 ML models** - scikit-learn, TensorFlow, PyTorch, PyKeen integrations
4. **DANS** - Degree-Aware Negative Sampling for better link prediction on biomedical KGs
5. **API access to 163,010 graphs** including KG-Hub graphs

## Your Involvement (from sources)

### Google Drive presentations (Justin Reese):
- "Practical Machine Learning on Knowledge Graphs" (SC23)
- KG-Hub presentations at ISMB 2023, WUSTL 2024
- Drug repurposing use cases (COVID-19, NSAIDs, metformin)

### Gmail thread (Marcin → Ben Busby @ NVIDIA, Aug 2025):
- Marcin working on **relation graph transformers** for KG-Microbe
- Struggling with A100s at NERSC on graphs with millions of nodes/edges
- NVIDIA interested in helping accelerate the approach
- Marcin mentioned "embedding health game" - training taking longer

### Slack discussions:
- Chris Mungall discussing **satellite image embeddings** for predicting ENVO/GOLD terms
- **env-embeddings** repo: https://github.com/contextualizer-ai/env-embeddings
- **biosample-enricher** repo: https://github.com/contextualizer-ai/biosample-enricher
- Monarch R24 grant tracking KG embedding evaluation (Aim 2.2.2)

## Related Work at LBNL/BerkeleyBOP

- **KG-Hub** (kghub.org) - federated KG ecosystem
- **KG-Microbe** - microbial data integration
- **OntoGPT/SPIRES** - LLM-based KG extraction from literature
- Marcin exploring **Relational Graph Transformers** (ReLiKT, KG-Former naming ideas)

## Open Issues

| Repo | Issue | Topic |
|------|-------|-------|
| AnacletoLAB/grape | #66 | Node/edge features support (unanswered) |
| AnacletoLAB/grape | #8 | Generating node embeddings from word embeddings |
| monarch-initiative/monarch_R24_grant_tracker | #23 | KG embedding evaluation |

## Key Links

- GRAPE repo: https://github.com/AnacletoLAB/grape
- Embiggen repo: https://github.com/monarch-initiative/embiggen
- KG-Hub: https://kghub.org
- env-embeddings: https://github.com/contextualizer-ai/env-embeddings
- biosample-enricher: https://github.com/contextualizer-ai/biosample-enricher

## Sources

- Google Drive: Justin Reese presentations on KG-Hub and GRAPE
- Gmail: Thread with Marcin Joachimiak and Ben Busby (NVIDIA) re: graph transformers
- Slack (NMDC, BerkeleyBOP): Discussions on embeddings for metadata prediction
- GitHub: GRAPE issues and Monarch grant tracker
