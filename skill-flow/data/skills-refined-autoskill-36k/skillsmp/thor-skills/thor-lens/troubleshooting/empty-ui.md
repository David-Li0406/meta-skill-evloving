# Empty UI

The web UI shows nothing, has no events, or displays a blank timeline.

## Quick Diagnosis

### 1. Check API Returns Data

```bash
curl http://127.0.0.1:8080/api/meta | jq .
```

**If this returns data**: UI issue (browser/frontend)
**If this returns empty/error**: Backend/import issue

### 2. Check Event Count

```bash
curl http://127.0.0.1:8080/api/meta | jq '.event_count'
```

**If 0**: Import failed or wrong input file
**If > 0**: Check filters in UI

## Common Causes

### Wrong Input File (Not Audit Trail)

**Symptom**: Import "succeeds" but 0 events

**Cause**: Imported a regular THOR log instead of audit trail

**Diagnosis**:
```bash
# Check first line of input file
head -1 /path/to/your/file.jsonl | jq .

# Audit trail has fields like:
# {"type": "...", "object": {...}, "timestamps": {...}}

# Regular JSON log has fields like:
# {"level": "...", "message": "...", "module": "..."}
```

**Solution**: Generate audit trail with THOR v11:
```bash
./thor-linux-64 --lab -p /target --audit-trail output.jsonl
```

### THOR v10 Used (No Audit Trail Support)

**Symptom**: File exists but format is wrong or empty

**Cause**: THOR v10 doesn't support `--audit-trail` flag

**Diagnosis**:
```bash
# Check THOR version
./thor-linux-64 --version
# Must be v11.x
```

**Solution**: Use THOR v11 for audit trail generation

### Import Pointed to Wrong File

**Symptom**: Import succeeds but wrong data

**Diagnosis**:
```bash
# Check what was imported
cat ./cases/mycase/meta.json | jq '.source_file'
```

**Solution**: Re-import with correct file:
```bash
rm -rf ./cases/mycase
./thorlens import --log /correct/path/audit.jsonl --case mycase
```

### Permission Issues

**Symptom**: Server starts but can't read case

**Diagnosis**:
```bash
ls -la ./cases/mycase/
ls -la ./cases/mycase/events/
```

**Solution**: Fix permissions:
```bash
chmod -R u+r ./cases/mycase/
```

### UI Filters Hiding Events

**Symptom**: API shows events but UI is empty

**Causes**:
- Time range filter excludes all events
- Object type filter excludes all events
- Search filter matches nothing
- Exclusion filters hiding everything

**Solution**:
1. Clear all filters in UI
2. Reset time range to "All"
3. Clear search box
4. Check exclusion filters list

### Browser Cache

**Symptom**: UI behaves strangely after update

**Solution**:
1. Hard refresh: Ctrl+Shift+R (Cmd+Shift+R on Mac)
2. Clear browser cache
3. Try incognito/private window

## Verification Steps

### 1. Verify Case Structure

```bash
ls -la ./cases/mycase/
```

Expected:
```
meta.json
events/
annotations.sqlite
```

### 2. Verify Parquet Files Exist

```bash
find ./cases/mycase/events -name "*.parquet" | wc -l
# Should be > 0
```

### 3. Verify Meta Has Data

```bash
cat ./cases/mycase/meta.json | jq '.event_count'
# Should be > 0
```

### 4. Test API Endpoints

```bash
# Metadata
curl http://127.0.0.1:8080/api/meta | jq .

# Events (first 10)
curl "http://127.0.0.1:8080/api/events?limit=10" | jq .

# Buckets
curl http://127.0.0.1:8080/api/buckets | jq .
```

## Starting Fresh

If nothing works, re-import:

```bash
# Backup annotations if you have any
cp ./cases/mycase/annotations.sqlite ./annotations_backup.sqlite

# Remove case
rm -rf ./cases/mycase

# Re-import
./thorlens import --log /path/to/audit.jsonl --case mycase

# Verify
cat ./cases/mycase/meta.json | jq '.event_count'
```
