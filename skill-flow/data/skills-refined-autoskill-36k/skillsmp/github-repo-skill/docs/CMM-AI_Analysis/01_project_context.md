# Chapter 1: Project Context

[<- Back to Index](00_index.md) | [Next: Data Model Analysis ->](02_data_model_analysis.md)

---

## DOE BER Critical Minerals Proposal

### Funding & Leadership

| Field | Value |
|-------|-------|
| **Project Title** | Advanced Biorecovery of Critical Minerals through AI/ML-Guided Design of Microbial Chassis and Bioadsorbent |
| **Prime Lab** | Lawrence Berkeley National Laboratory |
| **Partner** | University of California, Berkeley |
| **Principal Investigator** | Ning Sun (nsun@lbl.gov) |
| **Co-PIs** | Marcin Joachimiak, Rebecca Abergel, Romy Chakraborty, Yasuo Yoshikuni, N. Cecilia Martinez-Gomez |
| **Funding** | $850,000 |
| **Period** | 12 months (Year 1) |
| **Proposal Document** | `data/proposal/BER CMM Pilot Proposal-revised .docx` |

### Scientific Goals

The project aims to develop **AI/ML-guided biorecovery technology** for rare earth elements (REEs) through:

1. **Bioleaching** - Microbial extraction of REEs from waste
2. **Biomineralization** - Microbial precipitation of REE minerals
3. **Bioadsorption** - Microbial binding/accumulation of REEs

### The Knowledge Graph (KG-CMREE)

From the proposal:
> "The AI/ML framework for microbial biomineralization centers on constructing a comprehensive AI-ready data substrate in the form of a **Knowledge Graph for Critical Minerals and Rare Earth Elements (KG-CMREE)**."

This explains why the CMM-AI repo exists - it's building the data foundation for KG-CMREE.

### Task 1.1 from Proposal (AI/ML Framework)

> "Working with this core data resource we will apply both symbolic rule-mining to extract interpretable IF-THEN rules and advanced graph learning techniques including Graph Transformers to rank candidate taxa, pathways, and proteins for REE recovery."

**Multi-Agent System Components:**
- **Literature and Data Mining Agent** - LLM-assisted extraction from lanthanome publications
- **Experiment Design Agent** - Uses historical outcomes and predictive models
- **Failure Analysis Agent** - Learns from unsuccessful experiments

### Year 1 Deliverables (Relevant to Data)

1. Establish spectroscopic assays for REE quantification (HTP)
2. Identify/validate microbial strains with high REE bioaccumulation via AI/ML
3. Establish HTP pipeline for strain screening
4. **Establish AI/ML-guided framework as unified source of data integration**

---

## Key Organisms Mentioned

- *Methylobacterium extorquens AM1* (methylolanthanin producer)
- *Methylorubrum* species
- *Acidithiobacillus ferrooxidans*, *A. thiooxidans* (extremophiles)
- *Leptospirillum ferrooxidans*, *Sulfobacillus thermosulfidooxidans*
- *Pichia kudriavzevii* (fungal chassis)
- Martinez-Gomez collection (~20 strains with REE transport mechanisms)

## Key Chemicals/Molecules

- **Lanthanophores** (REE chelators): methylolanthanin (MLL), rodopetrobactin
- **Antenna ligands**: beta-diketonates, hydroxypyridinone derivatives
- **Target REEs**: Eu3+, Tb3+, gadolinium

---

## Connection to BER Data Lakehouse

From BBOP Slack (Chris Mungall, Oct 2025):

> "BER are also positioning the DLH concept more broadly for the cross-DOE AmSC, and possibly even manhattan project 2. We should make sure our groundbreaking KG work doesn't get too far ahead of DLH. It's better to own a table in the DLH and derive the KG from that than doing something unconnected."

This suggests the CMM-AI data tables may eventually need to align with DOE's broader **Data Lakehouse** initiative, and that:
- KG-CMREE should derive from DLH tables (not be independent)
- There's pressure for "analytics ready flattened denormalized forms"
- The `linkml/valuesets` repo contains "PVs for things like critical minerals"

---

## How Data Tables Map to Proposal Tasks

The 16 Google Sheet tabs are **seed data for KG-CMREE** - the Knowledge Graph that drives the AI/ML framework:

| Data Table | Proposal Connection |
|------------|---------------------|
| **taxa_and_genomes** | Candidate taxa for REE recovery (Task 2.1: "strains from Martinez-Gomez collection ~20") |
| **genes_and_proteins** | Lanthanophore biosynthetic clusters, REE-binding proteins (Task 2.1: "novel biosynthetic clusters producing novel lanthanophores") |
| **pathways** | Metabolic pathways for REE metabolism (Task 1.1: "rank candidate taxa, pathways, and proteins") |
| **chemicals** | Lanthanophores, chelators, REEs themselves (methylolanthanin, rodopetrobactin, beta-diketonates) |
| **strains** | Martinez-Gomez collection strains, ATCC/DSMZ culture collection IDs |
| **growth_media** / **media_ingredients** | Culture conditions for REE bioaccumulation experiments (Task 2.1: "grown comparing use of REE in soluble vs insoluble form") |
| **assays** | TRL assay, ICP-OES, FACS methods (Task 1.2: spectroscopic assay development) |
| **screening_results** | HTP strain screening output (Task 1.3: "6,000 samples per day") |
| **bioprocesses** | Bioleaching, biomineralization, bioadsorption conditions |
| **protocols** | SOPs for the HTP pipeline |
| **publications** | Lanthanome literature for the "Literature and Data Mining Agent" |
| **macromolecular_structures** | REE-binding protein structures for AI/ML prediction |
| **biosamples** | Environmental samples for isolate discovery |
| **datasets** / **transcriptomics** | Multi-omics data feeding into KG-CMREE |

### The Intended Data Flow (from Proposal)

```
Experimental Collaborators (Martinez-Gomez lab, etc.)
    |
    v
Google Sheets (manual entry of strains, assay results, media formulations)
    |
    v
KG-CMREE (Knowledge Graph)
    |
    v
AI/ML Agents (Literature Mining, Experiment Design, Failure Analysis)
    |
    v
DBTL Loop predictions -> back to experimentalists
```

### Why This Matters

The Google Sheets aren't just a data dump - they're **the human-machine interface** for the DBTL (Design-Build-Test-Learn) cycle:

1. **Experimentalists** enter screening results, new strains, assay data
2. **KG-CMREE** integrates this with literature and database knowledge
3. **AI agents** make predictions about which strains/conditions to try next
4. **Results** feed back into the sheets

### What the Sheets SHOULD Capture (Based on Proposal)

**screening_results** (Task 1.3 - HTP screening pipeline):
- Strain barcode
- REE type tested (Eu3+, Tb3+, etc.)
- TRL assay measurements
- Hit classification
- Link back to strain in strains table

**strains** (Task 2.1 - strain engineering):
- Martinez-Gomez collection IDs
- Lanthanophore gene clusters identified
- Growth rate/yield on different REEs
- Transcriptomic profile references

**assays** (Task 1.2 - spectroscopic assay development):
- TRL assay parameters (antenna ligands, detection limits)
- ICP-OES protocols
- FACS sorting criteria

The current tables have the right *structure* but the *workflow* for populating them from experiments isn't documented or automated.

---

## The Core Problem

The current workflow is **broken for the DBTL cycle** because:

| Issue | Impact on Proposal Goals |
|-------|-------------------------|
| **No real-time sync** | KG-CMREE can't see latest experimental data (XLSX download is manual) |
| **No structured entry** | Experimentalists can type anything; no validation against schema |
| **No provenance** | Can't tell if a strain recommendation came from AI or was manually entered |
| **Two disconnected tables** | `data/txt/sheet/` vs `extended/` means AI predictions and human data aren't merged |
| **No feedback loop** | AI agent outputs don't flow back to experimentalists in structured form |

---

[<- Back to Index](00_index.md) | [Next: Data Model Analysis ->](02_data_model_analysis.md)
