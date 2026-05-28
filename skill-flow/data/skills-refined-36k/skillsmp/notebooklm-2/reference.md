# NotebookLM Skill Reference

## Core commands

```bash
# Notebooks
nlm list
nlm list-featured
nlm create "Title"
nlm rm <notebook-id>
nlm analytics <notebook-id>

# Sources
nlm sources <notebook-id>
nlm add <notebook-id> <url|file|->
nlm discover-sources <notebook-id> "<query>"
nlm rm-source <notebook-id> <source-id>
nlm rename-source <source-id> "New Name"
nlm refresh-source <source-id>
nlm check-source <source-id>

# Notes
nlm notes <notebook-id>
nlm new-note <notebook-id> "Title"
nlm update-note <notebook-id> <note-id> "Content" "Title"
nlm rm-note <note-id>

# Chat / generation
nlm generate-chat <notebook-id> "Prompt"
nlm chat <notebook-id>
nlm chat-list
nlm generate-guide <notebook-id>
nlm generate-outline <notebook-id>
nlm generate-section <notebook-id>
nlm generate-magic <notebook-id> <source-ids...>
nlm generate-mindmap <notebook-id> <source-ids...>

# Content transformations
nlm summarize <notebook-id> <source-ids...>
nlm explain <notebook-id> <source-ids...>
nlm outline <notebook-id> <source-ids...>
nlm rephrase <notebook-id> <source-ids...>
nlm expand <notebook-id> <source-ids...>
nlm critique <notebook-id> <source-ids...>
nlm brainstorm <notebook-id> <source-ids...>
nlm verify <notebook-id> <source-ids...>
nlm study-guide <notebook-id> <source-ids...>
nlm faq <notebook-id> <source-ids...>
nlm briefing-doc <notebook-id> <source-ids...>
nlm mindmap <notebook-id> <source-ids...>
nlm timeline <notebook-id> <source-ids...>
nlm toc <notebook-id> <source-ids...>

# Audio / video
nlm audio-list <notebook-id>
nlm audio-create <notebook-id> "Instructions"
nlm audio-get <notebook-id>
nlm audio-download <notebook-id> [filename] --direct-rpc
nlm audio-share <notebook-id>
nlm audio-rm <notebook-id>

nlm video-list <notebook-id>
nlm video-create <notebook-id> "Instructions"
nlm video-download <notebook-id> [filename] --direct-rpc

# Artifacts
nlm artifacts <notebook-id>
nlm list-artifacts <notebook-id>
nlm create-artifact <notebook-id> <note|audio|report|app>
nlm get-artifact <artifact-id>
nlm rename-artifact <artifact-id> "New Title"
nlm delete-artifact <artifact-id>

# Sharing
nlm share <notebook-id>
nlm share-private <notebook-id>
nlm share-details <share-id>

# Other
nlm refresh
nlm feedback "Message"
nlm hb
```

## Auth + profiles

```bash
nlm auth --all --notebooks
NLM_USE_ORIGINAL_PROFILE=1 nlm auth --all --notebooks --debug
```

## Flags

```bash
nlm -debug list
nlm -debug-dump-payload list
nlm -debug-parsing list
nlm -debug-field-mapping list
nlm -chunked list
nlm -direct-rpc audio-download <notebook-id> out.mp3
nlm -skip-sources chat <notebook-id>
nlm add <notebook-id> file.xml -mime="text/xml"
```

## Environment variables

```bash
NLM_AUTH_TOKEN
NLM_COOKIES
NLM_BROWSER_PROFILE
NLM_USE_ORIGINAL_PROFILE=1

# Advanced overrides
NLM_BUILD_VERSION
NLM_SESSION_ID
```

## Safety

- Always confirm destructive ops: `rm`, `rm-source`, `rm-note`, `delete-artifact`, `audio-rm`
- Confirm privacy-impacting ops: `share` (public) and `share-private`

## Troubleshooting

- **Auth fails / no profiles found**: stop and ask the user to complete browser login manually, then retry:
  - `nlm auth --all --notebooks`
  - `NLM_USE_ORIGINAL_PROFILE=1 nlm auth --all --notebooks --debug`
