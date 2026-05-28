#!/usr/bin/env bash
set -euo pipefail

# Config
STAGING="${STAGING:-/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1}"
MAX_GB="${MAX_GB:-99}"
LOG="${LOG:-/home/yousuf/PROJECTS/PeopleNet/Logs/staging_watchdog.log}"
POLL="${POLL:-10}"

get_size_gb() {
	du -sBG "$STAGING" 2>/dev/null | awk '{print $1}' | tr -dc '0-9'
}

while true; do
	SZ="$(get_size_gb)"
	SZ="${SZ:-0}"
	if [ "$SZ" -ge "$MAX_GB" ]; then
		if pgrep -f '/tmp/copy_agent.sh' >/dev/null 2>&1; then
			pkill -STOP -f '/tmp/copy_agent.sh' || true
		fi
		echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ') paused size=${SZ}G ge=${MAX_GB}G" >> "$LOG"
	else
		if pgrep -f '/tmp/copy_agent.sh' >/dev/null 2>&1; then
			pkill -CONT -f '/tmp/copy_agent.sh' || true
		fi
		echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ') resumed size=${SZ}G lt=${MAX_GB}G" >> "$LOG"
	fi
	sleep "$POLL"
done

#!/usr/bin/env bash
set -euo pipefail
STAGING=/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1
MAX_GB=99
LOG=/home/yousuf/PROJECTS/PeopleNet/Logs/staging_watchdog.log
POLL=10
get_size_gb() { du -sBG  2>/dev/null | awk '{print bash -lc "set -euo pipefail; mkdir -p /home/yousuf/PROJECTS/PeopleNet/Scripts /home/yousuf/PROJECTS/PeopleNet/Logs; cat > /home/yousuf/PROJECTS/PeopleNet/Scripts/staging_watchdog.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
STAGING="${STAGING:-/home/yousuf/PROJECTS/PeopleNet/Staging/Park_R_Batch1}"
MAX_GB="${MAX_GB:-99}"
LOG="${LOG:-/home/yousuf/PROJECTS/PeopleNet/Logs/staging_watchdog.log}"
POLL="${POLL:-10}"
get_size_gb() { du -sBG "$STAGING" 2>/dev/null | awk '{print $1}' | tr -dc '0-9'; }
while true; do
  SZ="$(get_size_gb)"; SZ="${SZ:-0}"
  if [ "$SZ" -ge "$MAX_GB" ]; then
    if pgrep -f '/tmp/copy_agent.sh' >/dev/null 2>&1; then pkill -STOP -f '/tmp/copy_agent.sh' || true; fi
    echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ') paused size=${SZ}G ge=${MAX_GB}G" >> "$LOG"
  else
    if pgrep -f '/tmp/copy_agent.sh' >/dev/null 2>&1; then pkill -CONT -f '/tmp/copy_agent.sh' || true; fi
    echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ') resumed size=${SZ}G lt=${MAX_GB}G" >> "$LOG"
  fi
  sleep "$POLL"
done
