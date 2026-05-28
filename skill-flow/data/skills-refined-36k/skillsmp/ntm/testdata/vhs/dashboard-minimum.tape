# Dashboard Minimum Size Test
# Tests rendering at minimum terminal sizes

Output testdata/screenshots/dashboard-minimum.png

Set FontSize 14
Set Shell "bash"
Set Theme "Catppuccin Mocha"

# Start at minimum standard terminal size 80x24
Set Width 80
Set Height 24

Type "ntm dashboard --demo"
Enter
Sleep 2s

Screenshot testdata/screenshots/dashboard-minimum-80x24.png

# Even smaller (40x10 - extreme case)
Set Width 40
Set Height 10
Sleep 1s
Screenshot testdata/screenshots/dashboard-minimum-40x10.png

# Final screenshot at 80x24
Set Width 80
Set Height 24
Sleep 1s
Screenshot testdata/screenshots/dashboard-minimum.png
