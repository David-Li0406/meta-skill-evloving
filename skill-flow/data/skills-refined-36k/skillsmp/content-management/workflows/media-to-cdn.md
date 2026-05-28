---
name: media-to-cdn
description: Workflow automatisé - De l'upload média à la distribution CDN optimisée
version: 1.0.0
---

# Workflow : Upload Média → Distribution CDN

Ce workflow montre comment l'agence IA traite automatiquement un fichier média uploadé jusqu'à sa distribution optimisée sur CDN.

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     WORKFLOW MEDIA → CDN (< 5 min)                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   UPLOAD             PROCESS             CATALOG            DISTRIBUTE           │
│                                                                                  │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │  FILE    │─────►│ VALIDATE │──────►│ METADATA │──────►│   CDN    │         │
│   │  UPLOAD  │      │  FORMAT  │       │   TAGS   │       │  UPLOAD  │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│        │                 │                   │                  │               │
│        ▼                 ▼                   ▼                  ▼               │
│   ┌──────────┐      ┌──────────┐       ┌──────────┐       ┌──────────┐         │
│   │  TYPE    │      │ OPTIMIZE │       │ LIBRARY  │       │  PURGE   │         │
│   │ DETECT   │      │ COMPRESS │       │  INDEX   │       │  CACHE   │         │
│   └──────────┘      └──────────┘       └──────────┘       └──────────┘         │
│                                                                                  │
│   ~10 sec            ~30-120 sec          ~10 sec            ~30 sec            │
│                                                                                  │
│   TOTAL: 1-3 min (100% automatisé)                                              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Triggers

```yaml
triggers:
  - type: upload
    endpoints:
      - /api/media/upload
      - /admin/media/upload
    max_size: 100MB

  - type: webhook
    source: dropbox
    events: [file.added]
    folder: /assets/

  - type: webhook
    source: google-drive
    events: [file.created]
    folder: "Shared Assets"

  - type: batch
    cron: "0 2 * * *"  # 2h du matin
    action: process_pending_uploads
```

---

## Phase 1 : Upload & Détection (10 sec)

### 1.1 Réception fichier

| Étape | Skill | Agent | Input | Output |
|-------|-------|-------|-------|--------|
| Recevoir upload | content-management | assets/media-manager | File stream | Temp file |
| Détecter type | content-management | assets/media-manager | File | MIME type |

```json
{
  "upload": {
    "upload_id": "UPL-2025-001234",
    "filename": "hero-banner-spring.png",
    "original_size": 2457600,
    "mime_type": "image/png",
    "dimensions": {
      "width": 2400,
      "height": 1200
    },
    "temp_path": "/tmp/uploads/UPL-2025-001234.png",
    "checksum": "sha256:abc123...",
    "uploaded_by": "designer-001",
    "uploaded_at": "2025-01-10T14:30:00Z"
  }
}
```

### 1.2 Validation initiale

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Valider format | content-management | assets/media-manager | Format OK |
| Vérifier dimensions | content-management | assets/media-manager | Dims OK |
| Scan sécurité | content-management | assets/media-manager | Clean |

```json
{
  "validation": {
    "upload_id": "UPL-2025-001234",
    "checks": {
      "format_supported": { "status": "passed", "format": "PNG" },
      "dimensions": { "status": "passed", "min": true, "max": true },
      "file_size": { "status": "passed", "under_limit": true },
      "security_scan": { "status": "passed", "malware": false },
      "duplicate_check": { "status": "passed", "is_unique": true }
    },
    "overall": "PASSED",
    "proceed": true
  }
}
```

---

## Phase 2 : Traitement & Optimisation (30-120 sec)

### 2.1 Pipeline images

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Générer variantes | content-management | assets/image-optimizer | Multiple sizes |
| Convertir WebP | content-management | assets/image-optimizer | WebP versions |
| Compresser | content-management | assets/image-optimizer | Optimized |

```json
{
  "image_processing": {
    "upload_id": "UPL-2025-001234",
    "source": {
      "format": "PNG",
      "size_bytes": 2457600,
      "dimensions": "2400x1200"
    },
    "outputs": [
      {
        "variant": "original",
        "format": "webp",
        "dimensions": "2400x1200",
        "size_bytes": 185400,
        "quality": 90
      },
      {
        "variant": "1600w",
        "format": "webp",
        "dimensions": "1600x800",
        "size_bytes": 98200,
        "quality": 85
      },
      {
        "variant": "1200w",
        "format": "webp",
        "dimensions": "1200x600",
        "size_bytes": 62100,
        "quality": 85
      },
      {
        "variant": "800w",
        "format": "webp",
        "dimensions": "800x400",
        "size_bytes": 34500,
        "quality": 85
      },
      {
        "variant": "400w",
        "format": "webp",
        "dimensions": "400x200",
        "size_bytes": 12800,
        "quality": 80
      },
      {
        "variant": "thumbnail",
        "format": "webp",
        "dimensions": "150x75",
        "size_bytes": 4200,
        "quality": 75
      }
    ],
    "fallback": {
      "format": "jpeg",
      "variants": ["1200w", "800w"],
      "total_size": 142000
    },
    "compression": {
      "original_total": 2457600,
      "optimized_total": 539200,
      "reduction_percent": 78.1
    }
  }
}
```

### 2.2 Pipeline vidéos (si applicable)

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Transcoder | content-management | assets/video-handler | HLS/DASH |
| Générer thumbnails | content-management | assets/video-handler | Thumbnails |
| Extraire metadata | content-management | assets/video-handler | Duration, codec |

```json
{
  "video_processing": {
    "upload_id": "UPL-2025-005678",
    "source": {
      "format": "MP4",
      "codec": "H.264",
      "duration": 125,
      "resolution": "1920x1080",
      "size_bytes": 52428800
    },
    "outputs": {
      "hls": {
        "master_playlist": "/videos/VID-001/master.m3u8",
        "variants": ["1080p", "720p", "480p", "360p"]
      },
      "thumbnails": [
        { "time": 0, "url": "/thumbs/VID-001-0.jpg" },
        { "time": 30, "url": "/thumbs/VID-001-30.jpg" },
        { "time": 60, "url": "/thumbs/VID-001-60.jpg" }
      ],
      "preview_gif": "/previews/VID-001.gif"
    },
    "processing_time": "45s"
  }
}
```

---

## Phase 3 : Catalogage (10 sec)

### 3.1 Extraction métadonnées

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Extraire EXIF | content-management | assets/media-manager | EXIF data |
| Générer alt-text | content-management | assets/media-manager | AI alt-text |
| Auto-tagger | content-management | assets/media-manager | Tags |

```json
{
  "metadata": {
    "asset_id": "ASSET-2025-001234",
    "extracted": {
      "camera": null,
      "date_taken": null,
      "gps": null,
      "color_profile": "sRGB"
    },
    "generated": {
      "alt_text": "Bannière promotionnelle printemps avec fleurs colorées sur fond pastel",
      "description": "Image hero pour campagne marketing printemps 2025",
      "dominant_colors": ["#FFB6C1", "#98FB98", "#87CEEB"],
      "content_type": "promotional",
      "suggested_tags": ["banner", "spring", "flowers", "pastel", "marketing"]
    }
  }
}
```

### 3.2 Indexation bibliothèque

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Créer entrée | content-management | assets/media-manager | Asset record |
| Indexer recherche | content-management | assets/media-manager | Searchable |

```json
{
  "catalog_entry": {
    "asset_id": "ASSET-2025-001234",
    "filename": "hero-banner-spring-2025",
    "path": "/images/banners/spring-2025/",
    "type": "image",
    "metadata": {
      "title": "Bannière Printemps 2025",
      "alt_text": "Bannière promotionnelle printemps...",
      "author": "designer-001",
      "created_at": "2025-01-10T14:30:00Z",
      "expires_at": null
    },
    "tags": ["banner", "spring", "campaign", "hero", "2025"],
    "usage": {
      "license": "proprietary",
      "projects": [],
      "usage_count": 0
    },
    "search_index": {
      "indexed": true,
      "keywords": ["bannière", "printemps", "fleurs", "campagne", "marketing"]
    }
  }
}
```

---

## Phase 4 : Distribution CDN (30 sec)

### 4.1 Upload CDN

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Upload vers CDN | devops | deployment/cdn | CDN URLs |
| Configurer headers | devops | deployment/cdn | Cache headers |

```json
{
  "cdn_upload": {
    "asset_id": "ASSET-2025-001234",
    "provider": "cloudflare",
    "uploads": [
      {
        "variant": "original",
        "cdn_url": "https://cdn.acme.fr/images/banners/spring-2025/hero-banner-spring-2025.webp",
        "cache_control": "public, max-age=31536000, immutable"
      },
      {
        "variant": "1600w",
        "cdn_url": "https://cdn.acme.fr/images/banners/spring-2025/hero-banner-spring-2025-1600w.webp"
      },
      {
        "variant": "1200w",
        "cdn_url": "https://cdn.acme.fr/images/banners/spring-2025/hero-banner-spring-2025-1200w.webp"
      },
      {
        "variant": "800w",
        "cdn_url": "https://cdn.acme.fr/images/banners/spring-2025/hero-banner-spring-2025-800w.webp"
      },
      {
        "variant": "400w",
        "cdn_url": "https://cdn.acme.fr/images/banners/spring-2025/hero-banner-spring-2025-400w.webp"
      },
      {
        "variant": "thumbnail",
        "cdn_url": "https://cdn.acme.fr/images/banners/spring-2025/hero-banner-spring-2025-thumb.webp"
      }
    ],
    "edge_locations": ["Paris", "Frankfurt", "London", "Amsterdam"],
    "ssl": true
  }
}
```

### 4.2 Génération code embed

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Générer srcset | content-management | assets/image-optimizer | HTML code |
| Créer picture | content-management | assets/image-optimizer | Picture element |

```html
<!-- Code généré automatiquement -->
<picture>
  <!-- WebP (modern browsers) -->
  <source
    type="image/webp"
    srcset="
      https://cdn.acme.fr/.../hero-banner-spring-2025-400w.webp 400w,
      https://cdn.acme.fr/.../hero-banner-spring-2025-800w.webp 800w,
      https://cdn.acme.fr/.../hero-banner-spring-2025-1200w.webp 1200w,
      https://cdn.acme.fr/.../hero-banner-spring-2025-1600w.webp 1600w,
      https://cdn.acme.fr/.../hero-banner-spring-2025.webp 2400w
    "
    sizes="(max-width: 600px) 100vw,
           (max-width: 1200px) 50vw,
           1200px"
  />
  <!-- JPEG fallback -->
  <source
    type="image/jpeg"
    srcset="
      https://cdn.acme.fr/.../hero-banner-spring-2025-800w.jpg 800w,
      https://cdn.acme.fr/.../hero-banner-spring-2025-1200w.jpg 1200w
    "
  />
  <!-- Fallback img -->
  <img
    src="https://cdn.acme.fr/.../hero-banner-spring-2025-1200w.webp"
    alt="Bannière promotionnelle printemps avec fleurs colorées sur fond pastel"
    width="2400"
    height="1200"
    loading="lazy"
    decoding="async"
  />
</picture>
```

### 4.3 Purge cache (si remplacement)

| Étape | Skill | Agent | Output |
|-------|-------|-------|--------|
| Purge ancien | devops | deployment/cdn | Cache purged |
| Warm cache | devops | deployment/cdn | Cache warmed |

```json
{
  "cache_management": {
    "asset_id": "ASSET-2025-001234",
    "action": "new_upload",
    "purge": null,
    "warm": {
      "urls_warmed": 6,
      "locations": ["Paris", "Frankfurt"],
      "status": "completed"
    }
  }
}
```

---

## Phase 5 : Confirmation (instantané)

### 5.1 Réponse API

```json
{
  "success": true,
  "asset": {
    "id": "ASSET-2025-001234",
    "filename": "hero-banner-spring-2025",
    "urls": {
      "original": "https://cdn.acme.fr/.../hero-banner-spring-2025.webp",
      "thumbnail": "https://cdn.acme.fr/.../hero-banner-spring-2025-thumb.webp"
    },
    "embed_code": "<picture>...</picture>",
    "library_url": "/admin/media/ASSET-2025-001234"
  },
  "processing": {
    "duration_ms": 2340,
    "compression_ratio": 78.1
  }
}
```

### 5.2 Notification (optionnel)

```
✅ Asset uploadé avec succès

📁 hero-banner-spring-2025.webp
📊 2.4 MB → 185 KB (-78%)
🌍 CDN: 4 edge locations
🔗 6 variantes générées

[Voir dans la bibliothèque] [Copier l'URL]
```

---

## Métriques du Workflow

| Métrique | Cible | Mesuré |
|----------|-------|--------|
| Temps total | < 3 min | ~2 min |
| Compression moyenne | > 70% | 78% |
| Taux d'automatisation | 100% | 100% |
| Disponibilité CDN | < 30 sec | ~20 sec |
| Erreurs | < 1% | 0.2% |

## Types de Fichiers Supportés

| Type | Extensions | Traitement |
|------|------------|------------|
| Images | jpg, png, gif, webp, svg | Compression, resize, conversion |
| Vidéos | mp4, webm, mov | Transcoding HLS/DASH |
| Documents | pdf | Thumbnail, OCR (optionnel) |
| Audio | mp3, wav | Normalisation, metadata |

## Points d'Escalade

| Condition | Action |
|-----------|--------|
| Fichier > 100MB | Queue batch processing |
| Format non supporté | Reject + notify |
| Scan sécurité failed | Block + alert security |
| CDN unavailable | Queue + retry |
| Duplicate detected | Prompt user action |

## Références

- [content-management/SKILL.md](../SKILL.md)
- [devops/SKILL.md](../../devops/SKILL.md)
