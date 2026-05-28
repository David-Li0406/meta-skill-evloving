---
name: brainstorming
description: Use this skill when rough ideas need design before code or multiple approaches exist.
---

# Objective
Turn rough ideas into fully-formed designs through natural collaborative dialogue. Understand the context, explore alternatives, and validate incrementally.

# When to Use
Use brainstorming when you have a rough idea but unclear implementation, multiple approaches exist and you need to choose, requirements are fuzzy or incomplete, or design decisions need validation before coding. Skip for clear mechanical tasks with obvious solutions, well-defined requirements with standard implementations, or simple bug fixes.

# Understanding Context
Explore the current project state. Check existing files, documentation, and recent commits to understand what's already built. Ask questions one at a time to refine the idea, using multiple choice when possible to facilitate easier responses. Focus on understanding the purpose (what problem does this solve?), constraints (what limits the solution?), and success criteria (how do we know it works?). One question per message; if a topic needs more exploration, break it into multiple questions to avoid overwhelming the partner.

# Exploring Alternatives
Propose different approaches with their tradeoffs, presenting them conversationally and showing all options first before making a recommendation. Structure alternatives clearly, ensuring each option is distinct with clear tradeoffs. Avoid defaulting to hybrid approaches unless there is a specific, compelling reason. Make a clear recommendation by picking one approach and explaining why it fits best, and let the human partner react after your recommendation.

# Presenting Design
Once you understand what you're building, present the design in small, manageable sections covering architecture and component structure, data flow and state management, error handling and edge cases, and testing approach. Ask after each section whether it looks right and be ready to clarify if something doesn't make sense. This incremental validation catches misunderstandings early.

# After Validation
Write the validated design to `docs/plans/[topic]-design.md`, keeping it concise and focused on decisions and rationale, not implementation details. Commit the design document to git for tracking. If continuing to implementation, ask whether to proceed, set up an isolated workspace for development, and create a detailed implementation plan breaking the design into concrete tasks.

# Key Principles
- One question at a time; avoid listing multiple questions.
- Use multiple choice when possible.
- YAGNI (You Aren't Gonna Need It) ruthlessly; remove unnecessary features.
- Explore alternatives always; present multiple approaches before settling on one.
- Incremental validation; present design in sections and validate each before continuing.
- Be flexible; clarify when something doesn't make sense to your partner.

# Common Pitfalls
- Don't ask many questions at once.
- Don't present a complete design without incremental validation.
- Don't skip exploring alternatives.
- Don't add features beyond stated requirements.
- Don't continue with a design that confuses your partner; clarify first.