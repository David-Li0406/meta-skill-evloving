# Dashboard Refresh Test
# Tests that the ticker updates and refresh works

Output testdata/screenshots/dashboard-refresh.png

Set FontSize 14
Set Width 340
Set Height 60
Set Shell "bash"
Set Theme "Catppuccin Mocha"

Type "ntm dashboard --demo"
Enter
Sleep 2s

# Initial state
Screenshot testdata/screenshots/dashboard-refresh-t0.png

# Wait for ticker to update (default 5s interval)
Sleep 6s
Screenshot testdata/screenshots/dashboard-refresh-t1.png

# Force refresh with 'r' key
Type "r"
Sleep 1s
Screenshot testdata/screenshots/dashboard-refresh-manual.png

# Final screenshot
Screenshot testdata/screenshots/dashboard-refresh.png
