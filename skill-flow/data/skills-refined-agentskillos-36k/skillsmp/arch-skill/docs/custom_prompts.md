OpenAI Developers
Resources
Codex
ChatGPT
Blog

Overview
Quickstart
Pricing
Cookbooks
Rules
AGENTS.md
Custom Prompts
MCP
Authentication
Security
Enterprise
Windows
Non-interactive Mode
Codex SDK
MCP Server
GitHub Action
Changelog
Feature Maturity
Open Source
Add metadata and arguments
Invoke and manage custom commands

Copy Page
More page actions
Custom Prompts
Define reusable prompts that behave like slash commands

Custom prompts let you turn Markdown files into reusable prompts that you can invoke as slash commands in both the Codex CLI and the Codex IDE extension.

Custom prompts require explicit invocation and live in your local Codex home directory (for example, ~/.codex), so they’re not shared through your repository. If you want to share a prompt (or want Codex to implicitly invoke it), use skills.

Create the prompts directory:

mkdir -p ~/.codex/prompts

Create ~/.codex/prompts/draftpr.md with reusable guidance:

---
description: Prep a branch, commit, and open a draft PR
argument-hint: [FILES=<paths>] [PR_TITLE="<title>"]
---

Create a branch named `dev/<feature_name>` for this work.
If files are specified, stage them first: $FILES.
Commit the staged changes with a clear message.
Open a draft PR on the same branch. Use $PR_TITLE when supplied; otherwise write a concise summary yourself.

Restart Codex so it loads the new prompt (restart your CLI session, and reload the IDE extension if you are using it).

Expected: Typing /prompts:draftpr in the slash command menu shows your custom command with the description from the front matter and hints that files and a PR title are optional.

Add metadata and arguments

Codex reads prompt metadata and resolves placeholders the next time the session starts.

Description: Shown under the command name in the popup. Set it in YAML front matter as description:.
Argument hint: Document expected parameters with argument-hint: KEY=<value>.
Positional placeholders: $1 through $9 expand from space-separated arguments you provide after the command. $ARGUMENTS includes them all.
Named placeholders: Use uppercase names like $FILE or $TICKET_ID and supply values as KEY=value. Quote values with spaces (for example, FOCUS="loading state").
Literal dollar signs: Write $$ to emit a single $ in the expanded prompt.
After editing prompt files, restart Codex or open a new chat so the updates load. Codex ignores non-Markdown files in the prompts directory.

Invoke and manage custom commands

In Codex (CLI or IDE extension), type / to open the slash command menu.

Enter prompts: or the prompt name, for example /prompts:draftpr.

Supply required arguments:

/prompts:draftpr FILES="src/pages/index.astro src/lib/api.ts" PR_TITLE="Add hero animation"

Press Enter to send the expanded instructions (skip either argument when you don’t need it).

Expected: Codex expands the content of draftpr.md, replacing placeholders with the arguments you supplied, then sends the result as a message.

Manage prompts by editing or deleting files under ~/.codex/prompts/. Codex scans only the top-level Markdown files in that folder, so place each custom prompt directly under ~/.codex/prompts/ rather than in subdirectories.

OpenAI Developers
Resources
Codex
ChatGPT
Blog

Overview
Quickstart
Pricing
Cookbooks
Overview
Features
Command Line Options
Slash commands
Rules
AGENTS.md
Custom Prompts
MCP
Authentication
Security
Enterprise
Windows
Non-interactive Mode
Codex SDK
MCP Server
GitHub Action
Changelog
Feature Maturity
Open Source
Built-in slash commands
Control your session with slash commands
Custom prompts

Copy Page
More page actions
Slash commands in Codex CLI
Control Codex during interactive sessions

Slash commands give you fast, keyboard-first control over Codex. Type / in the composer to open the slash popup, choose a command, and Codex will perform actions such as switching models, adjusting approvals, or summarizing long conversations without leaving the terminal.

This guide shows you how to:

Find the right built-in slash command for a task
Steer an active session with commands like /model, /approvals, and /status
Create custom prompts that behave like new slash commands with arguments and metadata (see Custom Prompts)
Built-in slash commands

Codex ships with the following commands. Open the slash popup and start typing the command name to filter the list.

Command	Purpose	When to use it
/approvals	Set what Codex can do without asking first.	Relax or tighten approval requirements mid-session, such as switching between Auto and Read Only.
/compact	Summarize the visible conversation to free tokens.	Use after long runs so Codex retains key points without blowing the context window.
/diff	Show the Git diff, including files Git isn’t tracking yet.	Review Codex’s edits before you commit or run tests.
/exit	Exit the CLI (same as /quit).	Alternative spelling; both commands exit the session.
/feedback	Send logs to the Codex maintainers.	Report issues or share diagnostics with support.
/init	Generate an AGENTS.md scaffold in the current directory.	Capture persistent instructions for the repository or subdirectory you’re working in.
/logout	Sign out of Codex.	Clear local credentials when using a shared machine.
/mcp	List configured Model Context Protocol (MCP) tools.	Check which external tools Codex can call during the session.
/mention	Attach a file to the conversation.	Point Codex at specific files or folders you want it to inspect next.
/model	Choose the active model (and reasoning effort, when available).	Switch between general-purpose models (gpt-4.1-mini) and deeper reasoning models before running a task.
/fork	Fork a saved conversation into a new thread.	Branch an older session to try a different approach without losing the original transcript.
/resume	Resume a saved conversation from your session list.	Continue work from a previous CLI session without starting over.
/new	Start a new conversation inside the same CLI session.	Reset the chat context without leaving the CLI when you want a fresh prompt in the same repo.
/quit	Exit the CLI.	Leave the session immediately.
/review	Ask Codex to review your working tree.	Run after Codex completes work or when you want a second set of eyes on local changes.
/status	Display session configuration and token usage.	Confirm the active model, approval policy, writable roots, and remaining context capacity.
/quit and /exit both exit the CLI. Use them only after you have saved or committed any important work.

Control your session with slash commands

The following workflows keep your session on track without restarting Codex.

Set the active model with /model

Start Codex and open the composer.
Type /model and press Enter.
Choose a model such as gpt-4.1-mini or gpt-4.1 from the popup.
Expected: Codex confirms the new model in the transcript. Run /status to verify the change.

Update approval rules with /approvals

Type /approvals and press Enter.
Select the approval preset that matches your comfort level, for example Auto for hands-off runs or Read Only to review edits.
Expected: Codex announces the updated policy. Future actions respect the new approval mode until you change it again.

Inspect the session with /status

In any conversation, type /status.
Review the output for the active model, approval policy, writable roots, and current token usage.
Expected: You see a summary like what codex status prints in the shell, confirming Codex is operating where you expect.

Keep transcripts lean with /compact

After a long exchange, type /compact.
Confirm when Codex offers to summarize the conversation so far.
Expected: Codex replaces earlier turns with a concise summary, freeing context while keeping critical details.

Review changes with /diff

Type /diff to inspect the Git diff.
Scroll through the output inside the CLI to review edits and added files.
Expected: Codex shows changes you’ve staged, changes you haven’t staged yet, and files Git hasn’t started tracking, so you can decide what to keep.

Highlight files with /mention

Type /mention followed by a path, for example /mention src/lib/api.ts.
Select the matching result from the popup.
Expected: Codex adds the file to the conversation, ensuring follow-up turns reference it directly.

Start a new conversation with /new

Type /new and press Enter.
Expected: Codex starts a fresh conversation in the same CLI session, so you can switch tasks without leaving your terminal.

Resume a saved conversation with /resume

Type /resume and press Enter.
Choose the session you want from the saved-session picker.
Expected: Codex reloads the selected conversation’s transcript so you can pick up where you left off, keeping the original history intact.

Branch a saved conversation with /fork

Type /fork and press Enter.
Pick the saved session you want to branch from in the picker (same list you see with /resume).
Expected: Codex clones the selected conversation into a new thread with a fresh ID, leaving the original transcript untouched so you can explore an alternative approach in parallel.

Generate AGENTS.md with /init

Run /init in the directory where you want Codex to look for persistent instructions.
Review the generated AGENTS.md, then edit it to match your repository conventions.
Expected: Codex creates an AGENTS.md scaffold you can refine and commit for future sessions.

Ask for a working tree review with /review

Type /review.
Follow up with /diff if you want to inspect the exact file changes.
Expected: Codex summarizes issues it finds in your working tree, focusing on behavior changes and missing tests.

List MCP tools with /mcp

Type /mcp.
Review the list to confirm which MCP servers and tools are available.
Expected: You see the configured Model Context Protocol (MCP) tools Codex can call in this session.

Send feedback with /feedback

Type /feedback and press Enter.
Follow the prompts to include logs or diagnostics.
Expected: Codex collects the requested diagnostics and submits them to the maintainers.

Sign out with /logout

Type /logout and press Enter.
Expected: Codex clears local credentials for the current user session.

Exit the CLI with /quit or /exit

Type /quit (or /exit) and press Enter.
Expected: Codex exits immediately. Save or commit any important work first.

Custom prompts

To create your own reusable prompts that behave like slash commands (invoked as /prompts: <name>), see Custom Prompts.

Previous
Command Line Options
