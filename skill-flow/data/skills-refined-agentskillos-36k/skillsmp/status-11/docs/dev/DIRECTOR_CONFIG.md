Director tuning and local configuration

The Director used by the demo supports runtime tuning through a local configuration file at `.gengine/config.yaml`. Use `.gengine/config.example.yaml` as a template.

Supported keys:

- `directorConfig` (mapping): top-level director tuning entry. Contains:
  - `weights` (mapping): numeric weights for metrics (defaults shown below).
    - `proposal_confidence` (default 0.7)
    - `narrative_pacing` (default 0.15)
    - `return_path_confidence` (default 0.1)
    - `player_preference` (default 0.05)
    - `thematic_consistency` (default 0)
    - `lore_adherence` (default 0)
    - `character_voice` (default 0)
  - `pacingTargets` (mapping): expected lengths for narrative phases (defaults shown).
    - `exposition: 300`, `rising_action: 400`, `climax: 700`, `falling_action: 350`, `resolution: 300`
  - `pacingToleranceFactor` (number): default 0.6
  - `placeholderDefault` (number): default 0.3

Examples

Minimal override (change proposal confidence weight):

```yaml
# .gengine/config.yaml
directorConfig:
  weights:
    proposal_confidence: 0.6
```

Full example (copy from .gengine/config.example.yaml into .gengine/config.yaml and edit values)

Verification

1. Start the dev runner which logs when it loads `.gengine/config.yaml`:

   node scripts/dev-runner.js

2. Or quickly print the resolved Director config from Node at the repo root:

   node -e "console.log(JSON.stringify(require('./src/runtime/director-config.js'), null, 2))"

3. For browser/demo verification, start the demo server and open the demo UI; the Director will log telemetry events to console and buffer entries in `sessionStorage` (key `ge-hch.director.telemetry`). Changing `directorConfig` values should alter Director decisions in smoke tests or manual playthroughs.

Notes

- `.gengine/config.yaml` is intentionally git-ignored to avoid leaking secrets. Use `.gengine/config.example.yaml` to share recommended defaults.
- Environment variables may override specific director entries using the pattern `DIRECTOR_<SECTION>__<KEY>` (e.g., `DIRECTOR_WEIGHTS__PROPOSAL_CONFIDENCE=0.5`).
