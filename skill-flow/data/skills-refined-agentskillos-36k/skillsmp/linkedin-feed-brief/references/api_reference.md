# LinkedIn Feed Collection Reference

This reference backs the `linkedin-feed-brief` skill.

## Core selectors (best-effort)

- Post containers: `div.feed-shared-update-v2[data-urn]` (current), `div.occludable-update[data-urn]` (older)
- Feed scroll containers (debug): `main div.scaffold-finite-scroll`, `div.scaffold-finite-scroll__content`
- Permalink candidates: `a[href*="/feed/update/"]`
- Text candidates: `div.update-components-text`, `div.feed-shared-update-v2__description`, `span.break-words`
- Author candidates: `span.update-components-actor__name`, `a.update-components-actor__meta-link span[dir="ltr"]`

## Filtering rules (required)

Exclude if any of the following match:

- Label text equals `Promoted` (also accept common non-English equivalents, e.g., Korean UI labels)
- URN patterns:
  - `urn:li:inAppPromotion:*`
  - `urn:li:jobPosting:*`
  - `urn:li:aggregate:(urn:li:jobPosting:*...)`
- Obvious module text (only if you must fall back to text heuristics):
  - “Jobs recommended for you”
  - “See who’s hiring”
- Employment / job-change posts (do **not** count toward N):
  - Korean keywords (best-effort): `취업`, `이직`, `퇴사`, `입사`, `합류`, `새 직장`, `새 역할`, `새 직책`, `새 포지션`
  - English keywords (best-effort): “starting a new position”, “new role”, “I’m happy to share”, “I’m excited to share”, “joined”, “join … as”, “open to work”, “seeking opportunities”
  - Notes:
    - This filter is intentionally conservative; if LinkedIn UI changes, prefer updating selectors/snippets first.
    - When in doubt, exclude obvious “I joined / I resigned / I’m open to work” style posts rather than miscounting N.

## Fixed categories (suggested)

- AI/ Software Engineering
- Finance/ Economy
- Career
- Sales/ Marketing
- Essay
- StartUp
- Event
- ETC

## Troubleshooting

- If `browser_run_code` times out: avoid reading `root.innerText` for the whole post; only read targeted nodes.
- If extraction returns 0 posts: take a snapshot to confirm selectors, then click “New posts” and retry.
- If permalinks are missing: use `https://www.linkedin.com/feed/update/{URN}/` fallback.
