# Installation Guide - Quotefix Skill

This guide will help you install the **Quotefix** skill globally so it's available in **all** your Claude Code environments.

## 📍 What is Global Installation?

| Installation Type | Location | Scope |
|------------------|----------|-------|
| **Project Skill** | `.claude/skills/` | Only this repository |
| **Personal Skill** (Global) | `~/.claude/skills/` | **ALL projects and sessions** |

This installer creates a **personal skill** that works everywhere!

---

## 🚀 Quick Installation

### Option 1: Linux / macOS / WSL (Bash)

```bash
# Navigate to the skill directory
cd .claude/skills/quotefix

# Make the installer executable
chmod +x install.sh

# Run the installer
./install.sh
```

### Option 2: Windows (PowerShell)

```powershell
# Navigate to the skill directory
cd .claude\skills\quotefix

# Run the installer
.\install.ps1
```

### Option 3: Windows (Git Bash / MSYS2)

```bash
# Navigate to the skill directory
cd .claude/skills/quotefix

# Run the installer
bash install.sh
```

---

## 📦 Installation Locations

After installation, the skill will be located at:

**Linux / macOS / WSL:**
```
~/.claude/skills/quotefix/
├── SKILL.md
├── examples.md
└── README.md
```

**Windows:**
```
C:\Users\YourUsername\.claude\skills\quotefix\
├── SKILL.md
├── examples.md
└── README.md
```

---

## 🌍 Multi-Environment Setup (Windows + WSL)

If you use both **Windows** and **WSL**, install the skill in **both** environments:

### Step 1: Install in Windows

```powershell
# In PowerShell
cd C:\path\to\havok-training\.claude\skills\quotefix
.\install.ps1
```

### Step 2: Install in WSL

```bash
# In WSL
cd /path/to/havok-training/.claude/skills/quotefix
./install.sh
```

**Why install in both?**
- Windows Claude Code uses `C:\Users\YourUsername\.claude\skills\`
- WSL Claude Code uses `/home/username/.claude/skills/`
- These are **separate filesystems**, so you need the skill in both!

---

## 🔄 Installing on Multiple Machines

### Method 1: Clone the Repository

On each machine:

```bash
# Clone the repo
git clone https://github.com/havok-training/havok-training.git
cd havok-training/.claude/skills/quotefix

# Run the installer
./install.sh          # Linux/macOS/WSL
# OR
.\install.ps1         # Windows PowerShell
```

### Method 2: Direct Download (No Git)

1. **Download the skill files:**
   - Go to: https://github.com/havok-training/havok-training/tree/claude/detect-shell-environment-G4vQY/.claude/skills/quotefix
   - Download: `SKILL.md`, `examples.md`, `README.md`, `install.sh`, `install.ps1`

2. **Create the directory:**
   ```bash
   mkdir -p ~/.claude/skills/quotefix
   ```

3. **Copy files:**
   ```bash
   cp SKILL.md examples.md README.md ~/.claude/skills/quotefix/
   ```

### Method 3: Manual Installation Script

Create and run this on any machine:

**Bash version:**
```bash
#!/bin/bash
mkdir -p ~/.claude/skills/quotefix
cd ~/.claude/skills/quotefix

# Download files directly from GitHub
curl -O https://raw.githubusercontent.com/havok-training/havok-training/claude/detect-shell-environment-G4vQY/.claude/skills/quotefix/SKILL.md
curl -O https://raw.githubusercontent.com/havok-training/havok-training/claude/detect-shell-environment-G4vQY/.claude/skills/quotefix/examples.md
curl -O https://raw.githubusercontent.com/havok-training/havok-training/claude/detect-shell-environment-G4vQY/.claude/skills/quotefix/README.md

echo "Installation complete!"
```

**PowerShell version:**
```powershell
$SkillDir = "$env:USERPROFILE\.claude\skills\quotefix"
New-Item -Path $SkillDir -ItemType Directory -Force
Set-Location $SkillDir

$BaseUrl = "https://raw.githubusercontent.com/havok-training/havok-training/claude/detect-shell-environment-G4vQY/.claude/skills/quotefix"

Invoke-WebRequest -Uri "$BaseUrl/SKILL.md" -OutFile "SKILL.md"
Invoke-WebRequest -Uri "$BaseUrl/examples.md" -OutFile "examples.md"
Invoke-WebRequest -Uri "$BaseUrl/README.md" -OutFile "README.md"

Write-Host "Installation complete!" -ForegroundColor Green
```

---

## ✅ Verify Installation

Check if the skill is installed correctly:

**Linux / macOS / WSL:**
```bash
ls -la ~/.claude/skills/quotefix/
```

**Windows PowerShell:**
```powershell
Get-ChildItem ~\.claude\skills\quotefix\
```

You should see:
```
SKILL.md
examples.md
README.md
```

---

## 🧪 Test the Skill

Create a test project and ask Claude Code to:

```
Create a file named "Größenübersicht 2024.txt" and write some content to it
```

Claude should automatically:
- ✅ Set UTF-8 encoding (`export LANG=de_DE.UTF-8`)
- ✅ Quote the filename properly (`"Größenübersicht 2024.txt"`)
- ✅ Use correct syntax for your shell

Or test nested quoting:

```
Run this command: powershell.exe -Command "Get-Process | Where-Object {$_.Name -eq 'chrome'}"
```

Claude should automatically:
- ✅ Use single quotes to protect from Bash
- ✅ Apply correct nesting pattern

---

## 🗑️ Uninstall

If you want to remove the global installation:

**Linux / macOS / WSL:**
```bash
./install.sh --uninstall
# OR manually:
rm -rf ~/.claude/skills/quotefix
```

**Windows PowerShell:**
```powershell
.\install.ps1 -Uninstall
# OR manually:
Remove-Item ~\.claude\skills\quotefix -Recurse
```

---

## 🔧 Troubleshooting

### Skill Not Working

**Problem:** Claude Code doesn't seem to use the skill.

**Solutions:**
1. **Verify installation location:**
   ```bash
   ls -la ~/.claude/skills/quotefix/SKILL.md
   ```

2. **Check file permissions:**
   ```bash
   chmod 644 ~/.claude/skills/quotefix/*.md
   ```

3. **Restart Claude Code** - Skills are loaded at startup

4. **Check skill metadata:**
   ```bash
   head -20 ~/.claude/skills/quotefix/SKILL.md
   ```
   Ensure the YAML frontmatter is intact.

### Wrong Encoding for German Characters

**Problem:** Umlauts (ä, ö, ü) display incorrectly.

**Solution:**
Ensure files are saved with UTF-8 encoding:
```bash
file ~/.claude/skills/quotefix/SKILL.md
# Should output: UTF-8 Unicode text
```

### WSL Can't Find Skill

**Problem:** Skill works in Windows but not WSL (or vice versa).

**Solution:**
They're separate environments! Install in both:
```bash
# In WSL
./install.sh

# In Windows PowerShell
.\install.ps1
```

---

## 📚 What This Skill Does

Once installed, Claude Code will **automatically**:

1. **Detect your shell** (Bash, Zsh, PowerShell, CMD, Fish)
2. **Use correct quoting** for your environment
3. **Handle German characters** (ä, ö, ü, ß) with UTF-8
4. **Manage file permissions** correctly (chmod vs icacls)
5. **Apply nested quoting patterns** (PowerShell from Bash, etc.)
6. **Use heredoc/here-strings** for complex commands
7. **Prevent common errors** that require repeated iterations

---

## 💡 Tips

### Keep Skill Updated

To update the skill:
```bash
# Pull latest changes
git pull

# Re-run installer
cd .claude/skills/quotefix
./install.sh
```

### Share With Team

Share the installer with your team:
```bash
# They can clone and install
git clone https://github.com/havok-training/havok-training.git
cd havok-training/.claude/skills/quotefix
./install.sh
```

### Backup Your Skills

```bash
# Backup all personal skills
tar -czf claude-skills-backup.tar.gz ~/.claude/skills/

# Restore
tar -xzf claude-skills-backup.tar.gz -C ~/
```

---

## 📞 Support

- **Issues:** https://github.com/havok-training/havok-training/issues
- **Documentation:** See `README.md` in the skill directory
- **Examples:** See `examples.md` for practical use cases

---

## ✨ Features After Installation

### Before (Without Skill)
```bash
# Claude might generate:
filename=Größe.txt                              # ❌ Not quoted
powershell.exe -Command "Get-Process | Where {$_.Name -eq 'foo'}"  # ❌ Bash expands $_
git commit -m "Fix "bug" in O'Brien's code"     # ❌ Quote hell
```

### After (With Skill)
```bash
# Claude automatically generates:
export LANG=de_DE.UTF-8                         # ✅ UTF-8 encoding
filename="Größe.txt"                            # ✅ Proper quoting
powershell.exe -Command 'Get-Process | Where {$_.Name -eq "foo"}'  # ✅ Correct nesting
git commit -m "$(cat <<'EOF'
Fix "bug" in O'Brien's code
EOF
)"  # ✅ Heredoc pattern
```

---

**Enjoy error-free shell commands across all your Claude Code environments!** 🎉
