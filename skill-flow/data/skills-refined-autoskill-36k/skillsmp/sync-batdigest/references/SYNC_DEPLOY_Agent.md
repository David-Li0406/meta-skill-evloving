# SYNC PROMPTS

Copy/paste a prompt into a CLI terminal agent. Each prompt includes Mac/Linux and Windows (PowerShell) commands.

Common runlists (most used):
- #0 Standard deploy
- #1 Standard deploy + verify
- #2 Standard deploy + verify + IndexNow (auto)
- #3 Full deploy + verify + IndexNow (auto + manual)

---

## 0) Standard deploy

Run: #4 → #6 → #7 → #8

---

## 1) Standard deploy + verify

Run: #4 → #6 → #7 → #8 → #9

---

## 2) Standard deploy + verify + IndexNow (auto)

Run: #4 → #6 → #7 → #8 → #9 → #10

---

## 3) Full deploy + verify + IndexNow (auto + manual)

Run: #4 → #6 → #7 → #8 → #9 → #10 → #11

Notes:
- If `batdigest-static` is behind locally, run #5 before #8.

---

## 4) Sync batdigest-flask (backup local work + update)

Mac/Linux prompt:
```bash
# You are a terminal agent. Back up local work (if any), pull latest, then push.
cd ~/Coding_Projects/batdigest-flask
git status -sb
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "Backup before sync $(date +%F-%H%M)"
fi
git pull --rebase
git push
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Back up local work (if any), pull latest, then push.
cd $HOME\Coding_Projects\batdigest-flask
git status -sb
if (git status --porcelain) {
  git add -A
  git commit -m ("Backup before sync " + (Get-Date -Format "yyyy-MM-dd-HHmm"))
}
git pull --rebase
git push
```

---

## 5) Sync batdigest-static (backup local work + update)

Mac/Linux prompt:
```bash
# You are a terminal agent. Back up local work (if any), pull latest, then push.
cd ~/Coding_Projects/batdigest-static
git status -sb
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "Backup before sync $(date +%F-%H%M)"
fi
git pull --rebase
git push
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Back up local work (if any), pull latest, then push.
cd $HOME\Coding_Projects\batdigest-static
git status -sb
if (git status --porcelain) {
  git add -A
  git commit -m ("Backup before sync " + (Get-Date -Format "yyyy-MM-dd-HHmm"))
}
git pull --rebase
git push
```

---

## 6) Generate the static site (dist/)

Mac/Linux prompt:
```bash
# You are a terminal agent. Generate dist/ from the Flask app.
cd ~/Coding_Projects/batdigest-flask
source venv/bin/activate
python scripts/active/static_site_generator.py
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Generate dist/ from the Flask app.
cd $HOME\Coding_Projects\batdigest-flask
.\venv\Scripts\Activate.ps1
python scripts/active/static_site_generator.py
```

Notes:
- Script location: `batdigest-flask/scripts/active/static_site_generator.py`
- Output goes to `batdigest-flask/dist/`
- Also generates `app/static/js/search-data.json` (and copies it into `dist/static/js/`).

---

## 7) Inline CSS in dist/ (batdigest-flask)

Mac/Linux prompt:
```bash
# You are a terminal agent. Run the inliner in batdigest-flask.
cd ~/Coding_Projects/batdigest-flask
source venv/bin/activate
python scripts/inline_css_optimizer.py
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Run the inliner in batdigest-flask.
cd $HOME\Coding_Projects\batdigest-flask
.\venv\Scripts\Activate.ps1
python scripts/inline_css_optimizer.py
```

Notes:
- Script location: `batdigest-flask/scripts/inline_css_optimizer.py`
- It edits files in `batdigest-flask/dist/` in place.
- Also bundles core footer scripts into `dist/static/js/scripts-footer.js`.

---

## 8) Deploy dist/ into batdigest-static (rsync/robocopy)

Mac/Linux prompt:
```bash
# You are a terminal agent. Copy batdigest-flask/dist into batdigest-static.
# IMPORTANT: --delete is used, so keep the excludes to avoid nuking repo-only files.
cd ~/Coding_Projects/batdigest-static
rsync -av --delete \
  --exclude='.git/' \
  --exclude='.gitignore' \
  --exclude='.http_server.log' \
  ../batdigest-flask/dist/ ./

git status -sb
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "Deploy: sync dist from batdigest-flask $(date +%F-%H%M)"
  git push
else
  echo "No changes to deploy."
fi
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Copy batdigest-flask/dist into batdigest-static.
# IMPORTANT: /MIR mirrors the folder (deletes removed files), so exclude repo-only files.
cd $HOME\Coding_Projects\batdigest-static
robocopy ..\batdigest-flask\dist . /MIR /XD .git /XF .gitignore .http_server.log

git status -sb
if (git status --porcelain) {
  git add -A
  git commit -m ("Deploy: sync dist from batdigest-flask " + (Get-Date -Format "yyyy-MM-dd-HHmm"))
  git push
} else {
  Write-Host "No changes to deploy."
}
```

---

## 9) Verify live deploy against dist/ (smoke + parity checks)

Mac/Linux prompt:
```bash
# You are a terminal agent. Verify live site matches dist/ after deploy.
cd ~/Coding_Projects/batdigest-flask
source venv/bin/activate
python scripts/deploy/verify_live.py
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Verify live site matches dist/ after deploy.
cd $HOME\Coding_Projects\batdigest-flask
.\venv\Scripts\Activate.ps1
python scripts/deploy/verify_live.py
```

Notes:
- Checks sitemap parity, asset hashes, build stamp, and a handful of critical pages.
- If it fails, re-run after a few minutes (Cloudflare cache) and then investigate.

---

## 10) Submit IndexNow for changed pages in batdigest-static (auto)

Mac/Linux prompt:
```bash
# You are a terminal agent. Submit changed HTML pages from batdigest-static.
cd ~/Coding_Projects/batdigest-flask
source venv/bin/activate
python scripts/active/submit_indexnow_changes.py --fetch
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Submit changed HTML pages from batdigest-static.
cd $HOME\Coding_Projects\batdigest-flask
.\venv\Scripts\Activate.ps1
python scripts/active/submit_indexnow_changes.py --fetch
```

Notes:
- Automatic mode: submits the HTML pages that changed in your deploy by inspecting `batdigest-static` via git diff.
- Run after copying `batdigest-flask/dist/` into `batdigest-static/`.
- Best-case: run after the deploy commit and before `git push` so it diffs cleanly vs `origin/main`.
- If you already pushed, use `--base HEAD~1` (or another ref) to submit just the last deploy commit.

---

## 11) Submit IndexNow for specific URLs (manual)

Mac/Linux prompt:
```bash
# You are a terminal agent. Submit specific URLs to IndexNow.
cd ~/Coding_Projects/batdigest-flask
source venv/bin/activate
python scripts/active/submit_indexnow.py \
  --urls https://batdigest.com/path/ https://batdigest.com/another-path/
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Submit specific URLs to IndexNow.
cd $HOME\Coding_Projects\batdigest-flask
.\venv\Scripts\Activate.ps1
python scripts/active/submit_indexnow.py `
  --urls https://batdigest.com/path/ https://batdigest.com/another-path/
```

Notes:
- Manual mode: hand-pick one-off URLs (HTML or non-HTML like datasets/sitemaps).
- Recommended order: run #10 first (auto-changed pages), then #11 for extras.
- Uses the IndexNow key file in `batdigest-static/` by default.

---

## 12) Start Flask server (prefer 5003, fallback to 5004)

Mac/Linux prompt:
```bash
# You are a terminal agent. Start Flask on 5003 or 5004 if busy.
cd ~/Coding_Projects/batdigest-flask
source venv/bin/activate
PORT=5003
if lsof -i :$PORT >/dev/null 2>&1; then PORT=5004; fi
echo "Open http://localhost:$PORT/"
python -m flask --app run:app run --host 0.0.0.0 --port $PORT
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Start Flask on 5003 or 5004 if busy.
cd $HOME\Coding_Projects\batdigest-flask
.\venv\Scripts\Activate.ps1
$port = 5003
if (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue) { $port = 5004 }
Write-Host ("Open http://localhost:" + $port + "/")
python -m flask --app run:app run --host 0.0.0.0 --port $port
```

---

## 13) Serve local dist/ (pre-inliner site)

Mac/Linux prompt:
```bash
# You are a terminal agent. Serve dist/ (pre-inliner).
cd ~/Coding_Projects/batdigest-flask
source venv/bin/activate
PORT=5003
if lsof -i :$PORT >/dev/null 2>&1; then PORT=5004; fi
echo "Open http://localhost:$PORT/"
python -m http.server $PORT --directory dist
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Serve dist/ (pre-inliner).
cd $HOME\Coding_Projects\batdigest-flask
.\venv\Scripts\Activate.ps1
$port = 5003
if (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue) { $port = 5004 }
Write-Host ("Open http://localhost:" + $port + "/")
python -m http.server $port --directory dist
```

---

## 14) Serve local inlined site (batdigest-static)

Mac/Linux prompt:
```bash
# You are a terminal agent. Serve batdigest-static (inlined site).
cd ~/Coding_Projects/batdigest-static
PORT=5003
if lsof -i :$PORT >/dev/null 2>&1; then PORT=5004; fi
echo "Open http://localhost:$PORT/"
python3 -m http.server $PORT
```

Windows (PowerShell) prompt:
```powershell
# You are a terminal agent. Serve batdigest-static (inlined site).
cd $HOME\Coding_Projects\batdigest-static
$port = 5003
if (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue) { $port = 5004 }
Write-Host ("Open http://localhost:" + $port + "/")
python -m http.server $port
```

