# Meta-Skill Evolving

Evolve **meta-skills** — skill-library *management* methods (SkillX, AutoSkill,
SkillClaw, AgentSkillOS) written as agent-editable `SKILL.md` playbooks — with a
trajectory-informed loop:

```
manage a library → evaluate → attribute outcomes to management decisions
      → a Claude Code agent rewrites the meta-skill → repeat
```

Train and held-out sets are swappable between **SkillFlow** (~30K SKILL.md corpus,
executes SkillsBench tasks for reward) and **SkillRouter** (~80K skill pool,
retrieval metrics). Both derive ground truth from **SkillsBench**, so their tasks
overlap and only the skill pools differ — which is what makes them interchangeable.

This README is an **operational guide to reproduce the full experiment** (AutoSkill
over the entire 30,648-skill library × 74 SkillsBench tasks, 4 evolving iterations,
seed vs. evolved comparison with local SkillsBench execution).

---

## 1. The loop (`loop.py`)

```
meta = seed meta-skill (meta_skills/<method>/iter_0/SKILL.md)
for it in range(N):
    refined, decisions = manage(meta, train.pool)          # manage.py   -> decision log
    report             = evaluate(refined, train.tasks)    # evaluate.py -> retrieval (+ execution)
    attrib             = attribute(gold, decisions, report)# attribute.py-> blame / credit
    meta               = refine(meta, decisions, report, attrib, history)  # refine.py -> Claude Code
compare(best vs seed) on held_out                          # evolved vs. original
```

Two evaluation signals:

- **Retrieval proxy** (every iteration, cheap): embed the refined pool + each task
  instruction with BGE, cosine top-k. A ground-truth skill counts as *found* if its
  surviving representative is retrieved — itself if kept, or the merged skill that
  absorbed it. Scored with SkillRouter's `hit@k` / `recall@k`. The GT for a task is
  its SkillsBench **oracle skills** (`environment/skills/<name>/SKILL.md`), injected
  into the pool as `skillsbench/<task>/<name>`.
- **Execution reward** (≈ pass@1, expensive; only on the iterations in `exec_iters`,
  by default the seed and the final): inject each task's top-k refined skills and run
  the task in a **local Apptainer sandbox**; the hidden SkillsBench verifier scores
  the agent's output → reward ∈ [0,1].

A meta-skill `SKILL.md` carries YAML `params:` (mapped onto `RefinerConfig`) and
fenced prompt blocks the engines use:

```
<!-- PROMPT: merge -->
...jinja prompt the merge engine uses...
<!-- END PROMPT: merge -->
```

The whole file is the evolvable artifact the refiner edits (params + playbook + prompts).

---

## 2. Components

| File | Role |
|---|---|
| `data/schema.py` | unified `Skill / Task / SkillPool / GoldStandard / Dataset` |
| `data/skillrouter.py`, `data/skillflow.py` | dataset adapters (both → `Dataset`) |
| `data/subset.py` | GT-preserving ~N-skill subset for cheap smoke runs |
| `metaskill.py` | parse/load a meta-skill `SKILL.md` → `RefinerConfig` + prompt overrides |
| `meta_skills/<m>/iter_0/SKILL.md` | the 4 seed meta-skills |
| `manage.py` | run a meta-skill over a pool (reuses `skill_flow.refiner.refine_library`); emit a decision log; `prepare_source()` materializes + indexes the source library once |
| `evaluate.py` | retrieval proxy (GT→survivor mapping) + optional Apptainer execution |
| `execute.py` | **local** SkillsBench execution: inject refined top-k, run via the Apptainer backend, throttle-/resume-aware windows |
| `attribute.py` | join GT × decisions × outcomes → per-task blame/credit |
| `refine.py` | Claude Code (Opus, subscription) rewrites the meta-skill `SKILL.md` |
| `loop.py`, `cli.py` | orchestration + CLI (`loop` / `manage` / `compare`) |
| **operational / recovery scripts** | |
| `prefetch_sifs.py` | pre-pull each unique task base image once into a local **SIF cache** (see §4) |
| `regen_exec.py` | crash-safe **regeneration**: rebuild every iteration's refined library + run execution (resumable) |
| `rerun_failed.py` | re-run reward-0/None tasks (e.g. after a transient network outage) reusing the saved refined library |
| `posthoc_exec.py` | run execution for iterations that were retrieval-only |

---

## 3. Prerequisites (one-time)

```bash
cd /home/daweili5/meta-skill-evolving/skill-flow
export UV_PROJECT_ENVIRONMENT=/scratch/daweili5/skill-flow-venv UV_NO_SYNC=1

# .env supplies both auth paths:
#   OPENAI_API_KEY          -> AutoSkill management engines (judge / merge / filter)
#   CLAUDE_CODE_OAUTH_TOKEN  -> refiner (claude -p opus) AND the SkillsBench agent (subscription; NO API key)
set -a; source .env; set +a
```

- **Large data/models live under `/scratch/daweili5/`** (repo rule). The venv, source
  index, embeddings, SIF cache, and all run outputs go there.
- **Source library + index** (`data/skills-refined-36k` + `outputs/indices/bge-refined-36k`)
  must exist. The BGE index (`skill_contents.json`, `skill_ids.json`, …) is the fast
  path the loaders use instead of reading 30K files.
- **Apptainer** is the local execution backend (no Docker daemon / no Daytona). Verify:
  `apptainer --version` (tested on 1.4.5).

---

## 4. Local SkillsBench execution setup (Apptainer + SIF cache)

Execution runs SkillsBench tasks **locally** through the Apptainer harbor backend
(`benchmark/environments/apptainer.py`) — one writable sandbox per trial, agent +
verifier run via `apptainer exec --fakeroot`. Two things make this reliable at scale;
**do the SIF prefetch before any execution run**:

```bash
export APPTAINER_CACHEDIR=/scratch/daweili5/apptainer-cache
export APPTAINER_SIF_DIR=/scratch/daweili5/apptainer-sif
export HARBOR_APPTAINER_ROOT=/tmp/harbor-apptainer-metaskill

# Pull each unique task base image ONCE into the SIF cache (~11 images: ubuntu:24.04,
# python:3.x-slim, node, etc.). Task sandboxes then build from the local .sif with no
# registry access — immune to Docker Hub's anonymous pull-rate limit.
python -m meta_skill.prefetch_sifs
ls "$APPTAINER_SIF_DIR"/*.sif        # expect ~10–11 .sif files
```

Why this matters (learned the hard way):

- **Docker Hub anonymous pull limit** (100/6h) will fail *whole execution runs* once
  exhausted (`TOOMANYREQUESTS`, sometimes surfacing as a JSON parse error). The SIF
  cache pulls each image once; `benchmark/environments/apptainer.py:_base_image_source`
  builds sandboxes from the local `.sif` thereafter.
- **Apptainer OCI cache corruption**: apptainer corrupts its own cache index once it
  accumulates blobs across pulls, then fails *every* later pull with
  `invalid character 's' after top-level value`. `prefetch_sifs.py` uses a **fresh
  throwaway `APPTAINER_CACHEDIR` per pull** to avoid it. If you ever see that error,
  `rm -rf /scratch/daweili5/apptainer-cache && mkdir -p` it.
- Only Docker Hub works as a registry on this host; quay.io / ECR trip the parse bug,
  so `prefetch_sifs.py` retries Docker Hub images generously and bails fast on others.

---

## 5. Run the full experiment

Config: `meta_skill/config/evolve_autoskill_full.json`
(engine `autoskill`, full `skills-refined-36k` = 30,648 skills, all 74 tasks, 4
iterations, refiner `opus`, execution on the seed + final iteration only).

```bash
cd /home/daweili5/meta-skill-evolving/skill-flow
set -a; source .env; set +a
export APPTAINER_CACHEDIR=/scratch/daweili5/apptainer-cache \
       APPTAINER_SIF_DIR=/scratch/daweili5/apptainer-sif \
       HARBOR_APPTAINER_ROOT=/tmp/harbor-apptainer-metaskill

# long run (hours): manage 30K -> evaluate -> attribute -> refine, x4, with execution
# on iter_0 and the final iteration. Runs in the foreground; use nohup + & for background.
nohup /scratch/daweili5/skill-flow-venv/bin/python -u -m meta_skill.cli loop \
  --config meta_skill/config/evolve_autoskill_full.json \
  > /scratch/daweili5/meta_skill_evolve/autoskill_full.log 2>&1 &
```

The loop **checkpoints per iteration** (skips an iteration whose `eval_report.json`
already exists) and caches aggressively: source corpus/index built once
(`work_root/_source`), routing-text embeddings once (`work_root/emb_cache.npz`), and
the engine LLM judge/merge/filter caches shared across iterations
(`work_root/_caches`). `work_root` defaults to `/tmp` for speed.

> **Important — `/tmp` is reaped.** The refined libraries and execution job dirs live
> under `work_root` (`/tmp/...`) and are deleted after a few days of inactivity. The
> small durable artifacts (metrics, decision logs, evolved meta-skills) are on
> `/scratch` and survive. If you need to re-run execution after a gap, use the
> resumable regeneration in §7 — it rebuilds the refined libraries from the surviving
> caches on `/scratch`.

### Smaller runs

```bash
# tiny smoke: SkillX, 200-skill subset, 2 iterations, retrieval + 2 apptainer tasks
python -m meta_skill.cli loop   --config meta_skill/config/smoke_skillx.json
python -m meta_skill.cli manage --config meta_skill/config/smoke_skillx.json  # one management pass
```

---

## 6. Running the baseline (native) skill-management methods

The meta-skills wrap the **native skill-flow refiner engines** (`skill_flow/refiner/`).
Run any management method directly — this is the baseline the evolving loop starts
from. Each is a 3-step pipeline: **refine (manage) → pipeline (retrieve) → evaluate
(execute on SkillsBench)**.

### Step 1 — refine the library (choose the engine)

`skill_flow.cli refine` takes a standalone `RefinerConfig` JSON whose `engine` field
selects the method: `skillx` | `autoskill` | `skillclaw` | `agentskillos`.

```bash
# minimal RefinerConfig (autoskill shown; swap "engine" for the others)
cat > /tmp/refine_autoskill.json <<'JSON'
{
  "engine": "autoskill",
  "source_corpus_dir": "data/skills-refined-36k",
  "source_index_dir":  "outputs/indices/bge-refined-36k",
  "output_corpus_dir": "data/skills-refined-autoskill-36k",
  "report_dir":        "outputs/refiner/autoskill-36k",
  "autoskill": { "similarity_threshold": 0.85, "top_k": 10 }
}
JSON

python -m skill_flow.cli refine --config /tmp/refine_autoskill.json
# prints before/after counts, merges, drops; writes the refined corpus + summary.json
# override paths without editing the JSON: --source-corpus-dir / --source-index-dir /
#   --output-corpus / --report-dir
```

Engine knobs (fields of `RefinerConfig`; each engine ignores fields it doesn't use):

| engine | strategy | key params (defaults) |
|---|---|---|
| `skillx` | cluster → LLM-merge → quality-filter | `eps` (0.10, DBSCAN), `merger.max_group_size` (15) |
| `autoskill` | pairwise near-duplicate dedup + merge | `autoskill.similarity_threshold` (0.85), `autoskill.top_k` (10) |
| `skillclaw` | evolve + verify merges | `skillclaw.max_group_size` (5), `skillclaw.verify_min_score` (0.5) |
| `agentskillos` | hierarchical labeling tree | `agentskillos.n_categories` (32), `active_per_leaf` (0 = keep all) |

Management LLM calls use `OPENAI_API_KEY` (default model `gpt-4o-mini`).

### Step 2 — retrieve per task over the refined corpus

Build the per-task top-k "result cache" the benchmark injects, by running the SkillFlow
retrieval pipeline over the refined corpus:

```bash
python -m skill_flow.cli pipeline \
  --tasks-dir integration/skillsbench/tasks \
  --output-dir outputs/pipeline/autoskill_36k_paper74
# writes result_cache.json (task -> selected skill keys) used as the benchmark selector_cache
```

### Step 3 — evaluate on SkillsBench (local Apptainer)

Ready-made benchmark configs wire each method's refined corpus + result cache to the
Apptainer backend. **Prefetch SIFs first (§4).**

```bash
python -m benchmark.scripts.cli run \
  --config benchmark/config/apptainer_autoskill_36k_claude.json
```

Conditions (`benchmark/config/apptainer_<name>_36k_claude.json`):

| config `<name>` | condition |
|---|---|
| `vanilla` | no skills injected (lower bound) |
| `baseline` | unrefined full 36k library retrieval |
| `oracle` | ground-truth SkillsBench skills injected (upper bound) |
| `skillx` / `autoskill` / `skillclaw` / `agentskillos` | that method's refined library |

Each config points at its `corpus_dir` (e.g. `data/skills-refined-autoskill-36k`) and
`selector_cache` (the Step-2 `result_cache.json`); rewards land under `jobs_dir`
(`outputs/evaluation/...`). Compare two runs with
`python -m analysis.comparison.compare_runs RUN_A RUN_B`.

> **Meta-skill vs. baseline.** The evolving loop (§5) drives these same engines through
> `manage.py` (parameterized by a meta-skill `SKILL.md` instead of a `RefinerConfig`
> JSON) and adds the retrieval proxy + attribution + refiner on top. Iteration 0 of a
> meta-skill reproduces the corresponding baseline engine's behavior.

---

## 7. Outputs & building the comparison table

Everything durable lands under `output_dir` (`/scratch/daweili5/meta_skill_evolve/autoskill_full/`):

```
iter_<n>/decision_log.json     # management trajectory (cluster / merge / keep / filter)
iter_<n>/eval_report.json      # retrieval metrics + per-task top-k (+ execution if run)
iter_<n>/attribution.json      # per-task blame/credit
meta_iter_<n>.md               # the evolved meta-skill produced after iteration n-1
history.json                   # per-iteration score + metrics + blame
result.json                    # history + best-so-far + method
```

Read the 4-way table (params · retrieval · reward) straight from the reports:

```bash
python - <<'PY'
import json, re
from pathlib import Path
OUT = Path("/scratch/daweili5/meta_skill_evolve/autoskill_full")
metas = {"iter_0":"meta_skill/meta_skills/autoskill/iter_0/SKILL.md",
         "iter_1":OUT/"meta_iter_1.md","iter_2":OUT/"meta_iter_2.md","iter_3":OUT/"meta_iter_3.md"}
def p(m):
    t=Path(m).read_text(); s=re.search(r'similarity_threshold:\s*([\d.]+)',t); k=re.search(r'top_k:\s*(\d+)',t)
    return (s and s.group(1), k and k.group(1))
for n in metas:
    # prefer eval_report_regen.json (uniform re-run) if present, else eval_report.json
    f = OUT/n/"eval_report_regen.json"
    f = f if f.exists() else OUT/n/"eval_report.json"
    d=json.loads(f.read_text()); rm=d["retrieval"]["metrics"]; em=d.get("execution",{}).get("metrics",{})
    thr,tk=p(metas[n])
    print(f"{n}: thr={thr} top_k={tk} | hit@1={rm['hit@1']:.3f} recall@10={rm['recall@10']:.3f} "
          f"| reward={em.get('mean_reward')} ({em.get('n_scored')}/{em.get('n_tasks')})")
PY
```

### Result of the reference run (AutoSkill, 30,648 skills, 74 tasks)

| Meta-skill | params (thr / top_k) | hit@1 | recall@10 | reward (pass@1) | scored |
|---|---|---|---|---|---|
| iter_0 (seed)     | 0.85 / 10 | 0.581 | 0.681 | 0.481 | 65/74 |
| iter_1            | 0.92 / 5  | 0.541 | 0.663 | 0.497 | 65/74 |
| iter_2            | 0.90 / 8  | 0.554 | 0.656 | 0.486 | 65/74 |
| iter_3 (final)    | 0.92 / 8  | 0.541 | 0.656 | 0.463 | 65/74 |

Takeaways: the refiner tuned `similarity_threshold` up (fewer merges) and adjusted
`top_k`; the **retrieval proxy dipped slightly** while **execution reward stayed flat
(~0.46–0.50)** — evolution neither helped nor hurt end-task success on this library.
9 of 74 tasks never score under any meta-skill (genuinely hard: `lean4-proof`,
`manufacturing-*`, `crystallographic-*`, …). Retrieval rank and end-task success do
**not** move together — which is exactly why both signals are tracked.

---

## 8. Recovery / reproducibility (resumable regeneration)

If `/tmp` was reaped, the refined libraries are gone but the `/scratch` durable state
(decision logs, evolved meta-skills, and — under `regen_persist/` — the source index,
embeddings, and the judge/merge/filter caches) survives. `regen_exec.py` faithfully
rebuilds each iteration's refined library from those caches (**no new management LLM
calls** — everything is cached) and runs execution. It is crash/teardown-safe:
everything on `/scratch`, checkpoint after management, execution resumes at per-task
granularity.

```bash
set -a; source .env; set +a
export APPTAINER_CACHEDIR=/scratch/daweili5/apptainer-cache \
       APPTAINER_SIF_DIR=/scratch/daweili5/apptainer-sif \
       HARBOR_APPTAINER_ROOT=/tmp/harbor-apptainer-metaskill

python -m meta_skill.prefetch_sifs                 # ensure SIF cache is populated first
python -m meta_skill.regen_exec                    # all 4 (seed + iter_1/2/3); or pass e.g. `3`
# writes iter_<n>/eval_report_regen.json; touches REGEN_DONE when finished
```

If a **transient network outage** (e.g. the Ubuntu apt mirror) breaks some sandbox
builds during a run, those tasks score 0 from a broken environment. Re-run just the
affected tasks once the network is back — it reuses the already-rebuilt refined library
and only re-runs reward-0/None tasks:

```bash
python -m meta_skill.rerun_failed                  # all iters; or pass e.g. `3` for one
```

> Long background runs can be killed at session/host boundaries. Because every phase
> checkpoints to `/scratch`, just relaunch the same command — management is served from
> cache and execution resumes per task. Check state with:
> `ps -ef | grep regen_exec` and `cat /scratch/daweili5/meta_skill_evolve/regen_exec.log`.

---

## 9. Swapping train / held-out (SkillFlow ↔ SkillRouter)

`config/evolve_skillx.json` sets `train=skillflow`, `held_out=skillrouter`. The
SkillRouter pool needs its shards:

```bash
bash /scratch/daweili5/SkillRouter/scripts/download_eval_data.sh
```

Swap the two blocks to train on SkillRouter and hold out SkillFlow/SkillsBench.

---

## 10. Gotchas checklist

- **Run `prefetch_sifs.py` before any execution** — otherwise Docker Hub rate limits
  fail the run.
- **Apptainer cache corruption** (`invalid character 's' after top-level value`): wipe
  `/scratch/daweili5/apptainer-cache`.
- **`/tmp` is reaped** after a few days — durable artifacts are on `/scratch`; use
  `regen_exec.py` to recover refined libraries.
- **Transient apt/network outages** break sandbox builds → tasks score 0; re-run with
  `rerun_failed.py` once connectivity is back. A clean-1.0→0.0 flip across unrelated
  tasks is the signature of an infra failure, not skill quality.
- **Auth**: management engines use `OPENAI_API_KEY`; the refiner and the SkillsBench
  agent use the Claude Code **subscription** (`CLAUDE_CODE_OAUTH_TOKEN`, no API key).
  The OAuth token is refreshed automatically before each execution window.
- **Machine placement** (repo convention): API/agent calls run on Machine A (this box);
  GPU tuning/inference goes to the GitHub Actions self-hosted runner. Meta-skill
  evolving is all API/agent — keep it on Machine A.
```
