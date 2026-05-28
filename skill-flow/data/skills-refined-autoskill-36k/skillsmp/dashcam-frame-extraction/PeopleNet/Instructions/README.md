# PeopleNet – Net‑New Park_F / Park_R Pipeline (Verifier Instructions)

Follow these steps in order. After each part, return the requested “Checkpoint” outputs so I can verify quickly before you proceed.

Index
- 01-discovery.md: find sources and build net‑new list
- 02-stage.md: stage locally with ≥20GB free‑space guard
- 03-gpu-guard.md: ensure GPU free VRAM ≥2GB before runs
- 04-ds-config.md: prepare PeopleNet DeepStream config/engine
- 05-run-video.md: run one video, produce detection CSV
- 06-orchestrate.md: loop over pending with disk/GPU guards
- 07-consolidate.md: merge per‑video CSVs + update central log
- 08-qc-preview.md: optional annotated previews
- 09-report.md: final stats to return for verification

Prerequisites
- DeepStream + TensorRT installed and working with PeopleNet engine (FP16 recommended).
- Windows partition mounted read‑only (CARDV folder containing Park_F and Park_R).
- Project root: `/home/yousuf/PROJECTS/PeopleNet/`
- Create folders if missing:
  - `state/`, `staging/videos/`, `Outputs/videos/`, `logs/`, `configs/`


