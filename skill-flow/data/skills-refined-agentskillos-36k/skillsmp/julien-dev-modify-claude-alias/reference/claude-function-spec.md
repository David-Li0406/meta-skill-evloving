# Spécification de la fonction claude

## Architecture actuelle (v2.1)

### Sections de code

#### Section 1: Initialisation (ligne 403)
```powershell
$cmdArgs = @("--permission-mode", "bypassPermissions")
```
**Rôle** : Définir les arguments de base pour Claude Code
**Modifiable** : NON

#### Section 2: MCP Auto-détection (lignes 405-409)
```powershell
if (Test-Path -Path ".mcp.json" -PathType Leaf) {
    $cmdArgs += @("--mcp-config", ".mcp.json")
    Write-Host "→ MCP config (.mcp.json)" -ForegroundColor Cyan
}
```
**Rôle** : Détecter et charger la config MCP si présente
**Modifiable** : NON (sauf message ou couleur)

#### Section 3: Logique de resume (lignes 411-418)
```powershell
# Reprendre la dernière session par défaut
# Utiliser "claude ." ou "claude new" pour forcer nouvelle session
$forceNew = $args | Where-Object { $_ -eq '.' -or $_ -eq 'new' }
if (-not $forceNew) {
    $cmdArgs += "--continue"
}
# Filtrer "." et "new" des arguments passés à claude
$passArgs = $args | Where-Object { $_ -ne '.' -and $_ -ne 'new' }
```
**Rôle** : Déterminer si on reprend la session ou on démarre nouveau
**Variables** : `$forceNew`, `$passArgs`
**Modifiable** : OUI (cette section change souvent)

**Comportement actuel (v2.1)** :
- Par défaut: Toujours `--continue` (resume automatique)
- `claude .` ou `claude new` : Force nouvelle session
- Si pas de session existante, Claude Code démarre une nouvelle

#### Section 4: Gestion du titre (lignes 420-425)
```powershell
# Changer le titre de l'onglet avec le nom du projet
$folderName = Split-Path $PWD -Leaf
$Host.UI.RawUI.WindowTitle = $folderName

# Empêcher Claude de modifier le titre de l'onglet
$env:CLAUDE_CODE_DISABLE_TERMINAL_TITLE = "1"
```
**Rôle** : Changer le titre de l'onglet terminal
**Modifiable** : NON (critique pour l'UX)

#### Section 5: Recherche exécutable (lignes 427-440)
```powershell
# Trouver l'exécutable Claude (npm global ou dans PATH)
$claudeExe = "$env:APPDATA\npm\claude.ps1"
if (-not (Test-Path $claudeExe)) {
    $cmd = Get-Command claude.ps1 -ErrorAction SilentlyContinue
    if ($cmd) { $claudeExe = $cmd.Source }
}
if (-not $claudeExe -or -not (Test-Path $claudeExe)) {
    $cmd = Get-Command claude.cmd -ErrorAction SilentlyContinue
    if ($cmd) { $claudeExe = $cmd.Source }
}
if (-not $claudeExe) {
    Write-Error "Claude Code non trouvé. Installez avec: npm install -g @anthropic-ai/claude-code"
    return
}
```
**Rôle** : Trouver l'exécutable Claude Code
**Modifiable** : NON (logique complexe testée)

#### Section 6: Lancement (ligne 443)
```powershell
& $claudeExe @cmdArgs @passArgs
```
**Rôle** : Lancer Claude avec tous les arguments
**Modifiable** : NON

#### Section 7: Restauration titre (lignes 445-446)
```powershell
# Restaurer le titre après sortie de Claude
$Host.UI.RawUI.WindowTitle = $folderName
```
**Rôle** : Restaurer le titre après exit de Claude
**Modifiable** : NON

## Historique des versions

### v2.1 (Actuelle)
- Resume automatique par défaut (`--continue`)
- `claude .` ou `claude new` pour forcer nouvelle session
- Suppression du check de session existante

### v2.0
- Resume seulement si session existe
- `claude -` ou `claude --new` pour forcer nouveau
- Check filesystem pour détecter .jsonl

### v1.0
- Pas de resume automatique
- MCP auto-détection
- Titre d'onglet avec nom du dossier

## Cas d'usage à valider

Après toute modification, vérifier mentalement ces cas :

| Commande | Comportement attendu |
|----------|---------------------|
| `claude` | Resume automatiquement (ou nouvelle session si aucune) |
| `claude .` | Force nouvelle session |
| `claude new` | Force nouvelle session |
| `claude --help` | Affiche l'aide (avec resume) |
| `claude -m "prompt"` | Passe le prompt (avec resume) |
| `claude` avec .mcp.json | Charge la config MCP + resume |
| Titre d'onglet | Affiche le nom du dossier (pas "claude") |

## Variables importantes

- `$cmdArgs` : Array des arguments pour Claude Code
- `$passArgs` : Array des arguments utilisateur après filtrage
- `$forceNew` : Boolean, true si `.` ou `new` dans les args
- `$folderName` : Nom du dossier courant pour le titre
- `$claudeExe` : Chemin vers l'exécutable Claude Code
