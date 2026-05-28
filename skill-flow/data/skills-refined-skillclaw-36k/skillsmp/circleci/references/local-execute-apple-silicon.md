# Local Execute on Apple Silicon

## Preconditions

- Use the Docker executor only. `circleci local execute` does not support `machine` or `macos`.
- Enable Docker Desktop "Use Rosetta for x86/amd64 emulation" on Apple Silicon.
- Prefer amd64 containers to match CircleCI cloud images.

## Process config (expand orbs and params)

```bash
circleci config process .circleci/config.yml > /tmp/circleci.processed.yml
```

If you use private orbs or pipeline parameters, include `--org-slug` or `--pipeline-parameters` as needed.

## Run a job with amd64 emulation

```bash
DOCKER_DEFAULT_PLATFORM=linux/amd64 \
  circleci local execute -c /tmp/circleci.processed.yml <job-name>
```

## Troubleshooting

- If a specific Docker image is multi-arch and supports arm64, you can set `DOCKER_DEFAULT_PLATFORM=linux/arm64` instead.
- If the job mounts the repo incorrectly, add `--volume "$PWD:/repo"` and set the working directory in the job.
- If you see a Docker platform error, confirm Rosetta emulation is enabled and restart Docker Desktop.
