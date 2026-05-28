# User Rating System Workflow

Allow users to rate artifacts after deployment to improve recommendations and personalize future suggestions.

---

## Overview

The rating system captures user feedback on artifact usefulness to:
- **Improve recommendations**: Boost highly-rated artifacts in future suggestions
- **Personalize results**: Weight user's own ratings more than community ratings
- **Track context**: Remember what tasks artifacts were useful for
- **Build trust**: Show aggregate ratings to help users decide

**Core Principles**:
- **Optional**: Rating is never required, always skippable
- **Contextual**: Capture task context when relevant
- **Non-intrusive**: Quick 1-5 star prompt, no lengthy forms
- **Actionable**: Ratings immediately affect future recommendations

---

## Rating Flow

### 1. Post-Deployment Prompt

After successful artifact deployment, prompt user for rating:

**Timing**: Immediately after deployment confirmation

**Template**:
```
✓ Successfully deployed {artifact-name}!

Location: .claude/{type}s/{artifact-name}/
Files created: {N}

Would you rate {artifact-name}? (1-5 stars, or Enter to skip)

[ 1 ] Not useful
[ 2 ] Somewhat useful
[ 3 ] Useful
[ 4 ] Very useful
[ 5 ] Essential

Rating: _
```

**Example**:
```
✓ Successfully deployed pdf-processor!

Location: .claude/skills/pdf-processor/
Files created: 3

Would you rate pdf-processor? (1-5 stars, or Enter to skip)

[ 1 ] Not useful
[ 2 ] Somewhat useful
[ 3 ] Useful
[ 4 ] Very useful
[ 5 ] Essential

Rating: 4
```

### 2. Capture Task Context (Optional)

After rating, optionally capture what task the artifact was used for:

**Prompt** (only if rating ≥ 3):
```
Great! What task are you using {artifact-name} for? (optional)

Examples: "document-processing", "data-extraction", "report-generation"

Task context: _
```

**Example**:
```
Great! What task are you using pdf-processor for? (optional)

Examples: "document-processing", "data-extraction", "report-generation"

Task context: document-processing
```

**Skip Condition**: Press Enter with empty input to skip

### 3. Store Rating

Store rating in collection manifest with metadata:

**Format** (manifest.toml):
```toml
[[artifacts]]
name = "pdf-processor"
type = "skill"
source = "anthropics/skills/document-skills/pdf@latest"
version = "latest"
scope = "user"

[artifacts.rating]
score = 4
rated_at = "2025-12-24T12:00:00Z"
context = "document-processing"  # optional
deployment_count = 1             # track how many times deployed
usage_count = 0                  # track how many times used (future)
```

**Fields**:
- `score` (1-5): User's rating
- `rated_at` (ISO 8601): When rating was given
- `context` (string, optional): Task context if provided
- `deployment_count` (int): How many projects artifact deployed to
- `usage_count` (int): How many times artifact used (tracked separately)

### 4. Confirmation

Confirm rating saved:

**Template**:
```
✓ Rating saved: {score}/5 stars{context_suffix}

Your rating will help improve future recommendations.

{artifact-name} is ready to use.
```

**Example** (with context):
```
✓ Rating saved: 4/5 stars for document-processing

Your rating will help improve future recommendations.

pdf-processor is ready to use.
```

**Example** (without context):
```
✓ Rating saved: 4/5 stars

Your rating will help improve future recommendations.

pdf-processor is ready to use.
```

---

## Re-Rating Artifacts

Users can update ratings later with `skillmeat rate` command.

### Rate Command

**Syntax**:
```bash
skillmeat rate <artifact-name> <score> [--context <context>]
```

**Examples**:
```bash
# Rate artifact
skillmeat rate pdf-processor 5

# Rate with context
skillmeat rate pdf-processor 5 --context document-processing

# Remove rating
skillmeat rate pdf-processor --clear
```

### Re-Rating Flow

**User**: `skillmeat rate pdf-processor 5`

**Workflow**:
```bash
# 1. Check if artifact exists
skillmeat show pdf-processor 2>/dev/null || {
  echo "Error: Artifact 'pdf-processor' not found in collection"
  exit 1
}

# 2. Validate score (1-5)
if [ $SCORE -lt 1 ] || [ $SCORE -gt 5 ]; then
  echo "Error: Score must be between 1 and 5"
  exit 1
fi

# 3. Update manifest.toml
# (implementation detail - update rating section)

# 4. Confirm
echo "✓ Rating updated: $SCORE/5 stars"
```

**Output**:
```
✓ Rating updated: 5/5 stars

Previous rating: 4/5 stars (updated 2 hours ago)
New rating: 5/5 stars

Your ratings help improve future recommendations.
```

### Clear Rating

**User**: `skillmeat rate pdf-processor --clear`

**Output**:
```
✓ Rating cleared for pdf-processor

Previous rating: 4/5 stars (given 2 hours ago)

You can rate again anytime: skillmeat rate pdf-processor <1-5>
```

---

## Viewing Ratings

### In Show Command

Display rating in `skillmeat show <artifact>` output:

**Example**:
```
pdf-processor (skill)

Source: anthropics/skills/document-skills/pdf@latest
Version: v1.2.0
Status: deployed to 1 project

Your rating: ★★★★☆ (4/5)
  Rated: 2 hours ago
  Context: document-processing

Community rating: ★★★★★ (4.7/5 from 127 users)

Description:
  Extract text and images from PDF documents
  ...
```

### In List Command

Show ratings in `skillmeat list` output:

**Example**:
```
User Collection (3 artifacts)

Skills:
  pdf-processor        ★★★★☆ (4/5)  - document-processing
  docx-processor       ★★★☆☆ (3/5)  - document-processing
  xlsx-processor       (not rated)

Deployed to current project:
  pdf-processor        ★★★★☆ (4/5)
```

### Filter by Rating

**Syntax**:
```bash
# Show highly-rated artifacts (≥4 stars)
skillmeat list --rated 4+

# Show unrated artifacts
skillmeat list --unrated

# Show rated artifacts (any rating)
skillmeat list --rated
```

**Example**:
```bash
skillmeat list --rated 4+
```

**Output**:
```
Highly-rated artifacts (4+ stars):

Skills:
  pdf-processor        ★★★★★ (5/5)  - document-processing
  canvas-design        ★★★★☆ (4/5)  - ui-design

2 artifacts rated 4+ stars
```

---

## Using Ratings in Recommendations

### Score Boosting Algorithm

Apply rating-based boost to recommendation confidence scores:

**Formula**:
```
boost_percent = (rating - 3) * 10%

Examples:
  5 stars → +20% boost
  4 stars → +10% boost
  3 stars → +0% (neutral)
  2 stars → -10% penalty
  1 star  → -20% penalty
```

**Implementation**:
```javascript
function applyRatingBoost(artifact, userRating, communityRating) {
  let boost = 0;

  // User's own rating (2x weight)
  if (userRating && userRating.score) {
    const userBoost = (userRating.score - 3) * 10;
    boost += userBoost * 2;  // 2x weight for personal ratings
  }

  // Community rating (1x weight)
  if (communityRating && communityRating.avg_score) {
    const communityBoost = (communityRating.avg_score - 3) * 10;
    boost += communityBoost * 1;  // 1x weight for community
  }

  // Normalize (max ±30%)
  boost = Math.max(-30, Math.min(30, boost));

  return artifact.confidence * (1 + boost / 100);
}
```

**Example**:
```
Base confidence: 70

User rating: 5 stars → +20%
Community rating: 4.5 stars → +15%

Combined boost: (20% * 2) + (15% * 1) = 55%
Normalized: 30% (capped)

Final confidence: 70 * 1.30 = 91
```

### Context-Based Recommendations

Use task context to recommend artifacts for similar tasks:

**User**: "I need to process Word documents"

**Workflow**:
```bash
# 1. Detect task context
TASK_CONTEXT="document-processing"

# 2. Find artifacts rated for similar context
MATCHING_ARTIFACTS=$(skillmeat list --rated --context "$TASK_CONTEXT" --json)

# 3. Boost artifacts with matching context (+10-15%)
```

**Recommendation**:
```
For document processing, you've previously rated:

  pdf-processor (5 stars) - "document-processing"
    ✓ Highly rated by you
    ✓ Similar task context

I also recommend:

  docx-processor (85% confidence)
    ≈ Similar to pdf-processor (which you rated 5 stars)
    ✓ Same task context: document-processing
    ✓ High quality - 450 GitHub stars

Would you like me to add docx-processor?
```

### Historical Success Tracking

Track deployment success rate to improve recommendations:

**Metrics** (stored in manifest):
```toml
[artifacts.rating]
score = 4
deployment_count = 3      # deployed to 3 projects
success_count = 3         # successfully used in all 3
last_used = "2025-12-24"  # most recent usage
```

**Success Rate**:
```
success_rate = success_count / deployment_count

Examples:
  3/3 = 100% → +10% boost
  2/3 = 67%  → +5% boost
  1/3 = 33%  → -5% penalty
  0/3 = 0%   → -10% penalty
```

**User Message**:
```
pdf-processor (92% confidence)
  ✓ You've used this 3 times with 100% success
  ✓ Average rating: 4/5 stars
  ✓ Last used: 2 hours ago
```

---

## Aggregate Ratings (Community)

### Local Ratings File

Store aggregate ratings separately from manifests:

**File**: `~/.skillmeat/ratings.toml`

**Format**:
```toml
[ratings.pdf-processor]
local_score = 4.0           # user's own rating
local_rated_at = "2025-12-24T12:00:00Z"
local_context = "document-processing"

community_score = 4.7       # community average (if available)
community_count = 127       # number of community ratings
community_updated = "2025-12-23T10:00:00Z"

[ratings.docx-processor]
local_score = 3.0
local_rated_at = "2025-12-23T08:00:00Z"
# No community data available
```

### Fetching Community Ratings

**Endpoint** (future): `GET /api/v1/ratings/{artifact-id}`

**Response**:
```json
{
  "artifact_id": "skill:pdf-processor",
  "avg_score": 4.7,
  "total_ratings": 127,
  "distribution": {
    "5": 85,
    "4": 30,
    "3": 8,
    "2": 3,
    "1": 1
  },
  "last_updated": "2025-12-23T10:00:00Z"
}
```

**Update Schedule**:
- Fetch when: User rates artifact, or explicit refresh request
- Cache for: 24 hours (local ratings.toml)
- Refresh: `skillmeat ratings refresh` (manual)

### Combining Local + Community Ratings

**Weighting**:
```javascript
function combineRatings(localRating, communityRating) {
  const localWeight = 2.0;     // User's own rating (2x)
  const communityWeight = 1.0; // Community rating (1x)

  if (localRating && communityRating) {
    // Both available - weighted average
    const weighted = (
      (localRating.score * localWeight) +
      (communityRating.avg_score * communityWeight)
    ) / (localWeight + communityWeight);
    return weighted;
  } else if (localRating) {
    // Only local rating
    return localRating.score;
  } else if (communityRating) {
    // Only community rating
    return communityRating.avg_score;
  }
  return null; // No ratings
}
```

**Example**:
```
Local: 5 stars (weight 2x)
Community: 4.5 stars (weight 1x)

Combined: ((5 * 2) + (4.5 * 1)) / 3 = 4.83 stars
```

**Display**:
```
pdf-processor

Your rating: ★★★★★ (5/5)
Community rating: ★★★★★ (4.7/5 from 127 users)
Combined: ★★★★★ (4.8/5)
```

---

## Rating Prompts and Timing

### When to Prompt

**DO prompt after**:
- First-time deployment of artifact
- Successful task completion using artifact
- Re-deployment after significant time (>30 days)

**DON'T prompt**:
- Multiple deployments in same session
- Artifact already rated recently (<7 days)
- User previously skipped rating (<24 hours)
- During error handling or debugging

### Prompt Frequency Limits

**Rate-limiting rules**:
```toml
[prompts.rating]
max_per_session = 3           # max 3 rating prompts per session
min_interval_hours = 24       # minimum 24h between prompts
skip_if_rated_days = 7        # skip if rated within 7 days
```

**Session Tracking** (in-memory):
```javascript
const sessionPrompts = {
  rating_prompts_shown: 0,
  last_rating_prompt: null,
  user_skipped: [],  // artifacts user skipped in this session
};

function shouldPromptRating(artifactName) {
  // Check session limits
  if (sessionPrompts.rating_prompts_shown >= 3) {
    return false;
  }

  // Check if user skipped in this session
  if (sessionPrompts.user_skipped.includes(artifactName)) {
    return false;
  }

  // Check if rated recently (from manifest)
  const rating = getRatingFromManifest(artifactName);
  if (rating && wasRatedRecently(rating.rated_at, 7)) {
    return false;
  }

  // Check interval between prompts
  if (sessionPrompts.last_rating_prompt) {
    const hoursSince = hoursSince(sessionPrompts.last_rating_prompt);
    if (hoursSince < 1) {  // at least 1 hour between prompts
      return false;
    }
  }

  return true;
}
```

### Skip Tracking

When user skips rating, record it:

**User**: `[Enter]` (skips rating)

**Workflow**:
```javascript
// Don't prompt again for this artifact in this session
sessionPrompts.user_skipped.push(artifactName);

// But allow prompting again in future sessions
// (no persistent skip tracking - user can always rate later)
```

**User Message**:
```
Skipped rating. You can rate later with:
  skillmeat rate pdf-processor <1-5>
```

---

## Rating Analytics

### Stats Command

**Syntax**:
```bash
# Show rating statistics
skillmeat ratings stats

# Show for specific artifact
skillmeat ratings stats pdf-processor

# Export ratings
skillmeat ratings export --format json
```

### Stats Output

**Global stats**:
```
Rating Statistics

Total artifacts rated: 8 / 15 (53%)
Average rating: 4.1/5 stars

Distribution:
  5 stars: ★★★★★ (3 artifacts)
  4 stars: ★★★★☆ (4 artifacts)
  3 stars: ★★★☆☆ (1 artifact)
  2 stars: ★★☆☆☆ (0 artifacts)
  1 star:  ★☆☆☆☆ (0 artifacts)

Most helpful artifacts:
  1. pdf-processor (5 stars) - used 12 times
  2. canvas-design (5 stars) - used 8 times
  3. docx-processor (4 stars) - used 5 times

Least helpful:
  1. old-tool (2 stars) - used 1 time
```

**Per-artifact stats**:
```
pdf-processor Rating Stats

Your rating: ★★★★★ (5/5)
  Rated: 2 days ago
  Context: document-processing

Usage:
  Deployed to: 3 projects
  Success rate: 100% (3/3)
  Last used: 2 hours ago

Community:
  Average: ★★★★★ (4.7/5)
  Total ratings: 127 users
  Distribution:
    5 stars: 67% (85)
    4 stars: 24% (30)
    3 stars: 6% (8)
    2 stars: 2% (3)
    1 star: 1% (1)
```

### Export Format

**JSON**:
```json
{
  "version": "1.0.0",
  "exported_at": "2025-12-24T12:00:00Z",
  "ratings": [
    {
      "artifact_id": "skill:pdf-processor",
      "name": "pdf-processor",
      "type": "skill",
      "rating": {
        "score": 5,
        "rated_at": "2025-12-22T10:00:00Z",
        "context": "document-processing"
      },
      "usage": {
        "deployment_count": 3,
        "success_count": 3,
        "last_used": "2025-12-24T10:00:00Z"
      },
      "community": {
        "avg_score": 4.7,
        "total_ratings": 127
      }
    }
  ]
}
```

**CSV**:
```csv
artifact_id,name,type,score,rated_at,context,deployments,success_rate
skill:pdf-processor,pdf-processor,skill,5,2025-12-22T10:00:00Z,document-processing,3,100%
skill:docx-processor,docx-processor,skill,4,2025-12-23T08:00:00Z,document-processing,2,100%
```

---

## Privacy and Data Collection

### What's Stored Locally

**Always stored locally** (manifest.toml, ratings.toml):
- User's own ratings (score, timestamp, context)
- Deployment count and success rate
- Last used timestamp

**Never sent to server** (without explicit opt-in):
- Individual ratings
- Task context
- Usage patterns

### What's Shared (Opt-in)

**Community ratings** (opt-in with `--share-ratings`):
- Anonymous rating score (1-5)
- Artifact ID
- Timestamp (rounded to day)
- NO personal identifiers
- NO task context

**Opt-in prompt**:
```
Help improve SkillMeat for everyone!

Share your ratings anonymously to help other users discover useful artifacts?

What will be shared:
  ✓ Rating score (1-5)
  ✓ Artifact ID
  ✓ Timestamp (day only)

What will NOT be shared:
  ✗ Your identity
  ✗ Task context
  ✗ Usage patterns
  ✗ Project details

Share ratings? (yes/no/later)
```

**Configuration**:
```toml
[config]
share_ratings = true  # or false
share_prompt_shown = "2025-12-24T12:00:00Z"
```

**Disable sharing**:
```bash
skillmeat config set share-ratings false
```

---

## Integration with Recommendation System

### Match API Integration

Ratings integrate with confidence scoring system (see `confidence-integration.md`):

**Request with ratings**:
```json
{
  "query": "pdf tools",
  "user_ratings": {
    "pdf-processor": {
      "score": 5,
      "context": "document-processing"
    }
  },
  "min_confidence": 70
}
```

**Response with rating boost**:
```json
{
  "matches": [
    {
      "artifact_id": "skill:pdf-processor",
      "confidence": 92.0,
      "breakdown": {
        "base_score": 80.0,
        "rating_boost": 20.0,  // +20% from 5-star rating
        "context_boost": 0.0,
        "trust_score": 95.0
      }
    }
  ]
}
```

### Recommendation Flow with Ratings

**User**: "Find PDF tools"

**Workflow**:
```bash
# 1. Get user's ratings
USER_RATINGS=$(skillmeat ratings export --format json)

# 2. Call match API with ratings
curl -X POST http://localhost:8080/api/v1/match \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"pdf tools\",
    \"user_ratings\": $USER_RATINGS,
    \"min_confidence\": 70
  }"

# 3. Present boosted results
```

**User Message**:
```
Based on your previous ratings, I recommend:

pdf-processor (92% confidence)
  ★★★★★ You rated this 5 stars for document-processing
  ✓ 100% success rate (used 3 times)
  ✓ Last used: 2 hours ago

This artifact is already in your collection. Would you like to:
- Deploy to this project?
- See other PDF tools?
```

---

## Example Flows

### Flow 1: First-Time Rating

**User**: "Add the PDF skill"

**Claude**:
```bash
# Deploy artifact
skillmeat add skill anthropics/skills/document-skills/pdf@latest
skillmeat deploy pdf-processor --project .
```

**Output**:
```
✓ Successfully deployed pdf-processor!

Location: .claude/skills/pdf-processor/
Files created: 3

Would you rate pdf-processor? (1-5 stars, or Enter to skip)

[ 1 ] Not useful
[ 2 ] Somewhat useful
[ 3 ] Useful
[ 4 ] Very useful
[ 5 ] Essential

Rating: _
```

**User**: `4`

**Claude**:
```
Great! What task are you using pdf-processor for? (optional)

Examples: "document-processing", "data-extraction", "report-generation"

Task context: _
```

**User**: `document-processing`

**Claude**:
```
✓ Rating saved: 4/5 stars for document-processing

Your rating will help improve future recommendations.

pdf-processor is ready to use.
```

### Flow 2: Skip Rating

**User**: "Add the canvas skill"

**Claude**:
```bash
skillmeat add skill anthropics/skills/canvas-design@latest
skillmeat deploy canvas-design --project .
```

**Output**:
```
✓ Successfully deployed canvas-design!

Location: .claude/skills/canvas-design/
Files created: 5

Would you rate canvas-design? (1-5 stars, or Enter to skip)

Rating: _
```

**User**: `[Enter]` (skips)

**Claude**:
```
Skipped rating. You can rate later with:
  skillmeat rate canvas-design <1-5>

canvas-design is ready to use.
```

### Flow 3: Update Existing Rating

**User**: "I want to change my PDF skill rating to 5 stars"

**Claude**:
```bash
skillmeat rate pdf-processor 5
```

**Output**:
```
✓ Rating updated: 5/5 stars

Previous rating: 4/5 stars (updated 2 days ago)
New rating: 5/5 stars

Would you like to update task context? (current: document-processing)

Task context: _
```

**User**: `[Enter]` (keep existing context)

**Claude**:
```
✓ Rating updated successfully

pdf-processor: ★★★★★ (5/5) - document-processing

Your ratings help improve future recommendations.
```

### Flow 4: Rating-Boosted Recommendation

**User**: "Find tools for processing Word documents"

**Claude**:
```bash
# 1. Detect task context
TASK_CONTEXT="document-processing"

# 2. Get user's ratings
USER_RATINGS=$(skillmeat ratings export --json)

# 3. Call match API
curl -X POST http://localhost:8080/api/v1/match \
  -d "{\"query\": \"word processing\", \"user_ratings\": $USER_RATINGS}"
```

**Response**:
```
Based on your previous ratings, I recommend:

docx-processor (89% confidence)
  ≈ Similar to pdf-processor (★★★★★ 5/5)
  ✓ Same task context: document-processing
  ✓ High quality - 450 GitHub stars
  ✓ Official Anthropic skill

You've previously rated:
  pdf-processor: ★★★★★ (5/5) - document-processing

Would you like me to add docx-processor?
```

### Flow 5: View Rating Stats

**User**: "Show my ratings"

**Claude**:
```bash
skillmeat ratings stats
```

**Output**:
```
Rating Statistics

Total artifacts rated: 8 / 15 (53%)
Average rating: 4.1/5 stars

Distribution:
  5 stars: ★★★★★ (3 artifacts)
  4 stars: ★★★★☆ (4 artifacts)
  3 stars: ★★★☆☆ (1 artifact)

Most helpful artifacts:
  1. pdf-processor (5 stars) - used 12 times, 100% success
  2. canvas-design (5 stars) - used 8 times, 100% success
  3. docx-processor (4 stars) - used 5 times, 100% success

Unrated artifacts: 7
```

---

## Best Practices

### When to Prompt

**DO prompt after**:
- Successful first-time deployment
- Successful task completion
- Re-deployment after long period (>30 days)

**DON'T prompt**:
- During errors or failures
- Multiple times per session
- If recently rated (<7 days)
- If user previously skipped (<24 hours)

### Frequency Limits

**Recommended limits**:
- Max 3 rating prompts per session
- Minimum 1 hour between prompts
- Skip if rated within 7 days
- Don't re-prompt if user skipped in same session

### User Experience

**DO**:
- Make rating optional (always allow skip)
- Explain why rating helps (improve recommendations)
- Show existing ratings (user's own + community)
- Use ratings to personalize future suggestions

**DON'T**:
- Require rating before use
- Prompt repeatedly for same artifact
- Hide how ratings are used
- Share ratings without explicit opt-in

### Privacy

**DO**:
- Store ratings locally by default
- Ask before sharing (opt-in)
- Explain what's shared and what's not
- Allow disabling sharing anytime

**DON'T**:
- Send ratings without permission
- Share personally identifiable information
- Share task context without opt-in
- Require sharing for features

---

## Reference

### CLI Commands

```bash
# Rate artifact (post-deployment)
# (automatic prompt after deployment)

# Rate/update rating manually
skillmeat rate <artifact> <1-5> [--context <context>]

# Clear rating
skillmeat rate <artifact> --clear

# View stats
skillmeat ratings stats [artifact]

# Export ratings
skillmeat ratings export [--format json|csv]

# Refresh community ratings
skillmeat ratings refresh

# Configure sharing
skillmeat config set share-ratings true|false
```

### Manifest Schema

```toml
[[artifacts]]
name = "artifact-name"
type = "skill|command|agent"
source = "source-path"

[artifacts.rating]
score = 4                              # 1-5 stars
rated_at = "2025-12-24T12:00:00Z"     # ISO 8601 timestamp
context = "task-context"               # optional task context
deployment_count = 3                   # times deployed
success_count = 3                      # successful deployments
last_used = "2025-12-24T10:00:00Z"    # last usage timestamp
```

### Ratings File Schema

```toml
[ratings.artifact-name]
local_score = 4.0                      # user's rating
local_rated_at = "2025-12-24T12:00:00Z"
local_context = "task-context"

community_score = 4.7                  # community average
community_count = 127                  # number of ratings
community_updated = "2025-12-23T10:00:00Z"
```

### Rating Boost Formula

```
boost_percent = (rating - 3) * 10%

Combined boost = (local_boost * 2) + (community_boost * 1)
Normalized boost = min(30%, max(-30%, combined_boost))

Final confidence = base_confidence * (1 + normalized_boost / 100)
```

### Related Files

- **Confidence Scoring**: `confidence-integration.md`
- **Deployment Workflow**: `deployment-workflow.md`
- **Manifest Format**: `../cli-reference.md`
- **Match API**: See SkillMeat API documentation
