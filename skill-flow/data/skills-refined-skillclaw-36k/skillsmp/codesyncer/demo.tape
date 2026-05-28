# VHS Demo Script for CodeSyncer v3.0 (English)
# Run: vhs demo.tape

Output demo.gif
Output demo.mp4

Set FontSize 20
Set Width 800
Set Height 550
Set Theme "Dracula"
Set Padding 40
Set Shell "bash"
Set TypingSpeed 80ms

# ============================================
# Setup (hidden)
# ============================================

Hide
Type "cd /tmp && rm -rf demo-project && mkdir demo-project && cd demo-project && git init -q && echo '{}' > package.json && clear"
Enter
Sleep 500ms
Show
Sleep 1.5s

# ============================================
# Step 1: Install
# ============================================

Type "# Step 1: Install"
Enter
Sleep 2s

Type "npm install -g codesyncer"
Enter
Sleep 3s

# ============================================
# Step 2: Initialize
# ============================================

Type "# Step 2: Initialize"
Enter
Sleep 2s

Type "codesyncer init"
Enter
Sleep 4s

# Language: English is DEFAULT - just press Enter!
Enter
Sleep 3s

# Start setup? Yes
Enter
Sleep 2s

# Project name: default
Enter
Sleep 1s

# GitHub username
Type "your-name"
Enter
Sleep 5s

# ============================================
# Step 3: Done!
# ============================================

Sleep 2s

Type "# Done! Tell Claude: 'Read CLAUDE.md'"
Enter
Sleep 4s
