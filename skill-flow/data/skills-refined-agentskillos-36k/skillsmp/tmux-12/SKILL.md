---
name: tmux
description: Manage tmux sessions, windows, and panes for terminal multiplexing. Use when running long processes, managing multiple terminals, or executing commands in background sessions.
allowed-tools: Bash(tmux:*)
user-invocable: false
---

<skill name="Tmux Workflow">
  <purpose>Manage terminal sessions with tmux for background processes, parallel terminals, and persistent workspaces.</purpose>

  <section name="Session Management">
    <subsection name="Check Existing Sessions First">
      <principle>Always check before creating new sessions</principle>
      <command>tmux list-sessions 2>/dev/null || echo "No sessions"</command>
    </subsection>

    <subsection name="Create or Attach">
      <command description="Create new session">tmux new-session -d -s "session-name"</command>
      <command description="Attach to existing">tmux attach-session -t "session-name"</command>
      <command description="Create if not exists, attach if exists">tmux new-session -A -s "session-name"</command>
    </subsection>
  </section>

  <section name="Executing Commands">
    <subsection name="Run Command in Session">
      <command description="Send command to session">tmux send-keys -t "session-name" "your-command" Enter</command>
      <command description="Send to specific window">tmux send-keys -t "session-name:window-name" "command" Enter</command>
      <command description="Send to specific pane">tmux send-keys -t "session-name:0.0" "command" Enter</command>
    </subsection>

    <subsection name="Capture Output">
      <command description="Capture pane contents">tmux capture-pane -t "session-name" -p</command>
      <command description="Capture with history (last 1000 lines)">tmux capture-pane -t "session-name" -p -S -1000</command>
    </subsection>
  </section>

  <section name="Window and Pane Management">
    <command description="New window in session">tmux new-window -t "session-name" -n "window-name"</command>
    <command description="Split pane horizontally">tmux split-window -h -t "session-name"</command>
    <command description="Split pane vertically">tmux split-window -v -t "session-name"</command>
    <command description="List windows">tmux list-windows -t "session-name"</command>
    <command description="List panes">tmux list-panes -t "session-name"</command>
  </section>

  <section name="Common Patterns">
    <pattern name="Background Process">
      <description>Start process in background session</description>
      <command>tmux new-session -d -s "build" &amp;&amp; tmux send-keys -t "build" "npm run build" Enter</command>
    </pattern>

    <pattern name="Check Process Status">
      <description>Capture output to see if process completed</description>
      <command>tmux capture-pane -t "build" -p | tail -20</command>
    </pattern>

    <pattern name="Cleanup">
      <command description="Kill specific session">tmux kill-session -t "session-name"</command>
      <command description="Kill all sessions">tmux kill-server</command>
    </pattern>
  </section>

  <best-practices>
    <practice>Name sessions descriptively: Use meaningful names like `dev`, `build`, `logs`</practice>
    <practice>Check before creating: Always verify session doesn't exist first</practice>
    <practice>Capture output: Use `capture-pane` to verify command results</practice>
    <practice>Clean up: Kill sessions when work is complete</practice>
    <practice>Chain commands: Use `&amp;&amp;` to ensure proper sequencing</practice>
  </best-practices>
</skill>
