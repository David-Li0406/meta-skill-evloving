# Dashboard Basic Rendering Test
# Tests that the dashboard renders correctly at startup

Output testdata/screenshots/dashboard-basic.png

Set FontSize 14
Set Width 340
Set Height 60
Set Shell "bash"
Set Theme "Catppuccin Mocha"

# Start dashboard in demo mode (no real tmux sessions)
Type "ntm dashboard --demo"
Enter
Sleep 2s

# Take screenshot of initial render
Screenshot testdata/screenshots/dashboard-basic-initial.png

# Wait for any animations to settle
Sleep 500ms

# Final screenshot
Screenshot testdata/screenshots/dashboard-basic.png
