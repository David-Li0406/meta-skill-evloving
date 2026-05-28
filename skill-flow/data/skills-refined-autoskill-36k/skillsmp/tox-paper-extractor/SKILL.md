---
name: tox-paper-extractor
description: End-to-end OA literature pipeline for toxicity/peptide experimental data. Use to discover candidates (Europe PMC), download OA full text + supplementary (PDF/JATS XML/PMC OA packages), extract traceable raw records (tables/supp → raw_extractions.csv + raw_experimental_records.csv + extracted_tables), generate monitoring reports, and screen records for training readiness (units/aggregation/censoring).
---

# Workflow (OA-only, reproducible)

Prereq: run inside this repo’s `docs/` directory (scripts are referenced as `scripts/...`).

For a detailed write-up of the pipeline rationale and artifacts, see `论文数据收集.md` (Section 8).

## Option A: One-command pipeline (recommended)

Run discovery → download → extraction → report in one shot:

```bash
python scripts/run_tox_paper_pipeline.py \
  --query '((hemolysis OR hemolytic OR erythrocyte) AND (antimicrobial peptide OR peptides) AND (MIC OR "minimum inhibitory concentration" OR HC50 OR CC50 OR IC50) AND (sequence OR sequences)) NOT PUB_TYPE:"Review"' \
  --max-results 50 \
  --min-score 5 \
  --out-root runs \
  --screen --screen-min-seq-len 8 --augment-methods --methods-taxonomy --summarize \
  --overwrite
```

Outputs (under `runs/<run_name>/papers/`):
- `download_manifest.jsonl`: full provenance of OA resolution + sha256
- `raw_extractions.csv`: raw entities with source pointers (table/supp/page)
- `raw_experimental_records.csv`: joined experimental records (sequence × endpoint × value × condition) with table-cell pointers
- `extracted_tables/*.csv`: reconstructed tables for audit
- `extraction_report.md`: compact monitoring report (counts + gaps + sample rows)

Optional (recommended): training-readiness screening (QC flags + per-paper summary):

```bash
python scripts/screen_experimental_records.py --input-dir runs/<run_name>/papers
```

Outputs:
- `screened_experimental_records.csv`: adds flags like `unit_missing/is_censored/is_aggregate/train_ready_*`
- `screening_report.md`: per-paper QC summary + “0-record papers” list
- `papers_with_zero_experimental_records.txt`: full list of papers with 0 extracted experimental records (useful for follow-up triage)

Tip: for large-scale runs, consider raising the screening min sequence length (e.g., 8) to reduce false AA-like strings from non-peptide tables:
```bash
python scripts/screen_experimental_records.py --input-dir runs/<run_name>/papers --min-seq-len 8
```

Optional (strongly recommended for cross-paper comparability): method conditions augmentation + taxonomy

Why: endpoints like `MIC/IC50/HC50/HEMOLYSIS` are not directly comparable across papers unless you account for
protocol differences (medium, inoculum, incubation, RBC source, readout wavelength, etc.). This step extracts
auditable method snippets from JATS XML and attaches them to each experimental record.

```bash
python scripts/augment_records_with_methods.py --papers-dir runs/<run_name>/papers
python scripts/summarize_methods_taxonomy.py --papers-dir runs/<run_name>/papers
```

Outputs (under `runs/<run_name>/papers/`):
- `methods_conditions_by_paper.csv`: paper-level method fields + evidence snippets + table ids used
- `screened_experimental_records_with_methods.csv`: per-record `method_*` fields (endpoint-aware) for training filters
- `methods_conditions_report.md`: coverage diagnostics (how many papers got each method field)
- `methods_taxonomy.csv` / `methods_taxonomy.md`: coarse method class labels + normalized key parameters

Practical training filters (examples):
- Restrict MIC to `abx_method_class=broth_microdilution` and consistent `abx_medium_norm`/`abx_inoculum_norm`.
- Restrict hemolysis to consistent `hem_rbc_source_norm` + `hem_readout_nm` + `hem_incubation_norm`.

Auditing: keep `method_evidence` + `method_source_ref` (and table ids) in any downstream dataset so every method
assignment is traceable back to the exact XML section/snippet.

Optional: Unpaywall improves OA PDF resolution (no token needed):

```bash
export UNPAYWALL_EMAIL="you@lab.edu"
```

## Option B: Step-by-step (when you want manual control)

### 1) Discover experimental-data candidates (Europe PMC, OA-friendly)

```bash
python scripts/discover_epmc_experimental_papers.py \
  --query '<YOUR_EPMC_QUERY>' \
  --max-results 200 \
  --min-score 5 \
  --out experimental_candidates.csv \
  --ids-out paper_ids.txt
```

### 2) Download OA artifacts (no paywall bypass)

```bash
python scripts/fetch_open_access_papers.py \
  --input paper_ids.txt \
  --out papers_oa \
  --format both \
  --supplementary
```

### 3) Extract raw + auditable records

```bash
python scripts/extract_paper_extractions.py --input-dir papers_oa --overwrite
python scripts/make_extraction_report.py --input-dir papers_oa
```

### 4) (Recommended) Screen extracted records for training comparability

```bash
python scripts/screen_experimental_records.py --input-dir papers_oa
```

## Option D: Build training datasets + leakage-safe splits (strict/relaxed + audit)

Use this when you want a **reproducible, auditable dataset** for model training/evaluation from one or more completed runs.

Prereq per run:
- `runs/<run_name>/papers/screened_experimental_records_with_methods.csv` (recommended) or at least `screened_experimental_records.csv`
- `runs/<run_name>/papers/raw_experimental_records.csv`
- `runs/<run_name>/papers/download_manifest.jsonl`

Example: merge multiple runs → write union + strict/relaxed + 2 split schemes + metric reconciliation:

```bash
python scripts/build_union_dataset_and_splits.py \
  --run-dir runs/oa_seq_peptide_fast_20260121_214200 \
  --run-dir runs/oa_seq_peptide_fast_oa_inpmc_20260121_220445 \
  --out-dir analysis/splits_400_<timestamp> \
  --seed 20260122
```

Outputs (under `analysis/splits_.../`):
- `records_union.parquet` / `records_union.csv.gz`: union dataset (keeps provenance: `pmcid/doi/source_path/source_ref/snippet/context`)
- `dataset_strict.parquet`: `train_ready_strict==True` (best for cross-paper benchmarks)
- `dataset_relaxed.parquet`: `train_ready_relaxed==True` (allows censored values; requires censor-aware modeling)
- `splits/`:
  - `split_by_paper`: groups by `pmcid` (prevents paper-level leakage)
  - `split_by_sequence`: groups by `sequence` (prevents same-sequence leakage; falls back to `pmcid` if sequence missing)
- `reports/metrics_recompute_vs_official.md`: recomputed metrics vs `sample200_metrics.json` (if present)
- `reports/dataset_profile.md`: endpoint/unit/method missingness, plus guidance on what `unknown` means

## Option E: Missed recovery loop (high-signal 0-record papers → deep-read → rule regression)

Use this when your run has a “high-signal but 0 experimental records” list (e.g., `sequence_present_but_no_records.csv`).
This is the fastest way to increase hit rate without tightening the search query.

### 0) (Recommended) Recompute the missed list after any extraction regression

After you change extraction rules and re-run `extract_paper_extractions.py`, regenerate the missed list so you don’t deep-read stale candidates:

```bash
python scripts/build_sequence_present_but_no_records.py \
  --run-dir runs/<run_name> \
  --write-meta
```

This writes `runs/<run_name>/sequence_present_but_no_records_recomputed.csv` (schema compatible with the worklist selectors below).

### 1) Select a deterministic worklist from the missed list

```bash
python scripts/select_missed_worklist.py \
  --missed-csv runs/<run_name>/sequence_present_but_no_records_recomputed.csv \
  --n 10 \
  --max-sequence-extractions 5000 \
  --require-experimental-records-eq-0 \
  --out-worklist analysis/missed_round1/worklist_<run_name>.txt \
  --out-meta analysis/missed_round1/worklist_<run_name>.meta.json
```

### 2) Build an analysis queue (atomic de-dup via mv)

```bash
python scripts/build_analysis_queue.py \
  --worklist analysis/missed_round1/worklist_<run_name>.txt \
  --papers-dir runs/<run_name>/papers \
  --analysis-dir analysis_llm_missed_<run_name>
```

### 3) Deep-read with workers (must open evidence files)

```bash
PROMPT_TEMPLATE=analysis/prompts/per_paper_prompt_deep.txt \
  SANDBOX=read-only MODEL=gpt-5 \
  bash scripts/start_analysis_workers_tmux.sh 2 missed_workers analysis_llm_missed_<run_name>
```

### 4) Turn findings into minimal rule regression + re-run extraction

Principle: prefer small, auditable improvements in `scripts/extract_paper_extractions.py` (table layout/join/header rules),
then re-run the deterministic pipeline on the same `papers/` directory:

```bash
python scripts/extract_paper_extractions.py --input-dir runs/<run_name>/papers --overwrite
python scripts/make_extraction_report.py --input-dir runs/<run_name>/papers
python scripts/screen_experimental_records.py --input-dir runs/<run_name>/papers
python scripts/augment_records_with_methods.py --papers-dir runs/<run_name>/papers
python scripts/summarize_methods_taxonomy.py --papers-dir runs/<run_name>/papers
python scripts/summarize_sample_run.py --papers-dir runs/<run_name>/papers
```

Finally, rebuild the training dataset + splits (Option D) so the benchmark artifacts stay consistent with the new extraction.

## Option F: Scale to 1000+ papers with 2 workers (2×500) without overlap

Recommended approach: **discover once → split IDs deterministically → run two independent runs** (two Codex windows) → merge datasets.

### 1) Discovery (OA + inPMC + PMCID) for 1000 candidates

Pick a query that enforces peptide/sequence + tox/assay endpoints. Example (tune as needed):

```bash
python scripts/discover_epmc_pmcids_fast.py \
  --query '((peptide OR peptides OR "antimicrobial peptide" OR toxin OR venom) AND (sequence OR sequences OR "amino acid sequence") AND (MIC OR "minimum inhibitory concentration" OR IC50 OR CC50 OR HC50 OR hemolysis OR cytotoxicity OR LD50 OR LC50)) NOT PUB_TYPE:"Review"' \
  --keep 1200 \
  --min-score 1 \
  --out analysis/oa1000/candidates_fast.csv \
  --ids-out analysis/oa1000/paper_ids_1200.txt
```

### 2) Split into 2×500 (deterministic; supports excluding already-processed IDs)

```bash
python scripts/split_paper_ids.py \
  --input analysis/oa1000/paper_ids_1200.txt \
  --exclude runs/oa_seq_peptide_fast_20260121_214200/paper_ids_200.txt \
  --exclude runs/oa_seq_peptide_fast_oa_inpmc_20260121_220445/paper_ids_200.txt \
  --parts 2 --per-part 500 --seed 20260122 \
  --out-dir analysis/oa1000/splits_2x500
```

This writes:
- `analysis/oa1000/splits_2x500/paper_ids_part_01.txt`
- `analysis/oa1000/splits_2x500/paper_ids_part_02.txt`
- `analysis/oa1000/splits_2x500/split.meta.json` (audit)

### 3) Run two independent pipelines (two Codex windows)

For long runs, prefer `tmux` so the job keeps running even if the Codex window/UI disconnects.

Window A:
```bash
python scripts/run_tox_paper_pipeline.py \
  --paper-ids analysis/oa1000/splits_2x500/paper_ids_part_01.txt \
  --out-root runs --run-name oa1000_part01_<timestamp> \
  --max-pdf-pages 10 \
  --download-timeout 60 --download-delay 0.4 --max-file-mb 600 --max-file-seconds 600 \
  --screen --screen-min-seq-len 8 --augment-methods --methods-taxonomy --summarize
```

Window B:
```bash
python scripts/run_tox_paper_pipeline.py \
  --paper-ids analysis/oa1000/splits_2x500/paper_ids_part_02.txt \
  --out-root runs --run-name oa1000_part02_<timestamp> \
  --max-pdf-pages 10 \
  --download-timeout 60 --download-delay 0.4 --max-file-mb 600 --max-file-seconds 600 \
  --screen --screen-min-seq-len 8 --augment-methods --methods-taxonomy --summarize
```

tmux example (Window A):
```bash
tmux new -d -s oa1000_part01 'bash -lc "cd /root/private_data/aa_peptide/toxin/docs && python scripts/run_tox_paper_pipeline.py --paper-ids analysis/oa1000/splits_2x500/paper_ids_part_01.txt --out-root runs --run-name oa1000_part01_<timestamp> --max-pdf-pages 10 --download-timeout 60 --download-delay 0.4 --max-file-mb 600 --max-file-seconds 600 --screen --screen-min-seq-len 8 --augment-methods --methods-taxonomy --summarize |& tee runs/oa1000_part01_<timestamp>/logs/pipeline.log"'
tmux attach -t oa1000_part01
```

### 4) Merge the two runs into one training dataset + splits

```bash
python scripts/build_union_dataset_and_splits.py \
  --run-dir runs/oa1000_part01_<timestamp> \
  --run-dir runs/oa1000_part02_<timestamp> \
  --out-dir analysis/splits_1000_<timestamp> \
  --seed 20260122
```

Notes on method labels:
- Current `method_*` fields are extracted mainly from JATS XML; many papers will remain missing/unknown because protocol details often live in PDFs/supp PDFs.
- For comparability benchmarks, prefer method-filtered strict tracks (e.g., MIC + broth microdilution + consistent medium/inoculum/incubation where available).

## Option C: LLM-assisted per-paper review (queue + multi-worker)

Use this when you want **paper-by-paper auditable extraction + QC** without multiple Codex windows writing the same file.

Prereq: you already have a run folder like `runs/<run_name>/papers/` with:
- `*.xml` / `*.pdf` / `supplementary/<PMCID>/...` as available
- `extracted_tables/*.csv` and `raw_experimental_records.csv` (from `extract_paper_extractions.py`)

### 1) Freeze a deterministic worklist (example: 30 papers)

```bash
python scripts/freeze_analysis_worklist.py \
  --papers-dir runs/<run_name>/papers \
  --n 30 \
  --out analysis/worklist_30.txt \
  --meta-out analysis/worklist_30.meta.json
```

### 2) Build a de-duplicated task queue (atomic claim via mv)

```bash
python scripts/build_analysis_queue.py \
  --worklist analysis/worklist_30.txt \
  --papers-dir runs/<run_name>/papers \
  --analysis-dir analysis_llm
```

Queue layout:
- `analysis_llm/queue/pending/*.json` (tasks)
- `analysis_llm/queue/in_progress/*.json` (claimed)
- `analysis_llm/queue/done/*.json` / `analysis_llm/queue/failed/*.json` (final)

### 3) Start N workers (recommended: tmux)

```bash
SANDBOX=read-only MODEL=gpt-5 bash scripts/start_analysis_workers_tmux.sh 3 analysis_workers analysis_llm
```

Deep mode (stronger “must open files” + worker-provided previews):

```bash
PROMPT_TEMPLATE=analysis/prompts/per_paper_prompt_deep.txt \
  SANDBOX=read-only MODEL=gpt-5 \
  bash scripts/start_analysis_workers_tmux.sh 3 analysis_workers analysis_llm_deep
```

Tune preview depth (optional): pass `--preview-tables/--preview-supp-files/--preview-lines` to `scripts/analysis_worker.py`.
When using the tmux starter, you can pass simple space-separated flags via `WORKER_ARGS` (no quotes), e.g. `WORKER_ARGS='--preview-tables 10 --preview-lines 30'`.

Or run a single worker in one terminal:

```bash
python scripts/analysis_worker.py --analysis-dir analysis_llm --sandbox read-only --mode codex --worker-name w1
```

### 4) Merge per-paper Markdown into a single summary

```bash
python scripts/merge_per_paper_md.py --analysis-dir analysis_llm --out analysis_llm/summary.md
```

Notes:
- Each paper writes **one file**: `analysis_llm/per_paper/PMCxxxx.json` and `analysis_llm/per_paper/PMCxxxx.md`.
- To re-run cleanly, prefer a new `--analysis-dir` (e.g., `analysis_llm_fix3/`) instead of mutating `done/`.

## Monitoring checklist (for the LLM / reviewer)

- Read `extraction_report.md` first; verify: (1) PDF/XML availability, (2) supplementary files count, (3) endpoint distribution, (4) papers with 0 experimental rows.
- For any “0 experimental rows” paper: open `extracted_tables/*.csv` and check if endpoints are in figures-only or in non-tabular supplements (PDF/image).
- If key endpoints are missing but the paper has tables: inspect whether endpoints are in captions/footnotes or use nonstandard tokens; then update extraction heuristics (keep it auditable).

## Practical heuristics: filling missing fields (sequence/unit/organism) without breaking “raw + auditable”

Principle: treat every “filled” value as *paper-local evidence*. Never infer a peptide sequence from a name; only fill `sequence` when the AA string is present in the OA XML/PDF/supp that you already have, and keep a source pointer for the mapping.

### 1) Recover missing `sequence` (conservative, traceable)

- Build a `peptide_id → sequence` map from `extracted_tables/<PMCID>_*.csv` by scanning for a “sequence” column (headers often include `sequence`, `aa sequence`, `amino acid`, `primary structure`). Handle multi-row headers: many PMC tables have 2–3 header rows where the “sequence” label is not in row 1.
- Standardize AA strings conservatively:
  - Uppercase; remove whitespace/hyphens; strip obvious chemistry tokens/modifications (`H2N-`, `-NH2`, `CONH-`) from the *sequence* field (keep the modified form in `notes`/raw text if needed).
  - Prefer the **longest** AA-like run rather than concatenating letter chunks (prevents `CONH` / `CH3` artifacts).
- Recover from JATS XML full text if tables don’t print sequences:
  - Search within `root.itertext()` around the peptide name for patterns like:
    - `… aminoacidic sequence GLLR…`
    - `sequence: GLLR…` / `sequence of GLLR…`
    - `PeptideName (GLLR…)`
  - Require explicit “sequence/aa sequence/…” context to avoid false positives: many English phrases/cell-line descriptions can be composed solely of AA letters. Maintain a denylist for obvious non-sequence markers (e.g., `HUMAN`, `CELL`, `CANCER`, `CONTROL`, `OIL`) and drop such matches.
- Supplementary material:
  - Prefer already-extracted `extracted_tables/*.csv` from the pipeline when present.
  - If the sequence only appears in supplementary PDFs/spreadsheets, extract it but always store `source.file + source.ref` with page/table/sheet + row/col coordinates (auditable).
- Always record `coverage.sequence_sources` entries when you add a sequence mapping (with a text excerpt pointer for “methods text” mappings).

### 2) Avoid “derived endpoints” while still extracting primary endpoints

- Do not treat SI/TI/% inhibition/ratio/index as endpoints. Skip derived columns/rows (e.g., `MBC/MIC index`, `selectivity index`, `therapeutic index`) and log them in QC (e.g., `excluded_derived_endpoint_rows`) instead of turning them into new endpoints.
- When a cell encodes two primary endpoints (e.g., `MIC/MBC = 8/16`), split into two records only when the header clearly indicates both endpoints; keep `value_text` raw and auditable.

### 3) Recover `organism_or_cell`, `condition`, and `unit` from messy tables

- Table orientation matters:
  - Detect whether peptides live in **rows** or **column headers** (common in MIC/MBC tables). If column headers carry peptide labels, treat row 1 as “organism/strain” and columns as peptides.
  - Use group rows (rows where most non-empty cells repeat the same organism) as “current organism” context.
- Units:
  - Prefer explicit units in column headers; fallback to caption/footnotes.
  - Normalize common OCR variants (`ug/ml`→`μg/mL`, `µM`→`μM`, `nm`→`nM`) but be conservative: ignore parentheses that don’t actually contain unit tokens (e.g., `ATCC 29213, …`) and avoid treating `100% MHB` as a `%` measurement unit.
  - If unit is ambiguous, leave it blank and log a QC note instead of guessing.

Hemolysis-specific pitfalls (common):
- If a cell looks like `37.00 (200 µM or 577.34 µg/mL)`: keep **hemolysis = 37.00 %** as the endpoint, and treat the concentration inside parentheses as **dose/condition** (do not create a second `HEMOLYSIS` endpoint in `µM`).
- For multi-row headers where one row is `Erythrocyte Lysis (%)` and another row is `Peptides (μM), 2, 4, 8, ...`: treat the numeric header row as **dose levels** (conditions), not hemolysis values.
- For `> 100` / `< 1` style values: keep censoring info explicitly (e.g., `cmp` field) instead of converting to an equal value.

### 4) External sequence alignment (UniProt / DBAASP) + provenance template

Use external databases only when:
1) `sequence` is still missing after scanning **paper-local** artifacts (XML/PDF/supp/extracted tables), and
2) you can keep the resolution **auditable** (accession/URL + downloaded response + timestamp + matching rationale).

Evidence tiers (preferred order):
- `paper_local` (same paper XML/PDF/supp) → fill directly, store source pointer.
- `corpus_local` (another already-downloaded OA paper in your local corpus) → fill with that paper’s pointer.
- `external_db` (UniProt/DBAASP/DRAMP/APD3/…) → fill only with strong linkage; otherwise keep blank and store candidates.

#### UniProt (recommended when paper provides an accession, or the peptide is a mature fragment of a precursor)

Minimal, auditable workflow:
- Extract identifiers from the paper text first (preferred): `UniProt`, `accession`, `PDB`, `GenBank`, `PRIDE`, etc.
- Download the exact UniProt entry you used and keep it as a local artifact (plus sha256).

Example commands (placeholders):
```bash
# Search (inspect top hits; fields list may change—verify against UniProt docs when needed)
curl -L 'https://rest.uniprot.org/uniprotkb/search?query=<QUERY>&format=json&size=5&fields=accession,id,protein_name,organism_name,length,sequence' \
  -o uniprot_search_<slug>.json
sha256sum uniprot_search_<slug>.json > uniprot_search_<slug>.json.sha256

# Retrieve a specific entry (preferred once you have an accession)
curl -L 'https://rest.uniprot.org/uniprotkb/<ACCESSION>.json' -o uniprot_<ACCESSION>.json
sha256sum uniprot_<ACCESSION>.json > uniprot_<ACCESSION>.json.sha256

# Optional: FASTA for quick viewing
curl -L 'https://rest.uniprot.org/uniprotkb/<ACCESSION>.fasta' -o uniprot_<ACCESSION>.fasta
sha256sum uniprot_<ACCESSION>.fasta > uniprot_<ACCESSION>.fasta.sha256
```

How to avoid wrong “precursor vs mature peptide” mappings:
- Prefer entries where the **paper itself cites the accession**.
- If the peptide is a fragment (venom toxin/defensin/cyclotide precursor): use UniProt `Features` to locate the mature `Peptide`/`Chain` region, and record the exact start/end coordinates you used.
- If multiple entries match the name: require additional agreement (organism, expected length, modifications, and/or paper-provided IDs). If still ambiguous, do **not** fill `sequence`; keep candidates.

#### DBAASP (and other AMP databases)

Pragmatic rule:
- Prefer official dataset exports (CSV/JSON) if you have them; otherwise treat web lookups as “manual” and keep auditable artifacts (saved HTML/JSON + URL + timestamp + sha256).
- Always check license/terms before using database-derived sequences for training or redistribution.

#### Provenance “落盘”模板（建议字段）

When you resolve a sequence externally, store the evidence as a structured record (per paper, per peptide_id). A minimal JSON template:
```json
{
  "sequence_resolution": {
    "status": "resolved|unresolved|ambiguous",
    "tier": "paper_local|corpus_local|external_db",
    "peptide_id": "<peptide label in the paper>",
    "selected": {
      "sequence": "<AA sequence (standardized)>",
      "source": {
        "kind": "text|xml_table|supplementary|external_db",
        "ref": "<human-auditable pointer>",
        "file": "<local path if applicable>",
        "url": "<external URL if applicable>"
      }
    },
    "candidates": [
      {
        "db": "uniprot|dbaasp|dramp|apd3",
        "accession": "<e.g., UniProt accession>",
        "entry_url": "<https://...>",
        "retrieved_at": "<ISO8601>",
        "artifact_file": "<local cached response file>",
        "artifact_sha256": "<sha256 of artifact_file>",
        "sequence": "<candidate sequence>",
        "feature": "<optional: mature peptide region + coords>",
        "match_rationale": "<why you believe this maps to the paper peptide>"
      }
    ],
    "notes": "<any uncertainty or excluded alternatives>"
  }
}
```

Operational convention:
- Only write `records[*].sequence` when `status=resolved` and the mapping is unambiguous; otherwise keep `records[*].sequence` empty and keep candidates in `qc`/`coverage` for later review.

# Notes

- Keep extraction “raw + auditable”; do not silently drop rows without recording a source pointer.
- Do not bypass paywalls or anti-bot protections; only download OA artifacts (use PMC OA packages when available).
