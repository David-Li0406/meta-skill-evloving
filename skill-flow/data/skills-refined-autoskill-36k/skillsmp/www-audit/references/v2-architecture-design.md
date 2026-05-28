Here is a specialist architecture redesign proposal for the `www-audit` skill.

# www-audit v2: Distributed Specialist Architecture

## 1. Specialist Roster (12 Specialists)
Moving from 7 to 12 specialists to reduce cognitive load and file size.

| Specialist | Type | Domain | Gist Responsibility | Screenshot Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **00. Orchestrator** | `System` | Workflow management | **Main Index Gist** | None (Aggregates) |
| **01. Photographer** | `Copilot` | Visual Capture | **Asset Gists** (Desktop/Mobile) | **Core Scrolls**: Full page every 900px, standard responsive breakpoints. |
| **02. Director** | `Copilot` | UX & Journey | `product-experience.md` | **Flows**: Multi-page navigation sequence, 404 page, success states. |
| **03. Visual Sys.** | `Copilot` | Color & Theme | `visual-system.md` | **Theme**: Dark/Light mode toggles, color contrast failures. |
| **04. Typography** | `Copilot` | Type & Hierarchy | `typography.md` | **Type**: Type scales, specific font rendering, webfont loading. |
| **05. Layout Eng.** | `Copilot` | Spacing & Grid | `layout-grid.md` | **Responsive**: Breakpoint behaviors, grid overlays, container shifts. |
| **06. Materials** | `Codex` | CSS & Effects | `materials-effects.md` | **Details**: Glassmorphism, shadows, border-radius, gradients, blend modes. |
| **07. Components** | `Codex` | UI Library | `component-library.md` | **States**: Inputs, buttons, cards, variants (primary/secondary). |
| **08. Motion** | `Copilot` | Animation | `motion-interaction.md` | **Timing**: Hover states, transition sequences, loading skeletons. |
| **09. Content** | `Copilot` | Copy & Voice | `content-voice.md` | **Microcopy**: Empty states, error messages, value props. |
| **10. Tech Lead** | `Codex` | Stack & Perf | `tech-performance.md` | **Network**: Waterfalls, bundle analysis, headers (no visual screenshots). |
| **11. Architect** | `Codex` | Data & Routing | `architecture-data.md` | **Structure**: CMS structure, state management diagrams (mermaid). |
| **12. Feature Lead** | `Copilot` | Deep Dives | `feature-[name].md` | **Complex UI**: Dedicated coverage for heavy features (e.g. Stem FM). |

**Estimated Gist Sizes:**
- Specialist Gists: 80-150 lines (highly focused).
- Main Index: 50-80 lines (summary).

---

## 2. Gist Architecture
**Total Gists per Audit**: 2 Asset Gists + 11-12 Specialist Gists + 1 Main Index = **~14-15 Gists**.

### Main AUDIT.md Structure (The "Index")
Designed to be read in < 2 minutes.
1.  **Header**: Project Name, URL, Date, Total Score.
2.  **Executive Summary**: 3-sentence overview of the vibe/tech.
3.  **Key Metrics Table**: Lighthouse, Page Count, Tech Stack.
4.  **Specialist Findings (Linked)**:
    *   **Visuals**: [Typography] | [Colors] | [Materials] | [Layout]
    *   **Experience**: [UX Journey] | [Motion] | [Content]
    *   **Engineering**: [Tech Stack] | [Architecture] | [Components]
5.  **Asset Links**: [Desktop Gallery] | [Mobile Gallery]

### Linking Strategy
*   **Central Asset Hub**: We keep the `Desktop` and `Mobile` screenshot gists as the "Database".
*   **Reference by URL**: All specialist gists reference images via raw GitHub user content URLs from the Asset gists.
*   **Cross-Linking**: Main gist links to Specialist gists. Specialist gists link back to Main.

---

## 3. Orchestration Workflow

### Phase 1: Capture (Sequential Start)
1.  **Photographer** launches first. Captures core desktop/mobile scrolls.
2.  **Output**: Creates 2 Asset Gists immediately.
3.  **Signal**: Returns Gist URLs to context.

### Phase 2: Analysis (Parallel Fan-out)
1.  **Launch**: Orchestrator spins up Specialists 02-12 in parallel (background processes).
2.  **Input**: Each specialist receives: Target URL + Phase 1 Asset Gist URLs.
3.  **Execution**:
    *   Specialists browse live site for deep analysis.
    *   Specialists capture *specific* interaction screenshots (hover, focus).
    *   **Crucial**: Specialists clone the Asset Gists, add their specific images, and push (using a mutex/lock or randomized filenames to avoid collision, or simply separate folders if using git).
    *   *Simpler Alternative*: Specialists upload their specific images to their *own* gist (if binary allowed) or a 3rd "Details" Asset Gist to avoid lock contention on the main ones.

### Phase 3: Reporting (Asynchronous Completion)
1.  **Draft**: Each specialist compiles their `domain.md`.
2.  **Publish**: Specialist creates Gist via `gh gist create`.
3.  **Return**: Specialist returns Gist URL and a "One-Line Summary" string to Orchestrator.

### Phase 4: Assembly
1.  **Aggregate**: Orchestrator waits for all processes.
2.  **Compile**: Generates `AUDIT.md` index using the returned summaries and URLs.
3.  **Finalize**: Updates the terminal/user with the single Main Gist URL.

---

## 4. Aggregation Strategy

### What goes in Main AUDIT.md?
*   **The "What"**: Site identity, purpose.
*   **The "Wow"**: Top 3 standout features (e.g., "Glassmorphism implementation is world-class").
*   **The "Ouch"**: Top 3 critical issues.
*   **Navigation**: The "Menu" of specialist links.

### What goes in Specialist Gists?
*   **Deep Tables**: Color hex codes, font family stacks, spacing ramp values.
*   **Code Snippets**: Actual CSS extracted by Codex.
*   **Contextual Images**: Screenshots of *just* the hover state or *just* the font rendering.
*   **Validation**: The checkbox tables for that specific domain.

---

## 5. Implementation Considerations

### CLI Patterns
*   **Gist Creation**: `gh gist create filename.md -d "Description" --public`
*   **Binary Handling**:
    *   *Current*: `git clone <gist_url>`, `cp img.png .`, `git add .`, `git commit`, `git push`.
    *   *Optimization*: Use a specialized `screen-capture` agent that handles the git operations centrally to prevent race conditions, receiving requests like `capture(selector, state)` from specialists.

### Validation Enforcement
*   **Pre-commit Hook (Agent side)**: Before an agent returns, it runs a self-check: "Did I include the validation table? Are there placeholders?"
*   **Orchestrator Check**: If a specialist returns a Gist URL but the summary is empty or an error occurred, the Orchestrator flags it in the Main Gist: "⚠️ Typography Audit Failed - Retry Available".

### Migration
*   Existing audits remain as monoliths.
*   New audits use v2 structure.
*   Add a `--format=v1|v2` flag to the skill for backward compatibility.

---

## 6. Example Decomposition: stemplayer.com

### Main `AUDIT.md` (Summary)
```markdown
# Audit: Stem Player
**Score**: 98/100 | **Stack**: Next.js, WebGL

## Executive Summary
A masterclass in tactile web design. The site uses a "fleshy" material system with unique
subsurface scattering effects. Navigation is unconventional (scroll-jacking).

## Specialist Deep Dives
### 🎨 Visuals
*   **[Materials & Effects](gist-url)**: Analysis of the custom WebGL skin shaders and glass overlays.
*   **[Typography](gist-url)**: Usage of 'Moderat' mono across 7 distinct scales.
*   **[Layout](gist-url)**: unconventional grid-less layout engine.

### 🕹️ Experience
*   **[Feature: Stem FM](gist-url)**: (260 lines) Deep breakdown of the remixer interface.
*   **[Motion](gist-url)**: Spring-physics analysis of the floating pucks.

## Assets
[Desktop Gallery (33 imgs)] | [Mobile Gallery (5 imgs)]
```

### Specialist Gist: `materials-effects.md`
```markdown
# Materials: Stem Player

## Core Material: "Synthetic Skin"
The primary texture is a generated noise pattern simulating silicone.
- **Opacity**: 0.95
- **Blur**: 40px backdrop-filter
- **Shadow**: Double-layer soft drop shadow `0 20px 40px rgba(0,0,0,0.1)`

## Validation
- [x] 0 Blank Screenshots
- [x] Dark Mode Tested (N/A)
```

### Specialist Gist: `feature-stem-fm.md`
```markdown
# Feature: Stem FM Player

## Interface Analysis
The player uses a 4-channel mixer layout...
[Screenshot: hover-state-channel-1.png]

## Interaction Model
- Dragging stems isolates audio channels.
- Elastic return on release.
```

