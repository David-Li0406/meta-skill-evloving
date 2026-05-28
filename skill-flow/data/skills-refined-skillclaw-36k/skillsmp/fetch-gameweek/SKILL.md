---
name: fetch-gameweek
description: Fetches FPL Draft gameweek data and serves it locally for verification. Use when the user asks to fetch gameweek data, update FPL data, or get the latest gameweek results. Does NOT deploy to production.
allowed-tools: Bash(python3:*), Read
---

# FPL Gameweek Fetcher & Local Server

Fetches gameweek data from FPL API and serves it locally for verification BEFORE deployment.

## Workflow

This skill follows a two-step workflow:
1. **This skill**: Fetch data → Serve locally → Verify
2. **deploy-gameweek skill**: Deploy to staging/production (separate)

## What This Skill Does

1. Runs `fetch_gameweek.py` with the specified gameweek number
2. Fetches data from FPL Draft API
3. Generates all required CSV files:
   - `final_results_gwX.csv` or `partial_results_gwX.csv`
   - `transfer_history.csv` (cumulative)
   - `players_gwX.csv` (round points)
   - `pl_gwX.csv` (Pacific timezone)
4. Copies static files: `fixture_list.csv`, `starting_draft.csv`, `draftdata25_26.xlsx`
5. **For final results only**: Generates summaries automatically:
   - Runs `generate_summary.py` to create `summary_gwX.csv`
   - Runs `generate_ai_summary.py` to create `ai_summary_gwX.md`
6. **Serves dashboard locally** at http://localhost:8000 for verification

## Usage Examples

### Fetch Final Results (After GW Finishes)
User: "Fetch gameweek 18"

I will:
- Fetch final results with actual scores
- Generate summaries automatically
- Serve locally for you to verify

### Fetch Partial Results (During GW)
User: "Fetch partial results for gameweek 18"

I will:
- Fetch current scores (or 0-0 if not started)
- Skip summary generation
- Serve locally for you to verify

### Update Mid-Week
User: "Update gameweek 18"

I will:
- Re-fetch current scores
- Update all CSV files
- Serve locally

## Commands I Execute

### For Final Results
```bash
python3 fetch_gameweek.py --gameweek <number>
python3 serve_dashboard.py
```

### For Partial Results
```bash
python3 fetch_gameweek.py --gameweek <number> --partial
python3 serve_dashboard.py
```

## After This Skill Runs

You should:
1. **Open browser**: http://localhost:8000
2. **Verify everything looks correct**:
   - Match results are accurate
   - Player stats make sense
   - PL fixture times are right
   - AI summary (for final results) is good
3. **If looks good**: Say "deploy gameweek X" to push to production
4. **If needs fixes**: Make manual edits and re-run this skill

## What Gets Generated

### Always Generated
- Match results CSV (final or partial)
- `transfer_history.csv` - All transfers (cumulative from API)
- `players_gwX.csv` - Round points for this gameweek
- `pl_gwX.csv` - PL fixtures in Pacific time

### Copied from Previous GW
- `fixture_list.csv` - League H2H fixtures
- `starting_draft.csv` - Draft order
- `draftdata25_26.xlsx` - Excel data file

### Generated for Final Results Only
- `summary_gwX.csv` - Gameweek summary data
- `ai_summary_gwX.md` - AI-generated roast summary

## Important Notes

- **Local verification first**: This skill does NOT deploy to production
- **Partial results**: Show 0-0 for matches that haven't started
- **Team names**: Always uses original names from `fpl_config.json`
- **Bearer token**: Must be valid in `.env` file (expires ~8 hours)
- **AI summaries**: Require Claude API key in `.env`

## Next Step

After verifying locally, use the **deploy-gameweek** skill to push to staging/production.
