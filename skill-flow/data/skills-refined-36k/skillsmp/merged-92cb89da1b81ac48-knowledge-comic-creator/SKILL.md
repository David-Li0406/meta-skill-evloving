---
name: knowledge-comic-creator
description: Use this skill when you want to create original educational comics with detailed panel layouts and multiple art styles and tones.
---

# Knowledge Comic Creator

Create original knowledge comics with flexible art style and tone combinations.

## Usage

```bash
/comic posts/turing-story/source.md
/comic  # then paste content
```

## Options

| Option | Values |
|--------|--------|
| `--art` | ligne-claire (default), manga, realistic, ink-brush, chalk, classic, dramatic, warm, sepia, vibrant, ohmsha, wuxia, shoujo, or custom description | Art style / rendering technique |
| `--tone` | neutral (default), warm, dramatic, romantic, energetic, vintage, action | Mood / atmosphere |
| `--layout` | standard (default), cinematic, dense, splash, mixed, webtoon | Panel arrangement |
| `--aspect` | 3:4 (default, portrait), 4:3 (landscape), 16:9 (widescreen) | Page aspect ratio |
| `--lang` | auto (default), zh, en, ja, etc. | Output language |

Art Style × Tone × Layout can be freely combined. Incompatible combinations work but may produce unexpected results.

## Auto Selection

Content signals determine default art + tone + layout (or preset):

| Content Signals | Art Style | Tone | Layout | Preset |
|-----------------|-----------|------|--------|--------|
| Tutorial, how-to, beginner | manga | neutral | webtoon | **ohmsha** |
| Computing, AI, programming | manga | neutral | dense | **ohmsha** |
| Pre-1950, classical, ancient | realistic | vintage | cinematic | - |
| Personal story, mentor | ligne-claire | warm | standard | - |
| Conflict, breakthrough | (inherit) | dramatic | splash | - |
| Wine, food, business, lifestyle | realistic | neutral | cinematic | - |
| Martial arts, wuxia, xianxia | ink-brush | action | splash | **wuxia** |
| Romance, love, school life | manga | romantic | standard | **shoujo** |
| Biography, balanced | ligne-claire | neutral | mixed | - |

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/merge-to-pdf.ts` | Merge comic pages into PDF |

## File Structure

Output directory: `comic/{topic-slug}/`
- Slug: 2-4 words kebab-case from topic (e.g., `alan-turing-bio`)
- Conflict: append timestamp (e.g., `turing-story-20260118-143052`)

**Contents**:
- `source-{slug}.{ext}` - Source files
- `analysis.md` - Content analysis
- `storyboard.md` - Storyboard with panel breakdown
- `characters/characters.md` - Character definitions
- `characters/characters.png` - Character reference sheet
- `prompts/NN-{cover|page}-[slug].md` - Generation prompts
- `NN-{cover|page}-[slug].png` - Generated images
- `{topic-slug}.pdf` - Final merged PDF

## Workflow

### Step 1: Analyze Content → `analysis.md`

Read source content, save it if needed, and perform deep analysis.

**Actions**:
1. **Save source content** (if not already a file):
   - If user provides a file path: use as-is
   - If user pastes content: save to `source.md` in target directory
2. Read source content
3. **Deep analysis** following `references/analysis-framework.md`:
   - Target audience identification
   - Value proposition for readers
   - Core themes and narrative potential
   - Key figures and their story arcs
4. Detect source language
5. **Determine language**:
   - If EXTEND.md has `language` → use it
   - Else if `--lang` option provided → use it
   - Else → use detected source language
6. Determine recommended page count:
   - Short story: 5-8 pages
   - Medium complexity: 9-15 pages
   - Full biography: 16-25 pages
7. Analyze content signals for art/tone/layout recommendations
8. **Save to `analysis.md`**

### Step 2: Generate Storyboard + Characters

Create storyboard and character definitions using the confirmed style from Step 1.

1. **Storyboard** (`storyboard.md`):
   - YAML front matter with art_style, tone, layout, aspect_ratio
   - Cover design
   - Each page: layout, panel breakdown, visual prompts
   - **Written in user's preferred language**

2. **Character definitions** (`characters/characters.md`):
   - Visual specs matching the art style (in user's preferred language)
   - Include Reference Sheet Prompt for later image generation

### Step 3: User Confirmation

Present options for storyboard variant, visual style, language, and aspect ratio. Update files based on user selections.

### Step 4: Generate Images

With confirmed storyboard + art style + tone + aspect ratio:

1. Save prompt to `prompts/NN-{cover|page}-[slug].md` (in user's preferred language)
2. Generate image using confirmed art style and tone guidelines
3. Report progress after each generation

### Step 5: Merge to PDF

After all images generated:

```bash
npx -y bun ${SKILL_DIR}/scripts/merge-to-pdf.ts <comic-dir>
```

Creates `{topic-slug}.pdf` with all pages as full-page images.

### Step 6: Completion Report

```
Comic Complete!
Title: [title] | Art: [art] | Tone: [tone] | Pages: [count] | Aspect: [ratio] | Language: [lang]
Location: [path]
✓ analysis.md
✓ characters.png
✓ 00-cover-[slug].png ... NN-page-[slug].png
✓ {topic-slug}.pdf
```

## Page Modification

Support for modifying individual pages after initial generation.

### Edit Single Page

Regenerate a specific page with modified prompt.

### Add New Page

Insert a new page at specified position.

### Delete Page

Remove a page and renumber.

## Style-Specific Guidelines

### Ohmsha Style (`--style ohmsha`)

Additional requirements for educational manga:
- Use Doraemon characters directly unless custom characters are requested.
- Must use visual metaphors (gadgets, action scenes) - NO talking heads.

## References

Detailed templates and guidelines in `references/` directory:
- `analysis-framework.md` - Deep content analysis for comic adaptation
- `character-template.md` - Character definition format and examples
- `storyboard-template.md` - Storyboard structure and panel breakdown
- `ohmsha-guide.md` - Ohmsha manga style specifics

## Extension Support

Custom styles and configurations via EXTEND.md.

**Check paths** (priority order):
1. `.content-gen-skills/comic/EXTEND.md` (project)
2. `~/.content-gen-skills/comic/EXTEND.md` (user)

If found, load before Step 1. Extension content overrides defaults.