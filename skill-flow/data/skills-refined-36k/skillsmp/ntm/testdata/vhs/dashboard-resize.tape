# Dashboard Resize Test
# Tests tier transitions when terminal is resized

Output testdata/screenshots/dashboard-resize.png

Set FontSize 14
Set Shell "bash"
Set Theme "Catppuccin Mocha"

# Start at mega width (340 cols)
Set Width 340
Set Height 60

Type "ntm dashboard --demo"
Enter
Sleep 2s

Screenshot testdata/screenshots/dashboard-resize-mega.png

# Resize to ultra width (250 cols)
Set Width 250
Sleep 1s
Screenshot testdata/screenshots/dashboard-resize-ultra.png

# Resize to wide width (210 cols)
Set Width 210
Sleep 1s
Screenshot testdata/screenshots/dashboard-resize-wide.png

# Resize to split width (140 cols)
Set Width 140
Sleep 1s
Screenshot testdata/screenshots/dashboard-resize-split.png

# Resize to narrow width (100 cols)
Set Width 100
Sleep 1s
Screenshot testdata/screenshots/dashboard-resize-narrow.png

# Resize back to mega (test hysteresis - should not flicker)
Set Width 340
Sleep 1s
Screenshot testdata/screenshots/dashboard-resize.png
