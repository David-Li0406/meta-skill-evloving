# CrossPoint device API

API reference for Xteink X4 running CrossPoint firmware.

## connection

| property | value |
|----------|-------|
| IP | 10.0.0.61 (preferred) |
| hostname | crosspoint.local (flaky DNS) |
| port | 80 (HTTP) |
| prerequisite | device in file transfer mode |

## endpoints

### list files

```
GET /api/files?path=/
```

response:
```json
[
  {"name": "folder", "isDirectory": true},
  {"name": "file.epub", "size": 12345, "isDirectory": false, "isEpub": true}
]
```

### upload file

```
POST /upload?path=/target/folder
Content-Type: multipart/form-data

file: <binary epub data>
```

### create folder

```
POST /mkdir
Content-Type: application/x-www-form-urlencoded

name=FolderName&path=/parent
```

### delete file/folder

```
POST /delete
Content-Type: application/x-www-form-urlencoded

path=/full/path/to/item&type=file|folder
```

## epub CLI mapping

| API endpoint | epub CLI command |
|--------------|------------------|
| GET /api/files | `epub device files --ip 10.0.0.61 [path]` |
| POST /upload | `epub device sync --ip 10.0.0.61` |
| POST /mkdir | `epub device mkdir --ip 10.0.0.61 <name>` |
| POST /delete | `epub device delete --ip 10.0.0.61 <path>` |

## device detection

check if device is reachable:

```bash
curl -s --max-time 3 http://10.0.0.61/ | grep -q "CrossPoint" && echo "ready"
```

via epub CLI:

```bash
epub device files --ip 10.0.0.61 / 2>/dev/null && echo "ready"
```

## file transfer mode

to enable file transfer on X4:
1. power on device
2. navigate to Settings > File Transfer
3. enable WiFi transfer
4. wait for IP to appear on screen

note: device must be on same network as computer.

## timeouts

| operation | recommended timeout |
|-----------|---------------------|
| connection check | 3s |
| file list | 10s |
| upload (per file) | 60s |
| folder create | 10s |
| delete | 10s |

## error handling

| error | cause | fix |
|-------|-------|-----|
| connection refused | device not in file transfer mode | enable on device |
| timeout | wrong IP or device off | verify IP, check device |
| 404 | path doesn't exist | check path spelling |
| 500 | device storage full | delete old files |
