# File Organization - Scratchpad → History Pattern

## Working Directory (Scratchpad)

`${PAI_DIR}/scratchpad/YYYY-MM-DD-HHMMSS_story-explanation-[topic]/`

### Process

1. **Scratchpad (Working Files):**
   - Create timestamped directory for each story explanation project
   - Store raw content extraction (transcripts, article text, etc.)
   - Keep UltraThink analysis notes
   - Save multiple framing explorations (5+ options from deep analysis)
   - Draft iterations and refinements
   - Example: `${PAI_DIR}/scratchpad/2025-10-26-143000_story-explanation-agi-timeline/`

2. **History (Permanent Archive - Optional):**
   - Move to `${PAI_DIR}/history/research/YYYY-MM/YYYY-MM-DD-HHMMSS_AGENT-[agent]_RESEARCH_[slug].md` **ONLY IF:**
     - The analysis provides valuable reusable insights about narrative framing
     - The content analysis reveals patterns applicable to future work
     - The framing exploration demonstrates particularly effective techniques
     - You want to reference this analysis methodology later
   - Include: Final story explanation + UltraThink analysis notes + framing options explored
   - Most story explanations are one-off outputs and can stay in scratchpad

3. **Distinction:**
   - **Scratchpad = All working files** (content extraction, drafts, explorations)
   - **History = Only valuable analytical insights** (methodology learnings, exceptional framing discoveries)
   - **Most story explanations are throwaway content** - only archive exceptional analysis

## File Structure Example

```
${PAI_DIR}/scratchpad/2025-10-26-143000_story-explanation-agi-timeline/
├── raw-content.txt                    # Extracted article/transcript
├── ultrathink-analysis.md             # Deep narrative analysis notes
├── framing-explorations.md            # 5+ different narrative framings explored
├── draft-v1.md                        # First draft
├── draft-v2.md                        # Refined version
└── final-story-explanation.md         # Final output

# Only if exceptional:
${PAI_DIR}/history/research/2025-10/2025-10-26-143000_AGENT-default_RESEARCH_agi-timeline-narrative-framing-analysis.md
```

## Guidelines

- Always work in scratchpad first
- Only move to history if the analysis itself is valuable for future reference
- Clean up scratchpad after project completion (or leave for periodic cleanup)
- The story explanation output itself goes to the user - not necessarily to history
