# Media Stack Refresh - Troubleshooting Reference

Detailed troubleshooting for each step of the media stack refresh workflow.

## Step-by-Step Troubleshooting

### Step 1: Zurg Not Rebuilding Database

**Symptom**: Zurg logs show same torrent count after restart

**Diagnosis**:
```bash
docker logs zurg 2>&1 | grep -i "compiled\|torrents" | tail -5
```

**Solutions**:

1. **Clear Zurg cache**:
   ```bash
   docker stop zurg
   rm /home/automation/apps/.../config/zurg/cache/* 2>/dev/null
   docker start zurg
   ```

2. **Check Zurg config**:
   ```bash
   docker logs zurg 2>&1 | grep -i "error\|fail"
   ```

3. **Verify Real-Debrid API**:
   ```bash
   curl -s 'https://api.real-debrid.com/rest/1.0/user' \
     -H 'Authorization: Bearer YOUR_KEY' | jq .premium
   ```

---

### Step 2: Rclone Shows Old Data After Restart

**Symptom**: Deleted torrents still visible in `/mnt/rd/`

**Diagnosis**:
```bash
# Check if Rclone running
docker ps | grep rclone

# Check Rclone logs for errors
docker logs rclone --tail 50
```

**Solutions**:

1. **Force clear VFS cache**:
   ```bash
   docker exec rclone rclone rc vfs/forget
   docker restart rclone
   sleep 15
   ```

2. **Check Rclone config**:
   ```bash
   docker exec rclone rclone config show
   ```

3. **Nuclear option - restart Docker**:
   ```bash
   sudo systemctl restart docker
   sleep 30
   cd /home/automation/apps/14-media-servers/jellyfin-stack
   docker-compose up -d
   ```

---

### Step 3: Mount Not Accessible

**Symptom**: `ls /mnt/rd/` returns "Transport endpoint not connected"

**Diagnosis**:
```bash
# Check if mount exists
mount | grep "/mnt/rd"

# Check Rclone container
docker ps | grep rclone

# Check for errors
docker logs rclone 2>&1 | grep -i "error\|fail" | tail -20
```

**Solutions**:

1. **Remount**:
   ```bash
   docker restart rclone
   sleep 15
   ls /mnt/rd/shows/ | head -5
   ```

2. **Check Zurg is responding**:
   ```bash
   curl http://localhost:9999/debug/torrents | jq length
   ```

3. **Restart entire stack**:
   ```bash
   cd /home/automation/apps/14-media-servers/jellyfin-stack
   docker-compose restart zurg rclone
   sleep 30
   ```

---

### Step 4: Jellyfin Won't Start

**Symptom**: Jellyfin container restarting loop

**Diagnosis**:
```bash
docker ps | grep jellyfin
docker logs jellyfin --tail 100
```

**Common Causes**:

1. **Disk space full**:
   ```bash
   df -h | grep -E '/dev/sda1'
   # If >95%, run docker-cleanup skill
   ```

2. **Database corruption**:
   ```bash
   # Check last logs before crash
   docker logs jellyfin 2>&1 | grep -i "database\|sqlite" | tail -20
   ```

3. **Mount not ready**:
   ```bash
   # Ensure mount accessible first
   docker exec jellyfin ls /media/shows/ | wc -l
   ```

**Solutions**:

1. **Free disk space** (see docker-cleanup skill)

2. **Restore from backup**:
   ```bash
   /home/automation/scripts/restore-media-stack.sh [backup-file]
   ```

3. **Wait for mount then restart**:
   ```bash
   # Ensure Rclone healthy first
   docker restart rclone && sleep 30
   docker restart jellyfin
   ```

---

### Step 5: Jellyfin Scan Doesn't Start

**Symptom**: Scan API call succeeds but no activity in logs

**Diagnosis**:
```bash
# Check if scan task running
docker logs jellyfin --follow | grep -i "scan\|library\|validat"

# Check scheduled tasks
curl -s 'http://localhost:8096/ScheduledTasks' \
  -H 'X-Emby-Token: YOUR_TOKEN' | \
  jq '.[] | select(.Name | contains("Scan"))'
```

**Solutions**:

1. **Force refresh specific library**:
   ```bash
   # Get library ID
   curl -s 'http://localhost:8096/Library/VirtualFolders' \
     -H 'X-Emby-Token: YOUR_TOKEN' | jq '.[] | {Name, ItemId}'

   # Trigger refresh
   curl -X POST 'http://localhost:8096/Items/{ItemId}/Refresh?Recursive=true' \
     -H 'X-Emby-Token: YOUR_TOKEN'
   ```

2. **Check API token valid**:
   ```bash
   curl -s 'http://localhost:8096/System/Info' \
     -H 'X-Emby-Token: YOUR_TOKEN' | jq .ServerName
   ```

3. **Restart Jellyfin and retry**:
   ```bash
   docker restart jellyfin && sleep 30
   curl -X POST 'http://localhost:8096/Library/Refresh' \
     -H 'X-Emby-Token: YOUR_TOKEN'
   ```

---

### Step 6: Scan Takes Forever (>30 minutes)

**Symptom**: Scan running but very slow

**Diagnosis**:
```bash
# Check disk I/O
iostat -x 1 5

# Check Jellyfin CPU usage
docker stats jellyfin --no-stream

# Count files being scanned
docker exec jellyfin find /media/shows/ -type f | wc -l
```

**Solutions**:

1. **Scan specific library only** (not all libraries)

2. **Disable thumbnail extraction during scan**:
   - Dashboard → Scheduled Tasks
   - "Extract chapter images" → Disable

3. **Check for 404 errors** (dead files slow scan):
   ```bash
   docker logs jellyfin 2>&1 | grep -i "404\|not found" | wc -l
   # If many, run realdebrid-cleanup skill first
   ```

---

### Step 7: Content Still Missing After Scan

**Symptom**: Scan completed but content not detected

**Diagnosis**:
```bash
# Check if Jellyfin can see files
docker exec jellyfin ls -la /media/shows/ | grep -i "naruto"

# Check file naming
docker exec jellyfin find /media/shows/Naruto* -type f | head -5
```

**Common Causes**:

1. **Wrong library path**:
   ```bash
   # Check library config
   cat /home/automation/apps/.../config/jellyfin/root/default/*/options.xml | grep PathInfos
   ```

2. **File naming doesn't match Jellyfin patterns**:
   ```
   Good: /media/shows/Naruto (2002)/Season 01/Naruto S01E01.mkv
   Bad:  /media/shows/[Anime] Naruto - 01.mkv
   ```

3. **Mount not accessible from container**:
   ```bash
   docker exec jellyfin df -h | grep /media
   ```

**Solutions**:

1. **Check library path configuration**
2. **Rename files** (use Sonarr for automated renaming)
3. **Verify mount** inside container

---

## Emergency Recovery

If entire stack is broken:

```bash
cd /home/automation/apps/14-media-servers/jellyfin-stack

# Stop everything
docker-compose down

# Wait 10 seconds
sleep 10

# Start in order
docker-compose up -d zurg
sleep 15
docker-compose up -d rclone
sleep 15
docker-compose up -d jellyfin sonarr radarr prowlarr bazarr jellyseerr

# Verify
docker-compose ps
```

## Related Documentation

- [SKILL.md](./SKILL.md) - Quick start workflow
- [scripts/full_refresh.sh](./scripts/full_refresh.sh) - Automated script
- [realdebrid-cleanup](../realdebrid-cleanup/SKILL.md) - Pre-refresh cleanup
- [jellyfin-scan](../jellyfin-scan/SKILL.md) - Scan monitoring
- [health-check](../health-check.md) - Post-refresh verification
