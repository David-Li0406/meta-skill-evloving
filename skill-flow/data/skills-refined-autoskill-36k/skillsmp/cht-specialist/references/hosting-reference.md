# CHT Hosting and Deployment Reference

## Requirements

### App Developer Hosting (Docker)

| Resource | Minimum |
|----------|---------|
| RAM | 4 GB |
| CPU | 2 cores |
| Storage | 8 GB SSD |
| Root Access | Required |
| TLS Certificates | Required (CHT Docker Helper provides these automatically) |
| Docker | Current version with `docker compose` |

### Production Hosting - Docker

| Resource | Minimum |
|----------|---------|
| RAM | 8 GB |
| CPU | 4 cores |
| Storage | 100 GB SSD |
| Root Access | Required |
| Static IP | Required with DNS entry for TLS certificate provisioning |
| Docker | Current version with `docker compose` |

### Production Hosting - Kubernetes (K3s)

| Component | Specification |
|-----------|---------------|
| HA Control-plane nodes | 1 x 2 GB RAM / 2 CPU / 20 GB SSD |
| Worker servers | 3 x 16 GB RAM / 8 CPU / 50 GB SSD |
| Storage Area Network (SAN) | 500 GB for Persistent Volume Claims |
| Root Access | Required |
| Static IP | Required with DNS entry |
| Additional Tools | `helm`, K3s, Docker |

**Important**: During some upgrades, up to 5x current space used by CouchDB may be needed.

---

## Docker Installation

### Directory Structure

```shell
mkdir -p /home/ubuntu/cht/{compose,certs,upgrade-service,couchdb}
```

Directory purposes:
- `compose/` - Docker Compose files for cht-core and CouchDB
- `certs/` - TLS certificates directory
- `upgrade-service/` - Docker Compose file for the upgrade service
- `couchdb/` - CouchDB data path

### Download Docker Compose Files

```shell
cd /home/ubuntu/cht/
curl -s -o ./compose/cht-core.yml https://staging.dev.medicmobile.org/_couch/builds_4/medic:medic:4.21.1/docker-compose/cht-core.yml
curl -s -o ./compose/cht-couchdb.yml https://staging.dev.medicmobile.org/_couch/builds_4/medic:medic:4.21.1/docker-compose/cht-couchdb.yml
curl -s -o ./upgrade-service/docker-compose.yml https://raw.githubusercontent.com/medic/cht-upgrade-service/main/docker-compose.yml
```

### Prepare Environment Variables

```shell
sudo apt install wamerican uuid-runtime
uuid=$(uuidgen)
couchdb_secret=$(shuf -n7 /usr/share/dict/words --random-source=/dev/random | tr '\n' '-' | tr -d "'" | cut -d'-' -f1,2,3,4,5,6,7)
couchdb_password=$(shuf -n7 /usr/share/dict/words --random-source=/dev/random | tr '\n' '-' | tr -d "'" | cut -d'-' -f1,2,3,4,5,6,7)
cat > /home/ubuntu/cht/upgrade-service/.env << EOF
CHT_COMPOSE_PROJECT_NAME=cht
COUCHDB_SECRET=${couchdb_secret}
DOCKER_CONFIG_PATH=/home/ubuntu/cht/upgrade-service
COUCHDB_DATA=/home/ubuntu/cht/couchdb
CHT_COMPOSE_PATH=/home/ubuntu/cht/compose
COUCHDB_USER=medic
COUCHDB_PASSWORD=${couchdb_password}
COUCHDB_UUID=${uuid}
EOF
```

### Launch Containers

```shell
cd /home/ubuntu/cht/upgrade-service
docker compose up --detach
```

### Verify Installation

Check that all 7 containers are running:

```shell
docker ps
```

Expected containers:
- `cht-nginx-1`
- `cht-api-1`
- `cht-sentinel-1`
- `cht-couchdb-1`
- `cht-healthcheck-1`
- `cht-haproxy-1`
- `upgrade-service-cht-upgrade-service-1`

---

## CHT Watchdog (Monitoring)

CHT Watchdog provides Grafana and Prometheus monitoring for CHT deployments. Supported on CHT 3.12+.

### Setup

```shell
cd ~
git clone https://github.com/medic/cht-watchdog.git
cd cht-watchdog
cp cht-instances.example.yml cht-instances.yml
cp grafana/grafana.example.ini grafana/grafana.ini
mkdir -p grafana/data && mkdir -p prometheus/data
cp .env.example .env
password=$(shuf -n7 /usr/share/dict/words --random-source=/dev/random | tr '\n' '-' | tr -d "'" | cut -d'-' -f1,2,3,4,5,6,7)
sed -i -e "s/password/$password/g" .env
```

### Configure Instances

Edit `cht-instances.yml`:

```yaml
- targets:
  - https://subsub.sub.example.com
  - https://cht.domain.com
  - https://website.org
```

### Start Watchdog

```shell
cd ~/cht-watchdog
docker compose up -d
```

Grafana available at http://localhost:3000

---

## Migration Guides

### Upgrading to CHT 4.x

**Requirements:**
- CHT Android version 1.0.0+
- Update CHT Conf to latest version
- Test forms with cht-conf-test-harness 3.x

**Enketo Changes:**
- `+` operator cannot concatenate strings (use `concat()`)
- Invalid XPath paths no longer equal empty string
- Unanswered number questions return `NaN` instead of `0`
- `horizontal`/`horizontal-compact` appearances deprecated (use `columns`)
- `today` returns midnight instead of current time

### Upgrading to CHT 5.x

**Pre-Upgrade Checklist:**
1. Ensure on CHT 4.5+ (upgrade first if on 4.0-4.4)
2. Verify 5x disk space available
3. Update CHT Conf to latest version
4. Recompile and upload app settings
5. Add `app_url` if using token login
6. Configure `languages` in app_settings
7. Verify `needs_signoff` uses boolean values
8. Check all users have Chrome 107+
9. For Kubernetes: Use Stage button only, then upgrade via Helm

**Breaking Changes:**
- Kubernetes: Upgrade button removed from admin app
- `app_url` required for token login
- Languages must be configured in app_settings
- Declarative configuration mandatory
- `needs_signoff` must be boolean, not string
- Chrome 107+ required (Angular 20 preparation)

**Post-Upgrade:**
- Temporary downtime for replication during Nouveau index building
- Small deployments: minutes
- Large deployments: up to 24 hours
- Monitor at `/_utils/#/activetasks`

**Removed Views:**
- `contacts_by_freetext`
- `contacts_by_type_freetext`
- `reports_by_freetext`

---

## Backup and Recovery

### Backup CouchDB Data

```shell
# Stop CHT containers (optional for consistent backup)
cd /home/ubuntu/cht/upgrade-service
docker compose down

# Backup CouchDB data directory
tar -czvf cht-backup-$(date +%Y%m%d).tar.gz /home/ubuntu/cht/couchdb

# Restart containers
docker compose up -d
```

### Restore from Backup

```shell
# Stop containers
docker compose down

# Restore data
tar -xzvf cht-backup-YYYYMMDD.tar.gz -C /

# Restart containers
docker compose up -d
```

---

## Common Operations

### Upgrade CHT Version

```shell
cd /home/ubuntu/cht/upgrade-service
docker compose pull
docker compose up -d
```

### View Logs

```shell
# All containers
docker compose logs -f

# Specific container
docker logs -f cht-api-1
```

### Check Active Users

```shell
curl -s https://CHT-URL/api/v2/monitoring?connected_user_interval=30 | jq '. | {connected_users}'
```

### Retrieve Admin Password

```shell
grep COUCHDB_PASSWORD /home/ubuntu/cht/upgrade-service/.env | cut -d'=' -f2
```
