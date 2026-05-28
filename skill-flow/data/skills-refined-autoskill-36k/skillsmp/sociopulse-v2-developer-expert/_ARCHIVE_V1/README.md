# 🗃️ ARCHIVE V1 - Legacy Code

> **Date d'archivage:** 20 Janvier 2026
> **Migration:** V1 → V2 Architecture

## ⚠️ ATTENTION
Ce dossier contient du code **OBSOLÈTE** provenant de la V1 de SocioPulse/MedicoPulse.

**NE PAS IMPORTER** ces fichiers dans la nouvelle architecture.

## 📦 Contenu Archivé

### Pages Archivées (`app/`)
- `/wall/page.tsx` - Ancien mur social (remplacé par `/fil-pro`)
- `/feed/page.tsx` - Ancien feed (remplacé par `/fil-pro`)  
- `/profile/page.tsx` - Ancien profil générique (remplacé par `/dashboard/*/settings` & `/talent/[id]`)
- `/dashboard/page.tsx` - Ancien hub dashboard (remplacé par `/dashboard/client` & `/dashboard/talent`)

### Composants Archivés (`components/`)
- Aucun pour l'instant (les composants wall/ sont encore utilisés par fil-pro)

## 🔄 Nouvelles Routes V2

| V1 (Archivé) | V2 (Actif) |
|--------------|------------|
| `/wall` | `/fil-pro` |
| `/feed` | `/fil-pro` |
| `/profile` | `/dashboard/client/settings` ou `/dashboard/talent/profile` |
| `/dashboard` | `/dashboard/client` ou `/dashboard/talent` |

## 🗑️ Suppression Définitive

Ces fichiers peuvent être supprimés définitivement après validation de la V2 en production.

**Commande de suppression (à exécuter uniquement après validation):**
```bash
rm -rf _ARCHIVE_V1
```
