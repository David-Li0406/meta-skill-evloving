---
name: developer-growth-analysis
description: Use this skill to analyze your recent coding work, identify development patterns and gaps, and receive personalized learning resources and a growth report delivered to your Slack DMs.
---

# Developer Growth Analysis

This skill provides personalized feedback on your recent coding work by analyzing your Claude Code chat interactions and identifying patterns that reveal strengths and areas for growth.

## When to Use This Skill

Use this skill when you want to:
- Understand your development patterns and habits from recent work
- Identify specific technical gaps or recurring challenges
- Discover which topics would benefit from deeper study
- Get curated learning resources tailored to your actual work patterns
- Track improvement areas across your recent projects
- Find high-quality articles that directly address the skills you're developing

This skill is ideal for developers who want structured feedback on their growth without waiting for code reviews, and who prefer data-driven insights from their own work history.

## What This Skill Does

This skill performs a six-step analysis of your development work:

1. **Reads Your Chat History**: Accesses your local Claude Code chat history from the past 24-48 hours to understand what you've been working on.

2. **Identifies Development Patterns**: Analyzes the types of problems you're solving, technologies you're using, challenges you encounter, and how you approach different kinds of tasks.

3. **Detects Improvement Areas**: Recognizes patterns that suggest skill gaps, repeated struggles, inefficient approaches, or areas where you might benefit from deeper knowledge.

4. **Generates a Personalized Report**: Creates a comprehensive report showing your work summary, identified improvement areas, and specific recommendations for growth.

5. **Finds Learning Resources**: Uses HackerNews to curate high-quality articles and discussions directly relevant to your improvement areas, providing you with a reading list tailored to your actual development work.

6. **Sends to Your Slack DMs**: Automatically delivers the complete report to your own Slack direct messages so you can reference it anytime, anywhere.

## How to Use

Ask Claude to analyze your recent coding work:

```
Analyze my developer growth from my recent chats
```

Or be more specific about which time period:

```
Analyze my work from today and suggest areas for improvement
```

The skill will generate a formatted report with:
- Overview of your recent work
- Key improvement areas identified
- Specific recommendations for each area
- Curated learning resources from HackerNews
- Action items you can focus on

## Instructions

When a user requests analysis of their developer growth or coding patterns from recent work:

1. **Access Chat History**

   Read the chat history from `~/.claude/history.jsonl`. This file is a JSONL format where each line contains:
   - `display`: The user's message/request
   - `project`: The project being worked on
   - `timestamp`: Unix timestamp (in milliseconds)
   - `pastedContents`: Any code or content pasted

   Filter for entries from the past 24-48 hours based on the current timestamp.

2. **Analyze Work Patterns**

   Extract and analyze the following from the filtered chats:
   - **Projects and Domains**: What types of projects was the user working on? (e.g., backend, frontend, DevOps, data, etc.)
   - **Technologies Used**: What languages, frameworks, and tools appear in the conversations?
   - **Problem Types**: What categories of problems are being solved? (e.g., performance optimization, debugging, feature implementation, refactoring, setup/configuration)
   - **Challenges Encountered**: What problems did the user struggle with? Look for:
     - Repeated questions about similar topics
     - Problems that took multiple attempts to solve
     - Questions indicating knowledge gaps
     - Complex architectural decisions
   - **Approach Patterns**: How does the user solve problems? (e.g., methodical, exploratory, experimental)

3. **Identify Improvement Areas**

   Based on the analysis, identify 3-5 specific areas where the user could improve. These should be:
   - **Specific** (not vague like "improve coding skills")
   - **Evidence-based** (grounded in actual chat history)
   - **Actionable** (practical improvements that can be made)
   - **Prioritized** (most impactful first)

   Examples of good improvement areas:
   - "Advanced TypeScript patterns (generics, utility types, type guards) - you struggled with type safety in [specific project]"
   - "Error handling and validation - I noticed you patched several bugs related to missing null checks"
   - "Async/await patterns - your recent work shows some race conditions and timing issues"
   - "Database query optimization - you rewrote the same query multiple times"

4. **Generate Report**

   Create a comprehensive report with this structure:

   ```markdown
   # Your Developer Growth Report

   **Report Period**: [Yesterday / Today / [Custom Date Range]]
   **Last Updated**: [Current Date and Time]

   ## Work Summary

   [2-3 paragraphs summarizing what the user worked on, projects touched, technologies used, and overall focus areas]

   Example:
   "Over the past 24 hours, you focused primarily on backend development with three distinct projects. Your work involved TypeScript, React, and deployment infrastructure. You tackled a mix of feature implementation, debugging, and architectural decisions, with a particular focus on API design and database optimization."

   ## Improvement Areas (Prioritized)

   ### 1. [Area Name]

   **Why This Matters**: [Explanation of why this skill is important for the user's work]

   **What I Observed**: [Specific evidence from chat history showing this gap]

   **Recommendation**: [Concrete step(s) to improve in this area]

   **Time to Skill Up**: [Brief estimate of effort required]

   ---

   [Repeat for 2-4 additional areas]

   ## Strengths Observed

   [2-3 bullet points highlighting things you're doing well - things to continue doing]

   ## Action Items

   Priority order:
   1. [Action item derived from highest priority improvement area]
   2. [Action item from next area]
   3. [Action item from next area]

   ## Learning Resources

   [Will be populated in next step]
   ```

5. **Search for Learning Resources**

   Use Rube MCP to search HackerNews for articles related to each improvement area:

   - For each improvement area, construct a search query targeting high-quality resources
   - Search HackerNews using RUBE_SEARCH_TOOLS with queries like:
     - "Learn [Technology/Pattern] best practices"
     - "[Technology] advanced patterns and techniques"
     - "Debugging [specific problem type] in [language]"
   - Prioritize posts with high engagement (comments, upvotes)
   - For each area, include 2-3 most relevant articles with:
     - Article title
     - Publication date
     - Brief description of why it's relevant
     - Link to the article

   Add this section to the report:

   ```markdown
   ## Curated Learning Resources

   ### For: [Improvement Area]

   1. **[Article Title]** - [Date]
      [Description of what it covers and why it's relevant to your improvement area]
      [Link]

   2. **[Article Title]** - [Date]
      [Description]
      [Link]

   [Repeat for other improvement areas]
   ```

6. **Present the Complete Report**

   Deliver the report in a clean, readable format that the user can:
   - Quickly scan for key takeaways
   - Use for focused learning planning
   - Reference over the next week as they work on improvements
   - Share with mentors if they want external feedback

7. **Send Report to Slack DMs**

   Use Rube MCP to send the complete report to the user's own Slack DMs:

   - Check if Slack connection is active via RUBE_SEARCH_TOOLS
   - If not connected, use RUBE_MANAGE_CONNECTIONS to initiate Slack auth
   - Use RUBE_MULTI_EXECUTE_TOOL to send the report as a formatted message:
     - Send the report title and period as the first message
     - Break the report into logical sections (Summary, Improvements, Strengths, Actions, Resources)
     - Format each section as a well-structured Slack message with proper markdown
     - Include clickable links for the learning resources
   - Confirm delivery in the CLI output

   This ensures the user has the report in a place they check regularly and can reference it throughout the week.

## Tips and Best Practices

- Run this analysis once a week to track your improvement trajectory over time
- Pick one improvement area at a time and focus on it for a few days before moving to the next
- Use the learning resources as a study guide; work through the recommended materials and practice applying the patterns
- Revisit this report after focusing on an area for a week to see how your work patterns change
- The learning resources are intentionally curated for your actual work, not generic topics, so they'll be highly relevant to what you're building

## How Accuracy and Quality Are Maintained

This skill:
- Analyzes your actual work patterns from timestamped chat history
- Generates evidence-based recommendations grounded in real projects
- Curates learning resources that directly address your identified gaps
- Focuses on actionable improvements, not vague feedback
- Provides specific time estimates based on complexity
- Prioritizes areas that will have the most impact on your development velocity

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed