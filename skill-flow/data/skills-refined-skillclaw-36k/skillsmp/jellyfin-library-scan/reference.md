# Jellyfin Scan - Complete Reference

API documentation and file naming conventions for Jellyfin library scanning.

## API Endpoints

### Base URL
```
http://localhost:8096
```

### Authentication
All requests require API token:
```bash
-H 'X-Emby-Token: YOUR_API_TOKEN'
```

---

### 1. Trigger Full Library Scan

**Endpoint**: `POST /Library/Refresh`

```bash
curl -X POST 'http://localhost:8096/Library/Refresh' \
  -H 'X-Emby-Token: 9af5f56a66e44ee68ddeec7bd07c9db8'
```

**Response**: `204 No Content` (success)

---

### 2. Scan Specific Library

**Endpoint**: `POST /Items/{LibraryId}/Refresh`

**Parameters**:
- `Recursive=true`: Scan all sub-folders
- `ImageRefreshMode=Default`: How to refresh images
- `MetadataRefreshMode=Default`: How to refresh metadata
- `ReplaceAllMetadata=false`: Don't overwrite existing metadata

```bash
curl -X POST 'http://localhost:8096/Items/abc123/Refresh?Recursive=true' \
  -H 'X-Emby-Token: YOUR_TOKEN'
```

---

### 3. Get Library List

**Endpoint**: `GET /Library/VirtualFolders`

```bash
curl -s 'http://localhost:8096/Library/VirtualFolders' \
  -H 'X-Emby-Token: YOUR_TOKEN'
```

**Response**:
```json
[
  {
    "Name": "TV Shows",
    "Locations": ["/media/shows"],
    "CollectionType": "tvshows",
    "ItemId": "d565273fd114d77bdf349a2896867069",
    "LibraryOptions": {...}
  }
]
```

---

### 4. Get Library Counts

**Endpoint**: `GET /Items/Counts`

```bash
curl -s 'http://localhost:8096/Items/Counts' \
  -H 'X-Emby-Token: YOUR_TOKEN'
```

---

### 5. Get Scheduled Tasks

**Endpoint**: `GET /ScheduledTasks`

```bash
curl -s 'http://localhost:8096/ScheduledTasks' \
  -H 'X-Emby-Token: YOUR_TOKEN' | \
  jq '.[] | select(.Name | contains("Scan"))'
```

---

## File Naming Conventions

### TV Shows

#### Format
```
/Shows/Show Name (Year)/Season XX/Show Name - SXXExx - Episode Title.ext
```

#### Examples
```
✅ /media/shows/Naruto (2002)/Season 01/Naruto - S01E01 - Enter Naruto Uzumaki.mkv
✅ /media/shows/Breaking Bad (2008)/Season 05/Breaking Bad - S05E16 - Felina.mkv
✅ /media/shows/Game of Thrones/Season 01/Game.of.Thrones.S01E01.mkv

❌ /media/shows/Naruto/01.mkv  (missing season folder)
❌ /media/shows/[Anime] Naruto - 01.mkv  (wrong format)
❌ /media/shows/Naruto Complete/Episode 001.mkv  (missing SxxExx)
```

#### Multi-Episode Files
```
✅ Naruto - S01E01-E02 - Enter Naruto.mkv
✅ Naruto - S01E01E02.mkv
```

#### Absolute Episode Numbering (Anime)
```
✅ Naruto - 001 - Enter Naruto.mkv  (must enable in library settings)
```

---

### Movies

#### Format
```
/Movies/Movie Name (Year)/Movie Name (Year).ext
```

#### Examples
```
✅ /media/movies/Avatar (2009)/Avatar (2009).mkv
✅ /media/movies/Inception (2010)/Inception (2010).mkv
✅ /media/movies/The Matrix (1999)/The.Matrix.1999.1080p.mkv

❌ /media/movies/Avatar.mkv  (missing year and folder)
❌ /media/movies/Avatar (2009).mkv  (must be in subfolder)
❌ /media/movies/movie1.mkv  (no title)
```

#### Movies with Extras
```
/media/movies/Avatar (2009)/
├── Avatar (2009).mkv
├── extras/
│   ├── Avatar (2009)-trailer.mkv
│   └── Avatar (2009)-behind the scenes.mkv
```

---

### Collections

#### Format
```
/Movies/Collection Name/Movie Name (Year)/Movie Name (Year).ext
```

#### Example
```
/media/movies/Marvel Cinematic Universe/
├── Iron Man (2008)/Iron Man (2008).mkv
├── The Avengers (2012)/The Avengers (2012).mkv
└── Avengers Age of Ultron (2015)/Avengers Age of Ultron (2015).mkv
```

---

## Library Configuration

### Enable Absolute Episode Numbering (Anime)

For anime that uses absolute numbering (1-220 instead of S01E01):

1. Dashboard → Libraries
2. Select library → Manage Library
3. Display → **Prefer absolute episode numbers**

### Real-Time Monitoring

**Enable** (auto-detect new files):
- Good for: Small libraries, fast storage
- Bad for: Large libraries, network mounts (Rclone)

**Disable** (manual scan only):
- Good for: Large libraries, network mounts
- Recommended for: Zurg/Rclone setups

---

## Troubleshooting

### Issue: Content Not Detected After Scan

**Diagnosis**:
```bash
# Check if Jellyfin can see files
docker exec jellyfin ls -la /media/shows/ | grep -i "naruto"

# Check file structure
docker exec jellyfin find /media/shows/Naruto* -type f | head -5
```

**Common Causes**:
1. **Wrong naming format** → Rename files
2. **Mount not accessible** → Restart Rclone
3. **Wrong library type** → Movies in TV library won't work
4. **Hidden/system files** → Check file permissions

---

### Issue: Scan Finds Files But Wrong Metadata

**Diagnosis**:
Check file naming matches conventions exactly

**Solutions**:
1. **Rename files** to match format above
2. **Use Sonarr/Radarr** for automatic renaming
3. **Manual metadata edit** in Jellyfin UI

---

### Issue: Scan Takes >30 Minutes

**Diagnosis**:
```bash
# Count total files
docker exec jellyfin find /media/ -type f | wc -l

# Check for errors
docker logs jellyfin 2>&1 | grep -i "404\|error\|timeout" | wc -l
```

**Solutions**:
1. **Scan specific libraries** instead of all
2. **Remove dead files** (run realdebrid-cleanup)
3. **Disable thumbnail extraction** during scan
4. **Check disk I/O**: `iostat -x 1 5`

---

## Advanced Configuration

### Library Paths

**Config location**:
```
/home/automation/apps/.../config/jellyfin/root/default/{LibraryName}/options.xml
```

**Example**:
```xml
<LibraryOptions>
  <EnablePhotos>false</EnablePhotos>
  <EnableRealtimeMonitor>false</EnableRealtimeMonitor>
  <EnableChapterImageExtraction>false</EnableChapterImageExtraction>
  <PathInfos>
    <MediaPathInfo>
      <Path>/media/shows</Path>
    </MediaPathInfo>
  </PathInfos>
</LibraryOptions>
```

### Scan Performance Tuning

```xml
<!-- Disable expensive operations during scan -->
<EnableChapterImageExtraction>false</EnableChapterImageExtraction>
<EnableTrickplayImageExtraction>false</EnableTrickplayImageExtraction>

<!-- Skip metadata providers (if using NFO files) -->
<DisabledMetadataFetchers>
  <string>TheMovieDb</string>
  <string>TheTVDB</string>
</DisabledMetadataFetchers>
```

---

## Related Documentation

- [SKILL.md](./SKILL.md) - Quick start guide
- [scripts/monitor_scan.py](./scripts/monitor_scan.py) - Monitoring script
- [media-stack-refresh](../media-stack-refresh/SKILL.md) - Full refresh workflow
- Jellyfin Docs: https://jellyfin.org/docs/general/server/media/
