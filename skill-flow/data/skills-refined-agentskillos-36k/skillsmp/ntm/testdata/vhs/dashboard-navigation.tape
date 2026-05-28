# Dashboard Navigation Test
# Tests keyboard navigation between panels

Output testdata/screenshots/dashboard-navigation.png

Set FontSize 14
Set Width 340
Set Height 60
Set Shell "bash"
Set Theme "Catppuccin Mocha"

Type "ntm dashboard --demo"
Enter
Sleep 2s

# Initial state - pane list focused
Screenshot testdata/screenshots/dashboard-nav-initial.png

# Tab to next panel
Tab
Sleep 500ms
Screenshot testdata/screenshots/dashboard-nav-tab1.png

# Tab again
Tab
Sleep 500ms
Screenshot testdata/screenshots/dashboard-nav-tab2.png

# Shift+Tab back
Ctrl+Shift+Tab
Sleep 500ms
Screenshot testdata/screenshots/dashboard-nav-back.png

# Arrow key navigation within panel
Down
Sleep 300ms
Down
Sleep 300ms
Screenshot testdata/screenshots/dashboard-nav-arrows.png

# Final screenshot
Screenshot testdata/screenshots/dashboard-navigation.png
