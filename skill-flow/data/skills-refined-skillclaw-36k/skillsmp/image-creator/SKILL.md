---
name: image-creator
description: Create new container images in the my-images repo and wire them into the shared publish/dispatch workflows and reusable remote workflows.
---

# Image Creator

Use this skill when adding a brand-new image directory or wiring a new publish workflow. It focuses on build flows, remote reusable workflows, and dispatch wiring.

## Build/publish model (context)
- Universal workbench (`universal-workbench-docker/`) is the base; downstream images layer on top.
- Event-driven via `repository_dispatch`:
  - `universal-workbench-publish` → `universal-workbench-updated`.
  - Downstreams (e.g., `google-gemini-publish`, `openai-codex-publish`) listen, rebuild, then emit their own updates (e.g., `gemini-workbench-updated`, `openai-codex-workbench-updated`).
  - Runner workflows (e.g., `github-runner-publish-gemini`, `github-runner-publish-codex`) listen for those downstream update events.
- Keep downstream dispatch jobs named `trigger-downstreams`.
- Always include the `shared/` build context when building locally or in CI so helper scripts are available.

## Remote reusable workflow (shared)
- Most builds call `spigell/my-shared-workflows/.github/workflows/docker-build-release.yaml@main`.
- Required `secrets`: `gh-token: ${{ secrets.IMAGES_PUBLISH_TOKEN }}` (push to GHCR).
- Key inputs:
  - `image-name`: registry/image name suffix (e.g., `codex-binary`).
  - `context`: path to the image directory.
  - `version`: tag to push (often `vX.Y.Z` or the upstream version).
  - `build-args`: newline list of `KEY=VALUE`.
- Outputs: `version`, `sha-tag`, `digest` (commonly reused by dependent builds and dispatch payloads).

## Creating a new image
1) **Scaffold directory**: Create `<image-name>-docker/` (or similar). Add a `Dockerfile`, supporting files, and `README.md`. Base off an existing sibling if similar. Ensure the `Dockerfile` copies from `../shared` (include `shared/` context in builds).
2) **Update root README**: Add the image to the table with base and description.
3) **Add publish workflow** in `.github/workflows/<image>-publish.yaml`:
   - Triggers: `repository_dispatch` (listen to upstream event, e.g., `universal-workbench-updated`), `push` on the image path + workflow file, and `workflow_dispatch` inputs for manual tags.
   - If it depends on universal, add a `resolve-universal-tag` job using `.github/actions/resolve-ghcr-tag` (payload > manual input > latest GHCR).
   - Add a build job that `uses: spigell/my-shared-workflows/.github/workflows/docker-build-release.yaml@main` with `image-name`, `context`, `version`, and `build-args` (include upstream tags/digests as needed).
   - If another image depends on this one, add `trigger-downstreams` using `peter-evans/repository-dispatch@v3` to emit an update event (keep the job name `trigger-downstreams`).
4) **Secrets**: The workflow expects `IMAGES_PUBLISH_TOKEN` for GHCR pushes and dispatch.
5) **Dispatch wiring**: Choose an event name that downstream workflows will watch (pattern: `<image>-updated`). If this image depends on another, add a `repository_dispatch` trigger to listen to that upstream event.
6) **Versioning**: Prefer dynamic tag resolution and avoid static manifest JSON. When bumping tools in the new image, also update the workflow `version`/build args to match.

## Git remote and approvals
- Keep PR summaries noting new workflows, dispatch events, and any version bump rationale.
