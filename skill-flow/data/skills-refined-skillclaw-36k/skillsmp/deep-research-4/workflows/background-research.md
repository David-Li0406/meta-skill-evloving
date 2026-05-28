# Background Research Workflow

For autonomous "fire and forget" research when the user wants to continue other work.

<when_to_use>
- User says "run this in the background"
- User has other tasks to work on
- Research is well-defined and doesn't need steering
- User explicitly skips the refinement step
</when_to_use>

<how_it_works>
Instead of main Claude orchestrating, spawn a dedicated orchestrator subagent that handles the entire research loop autonomously.

The orchestrator:
1. Generates the research brief (no user validation)
2. Spawns workers in parallel
3. Synthesizes findings
4. Runs gap detection
5. Iterates as needed
6. Writes final report to file
7. Returns summary when complete
</how_it_works>

<invocation>
```
Task(
  subagent_type: "deep_research:research-orchestrator",
  prompt: "Conduct deep research on: [QUERY]

Constraints:
- Depth: [standard/exhaustive]
- Focus: [any user-specified focus]
- Max iterations: 3
- Output file: research_output/[slug]_[date].md

Run the full diffusion research loop autonomously.
Return a brief summary when complete.",
  description: "Background research: [topic]",
  run_in_background: true
)
```
</invocation>

<checking_progress>
Use TaskOutput to check on the background research:

```
TaskOutput(
  task_id: [agent_id],
  block: false,
  timeout: 1000
)
```

Or read the output file directly if the agent provided a path.
</checking_progress>

<tradeoffs>
**Advantages:**
- User can continue other work
- No interruptions for questions
- Full context isolation

**Disadvantages:**
- No mid-research steering
- No refinement step (may research wrong things)
- Can't ask clarifying questions
- Results only visible when complete

**Recommendation:** Use background mode only when:
- The query is very clear and specific
- You trust the default research dimensions
- You don't need to steer the research
</tradeoffs>
