---
name: Zimbra Mail Flow
description: This skill should be used when the user asks about "Postfix configuration", "mail queue", "content filter", "mail routing", "amavisd", "milter", "SMTP relay", "mail delivery", "MTA settings", "message flow", or mentions mail transport issues with Zimbra. Provides guidance for mail flow configuration and troubleshooting.
version: 1.0.0
---

# Zimbra Mail Flow

Guide for configuring and troubleshooting mail flow in Zimbra, including Postfix integration, content filtering, and queue management.

## Architecture Overview

Zimbra uses Postfix as its MTA (Mail Transfer Agent):

```
Internet → Proxy (nginx) → Postfix → Content Filter → Postfix → Mailbox
                              ↓
                          amavisd-new
                              ↓
                        SpamAssassin/ClamAV
```

### Components

- **Postfix** - SMTP server for sending and receiving mail
- **amavisd-new** - Content filter interface
- **SpamAssassin** - Spam detection
- **ClamAV** - Antivirus scanning
- **policyd** - Policy daemon for rate limiting

## Postfix Configuration

### Key Configuration Files

| File | Purpose |
|------|---------|
| `/opt/zimbra/common/conf/main.cf` | Main Postfix config |
| `/opt/zimbra/common/conf/master.cf` | Service definitions |
| `/opt/zimbra/conf/zmconfigd/smtpd.cf` | SMTP daemon config |

### View/Modify Settings

```bash
# View current setting
postconf content_filter

# View all settings
postconf -n

# Modify setting (as zimbra user)
zmprov ms $(hostname) zimbraMtaContentFilter "smtp-amavis:[127.0.0.1]:10024"

# Direct postconf (may be overwritten by Zimbra)
postconf -e "content_filter = smtp-amavis:[127.0.0.1]:10024"

# Reload after changes
postfix reload
```

### Common Settings via zmprov

```bash
# Content filter
zmprov ms mail.domain.com zimbraMtaContentFilter "smtp-amavis:[127.0.0.1]:10024"

# Relay host
zmprov ms mail.domain.com zimbraMtaRelayHost "smtp.relay.com:25"

# Message size limit (bytes)
zmprov ms mail.domain.com zimbraMtaMaxMessageSize 52428800

# SMTP authentication
zmprov ms mail.domain.com zimbraMtaSaslAuthEnable TRUE
```

## Content Filtering

### Default Flow

1. Mail arrives on port 25
2. Postfix sends to amavisd on port 10024
3. amavisd processes (spam/virus check)
4. Clean mail returns to Postfix on port 10025
5. Postfix delivers to mailbox

### Custom Content Filter

To add a custom content filter (e.g., policy server):

```bash
# Check port availability FIRST
netstat -tlnp | grep 2525

# Add service to master.cf
postconf -Me "policy-filter/unix = policy-filter unix - n n - 10 smtp -o smtp_send_xforward_command=yes"

# Set content filter
zmprov ms $(hostname) zimbraMtaContentFilter "smtp:[127.0.0.1]:2525"

# Reload MTA
zmcontrol restart mta
```

### Bypass Content Filter

For specific senders/recipients:

```bash
# Create transport map
echo "admin@domain.com :" >> /opt/zimbra/conf/transport

# Rebuild and reload
postmap /opt/zimbra/conf/transport
postfix reload
```

## Queue Management

### View Queue

```bash
# Queue summary
mailq

# Detailed queue listing
postqueue -p

# Count messages
mailq | tail -n 1
```

### Manage Queue

```bash
# Flush queue (attempt redelivery)
postqueue -f

# Delete specific message
postsuper -d <queue-id>

# Delete all queued messages
postsuper -d ALL

# Hold message
postsuper -h <queue-id>

# Release held message
postsuper -H <queue-id>

# Requeue message
postsuper -r <queue-id>
```

### View Message Content

```bash
# Find message in queue
find /opt/zimbra/data/postfix/spool -name "<queue-id>"

# View message headers
postcat -q <queue-id> | head -50

# View full message
postcat -q <queue-id>
```

## Troubleshooting

### Check MTA Status

```bash
# Service status
zmmtactl status

# Postfix status
postfix status

# Check listening ports
netstat -tlnp | grep -E "(25|465|587|10024|10025)"
```

### Log Analysis

```bash
# Main mail log
tail -f /var/log/zimbra.log

# Postfix log
tail -f /opt/zimbra/log/zimbra.log | grep postfix

# Track message by ID
grep <message-id> /var/log/zimbra.log
```

### Common Issues

#### Mail Stuck in Queue

```bash
# Check queue reason
postqueue -p | grep -A 2 <queue-id>

# Check DNS
host -t mx recipient-domain.com

# Check relay connectivity
telnet relay.host.com 25
```

#### Content Filter Not Working

```bash
# Verify amavisd running
zmamavisdctl status

# Check content_filter setting
postconf content_filter

# Verify ports
netstat -tlnp | grep 10024
netstat -tlnp | grep 10025
```

#### SMTP Authentication Failing

```bash
# Check SASL config
postconf smtpd_sasl_auth_enable

# Test auth
openssl s_client -connect mail.domain.com:465 -quiet
AUTH LOGIN
```

## Relay Configuration

### Outbound Relay

```bash
# Set relay host
zmprov ms $(hostname) zimbraMtaRelayHost "smtp.relay.com:25"

# With authentication
zmprov ms $(hostname) zimbraMtaRelayHost "[smtp.relay.com]:587"
zmprov ms $(hostname) zimbraMtaSaslAuthEnable TRUE

# Configure credentials in sasl_passwd
echo "[smtp.relay.com]:587 username:password" >> /opt/zimbra/conf/sasl_passwd
postmap /opt/zimbra/conf/sasl_passwd
```

### Inbound Relay (Accept from specific hosts)

```bash
# Add to mynetworks
zmprov ms $(hostname) +zimbraMtaMyNetworks "192.168.1.0/24"

# Reload
postfix reload
```

## Rate Limiting

### Using cbpolicyd

```bash
# Check status
zmcbpolicydctl status

# View policies
sqlite3 /opt/zimbra/data/cbpolicyd/db/cbpolicyd.sqlitedb \
  "SELECT * FROM policies;"

# Common rate limit (via admin console or direct SQL)
# Limit 100 messages per hour per sender
```

## Additional Resources

### Reference Files

- **`references/postfix-settings.md`** - Complete Postfix parameter reference
- **`references/amavisd-config.md`** - amavisd configuration options

### Example Files

- **`examples/custom-content-filter.sh`** - Setup custom filter
- **`examples/transport-map.sh`** - Configure transport routing
