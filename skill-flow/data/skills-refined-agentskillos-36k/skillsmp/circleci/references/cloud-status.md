# Cloud Status and Logs (CircleCI API v2)

## Prereqs

- Export a token: `export CIRCLECI_CLI_TOKEN=...` (or pass `--token` to CLI/API calls).
- The helper script also reads `~/.circleci/cli.yml` (created by `circleci setup`).
- Get the Project ID from Project Settings -> Overview for `circleci pipeline list`.
- Get the project slug for API calls, e.g. `gh/org/repo` or `circleci/org/repo`.

## List pipelines (CLI)

```bash
circleci pipeline list "$PROJECT_ID"
```

Capture a pipeline ID from the output.

## List pipelines (script, no curl)

```bash
python3 scripts/cc_status.py pipelines gh/org/repo --limit 10
```

Add `--json` to print the raw API response:

```bash
python3 scripts/cc_status.py --json pipelines gh/org/repo --limit 10
```

## List workflows for a pipeline (API)

```bash
PIPELINE_ID=...
curl -s -H "Circle-Token: $CIRCLECI_CLI_TOKEN" \
  "https://circleci.com/api/v2/pipeline/$PIPELINE_ID/workflow" | \
  jq -r '.items[] | "\(.id) \(.name) \(.status)"'
```

## List jobs for a workflow (API)

```bash
WORKFLOW_ID=...
curl -s -H "Circle-Token: $CIRCLECI_CLI_TOKEN" \
  "https://circleci.com/api/v2/workflow/$WORKFLOW_ID/job" | \
  jq -r '.items[] | "\(.job_number) \(.name) \(.status)"'
```

## Fetch job details and step logs

```bash
PROJECT_SLUG=gh/org/repo
JOB_NUMBER=...
curl -s -H "Circle-Token: $CIRCLECI_CLI_TOKEN" \
  "https://circleci.com/api/v2/project/$PROJECT_SLUG/job/$JOB_NUMBER" > job.json

# Fetch step output logs.
jq -r '.steps[].actions[] | select(.output_url != null) | .output_url' job.json | \
  while read -r url; do
    curl -sL "$url"
  done
```

## Script shortcuts

```bash
python3 scripts/cc_status.py workflows "$PIPELINE_ID"
python3 scripts/cc_status.py jobs "$WORKFLOW_ID"
python3 scripts/cc_status.py job gh/org/repo "$JOB_NUMBER" --steps
```

JSON output:

```bash
python3 scripts/cc_status.py --json workflows "$PIPELINE_ID"
```

## Notes

- If `jq` is not available, replace with `python -m json.tool` or a small Python parser.
- Use `circleci open` to jump to the project in the browser when you want the UI view.
