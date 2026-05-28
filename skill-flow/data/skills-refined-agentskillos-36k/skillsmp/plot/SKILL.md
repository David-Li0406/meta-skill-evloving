---
name: plot
description: Annoter visuellement des plots matplotlib et les modifier via référence par couleur
metadata:
  short-description: Annotation visuelle de plots
---

# Skill Plot - Annotation visuelle de plots

Workflow pour annoter des plots matplotlib avec des zones colorées et les modifier par référence.

## Commandes

| Commande | Description |
|----------|-------------|
| `/plot` ou `/plot show` | Affiche le plot actuel et ses annotations |
| `/plot load <chemin>` | Charge une image et lance l'annotateur |
| `/plot annotate` | Lance l'annotateur HTML |
| `/plot zones` | Liste les annotations par groupe |
| `/plot apply` | Applique les modifications au code source |
| `/plot list` | Liste tous les plots sauvegardés |

---

## Pipeline complet

### Étape 1: Charger le plot
```bash
/plot load /chemin/vers/figure.png
```
Actions:
1. Copier l'image vers `~/.claude/plots/current.png`
2. Chercher le script source automatiquement (grep dans le projet)
3. Demander la commande de régénération
4. Sauvegarder les métadonnées
5. Lancer l'annotateur

### Étape 2: Annoter (utilisateur)
L'utilisateur dans le navigateur:
- Zoom/pan pour naviguer
- Dessiner formes + ajouter texte descriptif
- **➕ Nouveau groupe** pour séparer les annotations
- 💾 Sauvegarder

### Étape 3: Appliquer les modifications
```bash
/plot apply
```
Claude:
1. Lit les annotations groupées
2. Pour chaque groupe: forme(s) + texte = une modification
3. Trouve l'élément matplotlib correspondant
4. Modifie le code source
5. Régénère le plot

---

## Format des annotations (JSON)

```json
{
  "zones": [
    {
      "id": "blue",
      "color": "#2196F3",
      "type": "rect",
      "group_id": 2,
      "bbox": [1730, 115, 2266, 300],
      "label": null
    },
    {
      "id": "blue",
      "color": "#2196F3",
      "type": "text",
      "group_id": 2,
      "text": "remplacer Dynamic par Updated",
      "position": [726, 172],
      "label": null
    },
    {
      "id": "red",
      "color": "#F44336",
      "type": "rect",
      "group_id": 3,
      "bbox": [197, 1283, 2299, 1487],
      "label": null
    },
    {
      "id": "red",
      "color": "#F44336",
      "type": "text",
      "group_id": 3,
      "text": "plus petit labels",
      "position": [1758, 1490],
      "label": null
    }
  ],
  "created": "2026-01-22T16:09:51.051Z",
  "plot_name": "current"
}
```

**Interprétation:**
- **Groupe 2 (bleu):** Rectangle sur titre/légende + "remplacer Dynamic par Updated"
- **Groupe 3 (rouge):** Rectangle sur x-axis + "plus petit labels"

---

## Logique de `/plot apply`

### 1. Parser les annotations par groupe
```python
# Pseudo-code
groups = {}
for zone in annotations["zones"]:
    gid = zone["group_id"]
    if gid not in groups:
        groups[gid] = {"shapes": [], "text": None, "color": zone["id"]}
    if zone["type"] == "text":
        groups[gid]["text"] = zone["text"]
    else:
        groups[gid]["shapes"].append(zone)
```

### 2. Pour chaque groupe, identifier la modification
| Zone (bbox) | Texte | Action matplotlib |
|-------------|-------|-------------------|
| Titre (haut centre) | "changer X" | `ax.set_title(...)` |
| Légende | "modifier label" | `ax.legend(...)` ou dans `plot()/scatter()` |
| Axes X (bas) | "plus petit" | `ax.tick_params(axis='x', labelsize=...)` |
| Axes Y (gauche) | "rotation" | `ax.set_ylabel(..., rotation=...)` |
| Points scatter | "enlever bordure" | `scatter(..., edgecolors='none')` |
| Ligne | "changer couleur" | `plot(..., color='...')` |

### 3. Mapper bbox → élément du plot
Pour une image 4200×1650:
- **Titre:** y < 200, x centré
- **Légende:** souvent coin supérieur droit ou selon `loc=`
- **X-axis labels:** y > 1400 (bas)
- **Y-axis labels:** x < 200 (gauche)
- **Zone données:** rectangle central

### 4. Modifier le code source
1. Lire `current_meta.json` pour obtenir `source_script`
2. Trouver la fonction/section qui génère le plot
3. Appliquer la modification (ex: ajouter `labelsize=8`)
4. Sauvegarder le fichier

### 5. Régénérer le plot
```bash
cd {regen_cwd} && {regen_cmd}
```

---

## Actions détaillées par commande

### `/plot show`
```python
# 1. Afficher l'image
Read("~/.claude/plots/current.png")

# 2. Lire métadonnées
meta = Read("~/.claude/plots/current_meta.json")

# 3. Lire annotations
annotations = Read("~/.claude/plots/current_annotations.json")

# 4. Résumer par groupe
for group_id, items in group_by(annotations, "group_id"):
    shapes = [i for i in items if i["type"] != "text"]
    text = next((i["text"] for i in items if i["type"] == "text"), None)
    print(f"Groupe {group_id}: {len(shapes)} forme(s), instruction: {text}")
```

### `/plot annotate`
Lance l'annotateur vide (sans image). L'utilisateur peut drag & drop ou cliquer "current.png".
```bash
fuser -k 8888/tcp 2>/dev/null || true
sleep 1
python3 ~/.claude/tools/annotate_server.py &
sleep 2
xdg-open "http://localhost:8888/annotate.html"  # Sans ?load=true → démarre vide
```

### `/plot zones`
Lire et afficher `current_annotations.json` groupé par `group_id`.

### `/plot load <chemin>`
1. `cp <chemin> ~/.claude/plots/current.png`
2. Chercher script source:
   ```bash
   # Extraire nom fichier
   filename=$(basename <chemin> .png)
   # Trouver projet root
   project_root=$(git -C $(dirname <chemin>) rev-parse --show-toplevel 2>/dev/null)
   # Chercher dans les .py
   grep -r "$filename" --include="*.py" "$project_root"
   ```
3. Demander commande regen (AskUserQuestion)
4. Sauver métadonnées
5. Lancer annotateur avec `?load=true` pour charger l'image automatiquement:
   ```bash
   fuser -k 8888/tcp 2>/dev/null || true
   sleep 1
   python3 ~/.claude/tools/annotate_server.py &
   sleep 2
   xdg-open "http://localhost:8888/annotate.html?load=true"
   ```

### `/plot apply`
**IMPORTANT:** Suivre cette logique exacte avec CONFIRMATION OBLIGATOIRE:

1. **Lire les fichiers**
   ```
   annotations = ~/.claude/plots/current_annotations.json
   meta = ~/.claude/plots/current_meta.json
   ```

2. **Grouper les annotations**
   ```
   Pour chaque group_id unique:
     - Collecter les formes (rect, circle, line)
     - Extraire le texte (instruction)
   ```

3. **Pour chaque groupe, analyser:**
   - Où pointe la forme? (bbox → élément matplotlib)
   - Que demande le texte? (instruction)

4. **Lire le code source** (`meta.source_script`)

5. **AFFICHER UN RÉSUMÉ DÉTAILLÉ** (NE PAS MODIFIER ENCORE!)
   ```markdown
   ## Modifications proposées

   **Fichier:** `/chemin/vers/script.py`

   ### Groupe X (couleur):
   - **Zone ciblée:** [description de l'élément, ex: "Titre principal", "Légende", "Labels axe X"]
   - **Instruction:** "texte de l'annotation"
   - **Modification proposée:**
     - Ligne ~XX: `ancien_code`
     - Devient: `nouveau_code`

   ### Groupe Y (couleur):
   - **Zone ciblée:** ...
   - **Instruction:** ...
   - **Modification proposée:** ...

   ---
   **Confirmer ces modifications?** (oui/non)
   ```

6. **ATTENDRE LA CONFIRMATION EXPLICITE**
   - Si "oui" → procéder aux modifications
   - Si "non" → demander ce qui doit être ajusté
   - NE JAMAIS modifier le code sans confirmation!

7. **Appliquer les modifications** (seulement après confirmation)

8. **Régénérer** si `regen_cmd` disponible

---

## Contrôles de l'annotateur

| Action | Contrôle |
|--------|----------|
| Zoom | Molette souris |
| Pan | Espace+drag, Clic-droit+drag, ou bouton ✋ |
| Dessiner | Choisir outil (rect/circle/line/freedraw/text) |
| Texte | Outil 📝 + clic → modal stylée (Enter=OK, Esc=annuler) |
| Nouveau groupe | Bouton ➕ (sépare les annotations) |
| Labels | Bouton 🏷️ → panneau latéral |
| Sauvegarder | Bouton 💾 (auto-save sur disque) |
| Supprimer | Sélection + Delete |

---

## Fichiers

| Fichier | Contenu |
|---------|---------|
| `~/.claude/plots/current.png` | Plot actuel (sauvegardé auto quand user drop + save) |
| `~/.claude/plots/current_annotated.png` | Plot avec annotations visuelles |
| `~/.claude/plots/current_meta.json` | Métadonnées (source_script détecté auto) |
| `~/.claude/plots/current_annotations.json` | Zones annotées avec group_id |
| `~/.claude/tools/annotate.html` | App HTML (Fabric.js) |
| `~/.claude/tools/annotate_server.py` | Serveur Python (port 8888) |

## Détection automatique

Quand l'utilisateur drop une image dans l'annotateur et clique Save:
1. L'image de fond → `current.png`
2. Le nom du fichier est envoyé au serveur
3. Le serveur cherche dans les projets connus (`grep -r "filename" --include="*.py"`)
4. Si trouvé → `current_meta.json` est mis à jour avec `source_script`

**Projets scannés:**
- Dossiers des précédents `/plot load`
- `~/Github`, `/media/*/Data/Github`

---

## Couleurs disponibles

| Couleur | Hex | Usage suggéré |
|---------|-----|---------------|
| blue | #2196F3 | Annotations principales |
| red | #F44336 | Erreurs, suppressions |
| green | #4CAF50 | Validations, OK |
| yellow | #FFEB3B | Attention, warnings |
| orange | #FF9800 | Modifications secondaires |
| purple | #9C27B0 | Notes spéciales |

---

## Exemple complet

```
Utilisateur: /plot load /media/data/outputs/fig_trends.png

Claude: Plot chargé.
- Source: /media/data/scripts/plot_trends.py
- Commande regen: python scripts/plot_trends.py --output outputs/
- Annotateur: http://localhost:8888/annotate.html

[Utilisateur annote: rect bleu sur légende + texte "Dynamic → Updated"]
[Utilisateur annote: rect rouge sur x-axis + texte "smaller font"]
[Utilisateur clique 💾]

Utilisateur: /plot apply

Claude: J'ai analysé 2 groupes d'annotations. Voici les modifications proposées:

---
## Modifications proposées

**Fichier:** `/media/data/scripts/plot_trends.py`

### Groupe 2 (bleu) - Légende
- **Zone ciblée:** Légende (bbox: 2491,1146 → 3054,1301)
- **Instruction:** "Dynamic → Updated"
- **Modification proposée:**
  - Ligne 45: `label='Dynamic (Sentinel-2)'`
  - Devient: `label='Updated (Sentinel-2)'`

### Groupe 3 (rouge) - Labels axe X
- **Zone ciblée:** Labels axe X (bbox: 197,1283 → 2299,1487)
- **Instruction:** "smaller font"
- **Modification proposée:**
  - Ajouter après ligne 52: `ax.tick_params(axis='x', labelsize=8)`

---
**Confirmer ces modifications?** (oui/non)

Utilisateur: oui

Claude: Modifications appliquées ✓
- Ligne 45: label mis à jour
- Ligne 53: tick_params ajouté

Régénération du plot...
[Commande exécutée]

✅ Nouveau plot généré. Voici le résultat:
[Affiche le nouveau plot]
```
