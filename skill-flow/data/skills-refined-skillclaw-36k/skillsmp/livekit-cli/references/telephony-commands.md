# Telephony commands

The LiveKit CLI provides commands for managing phone numbers and SIP configuration. These commands help you set up inbound and outbound calling for your voice AI agents.

## Phone number commands

> **Note:** LiveKit Phone Numbers currently only supports inbound calling. Support for outbound calls is coming soon.

All phone number commands are prefixed with `lk number`.

### Search available numbers

Search for phone numbers available for purchase:

```bash
lk number search --country-code US --area-code 415
```

**Options**:
- `--country-code STRING`: Filter by country code (e.g., "US", "CA"). Required.
- `--area-code STRING`: Filter by area code (e.g., "415")
- `--limit INT`: Maximum number of results (default: 50)
- `--json, -j`: Output as JSON

**Example**:
```bash
lk number search --country-code US --area-code 415 --limit 10
```

### Purchase numbers

Buy phone numbers from inventory:

```bash
lk number purchase --numbers +14155550100
```

**Options**:
- `--numbers STRING`: Phone numbers to purchase (e.g., "+16505550010"). Required.
- `--sip-dispatch-rule-id STRING`: SIP dispatch rule ID to apply to purchased numbers

### List numbers

List phone numbers for your project:

```bash
lk number list
```

**Options**:
- `--limit INT`: Maximum number of results (default: 50)
- `--status STRING`: Filter by status: `active`, `pending`, `released` (can use multiple times)
- `--sip-dispatch-rule-id STRING`: Filter by SIP dispatch rule ID
- `--json, -j`: Output as JSON

**Examples**:
```bash
# List all active numbers
lk number list

# List active and released numbers
lk number list --status active --status released
```

### Get number details

Get details for a specific phone number:

```bash
lk number get --id <PHONE_NUMBER_ID>
# or
lk number get --number +16505550010
```

**Options**:
- `--id STRING`: Phone number ID for direct lookup
- `--number STRING`: Phone number string for lookup

### Update number

Update a phone number's configuration:

```bash
lk number update --id <PHONE_NUMBER_ID> --sip-dispatch-rule-id <DISPATCH_RULE_ID>
```

**Options**:
- `--id STRING`: Phone number ID
- `--number STRING`: Phone number string (alternative to --id)
- `--sip-dispatch-rule-id STRING`: Dispatch rule ID to assign

**Example**:
```bash
lk number update --number +16505550010 --sip-dispatch-rule-id <RULE_ID>
```

### Release numbers

Release phone numbers:

```bash
lk number release --ids <PHONE_NUMBER_ID>
# or
lk number release --numbers +16505550010
```

**Options**:
- `--ids STRING`: Phone number IDs to release
- `--numbers STRING`: Phone number strings to release

## SIP inbound trunk commands

Inbound trunks control how incoming calls are authenticated and processed. Commands are prefixed with `lk sip inbound`.

### Create inbound trunk

Create a trunk from a JSON file:

```bash
lk sip inbound create inbound-trunk.json
```

**Example JSON** (`inbound-trunk.json`):
```json
{
  "trunk": {
    "name": "My trunk",
    "numbers": ["+15105550100"],
    "krispEnabled": true
  }
}
```

**Trunk with allowed callers**:
```json
{
  "trunk": {
    "name": "My trunk",
    "numbers": ["+15105550100"],
    "allowedNumbers": ["+13105550100", "+17145550100"]
  }
}
```

### List inbound trunks

List all inbound trunks:

```bash
lk sip inbound list
```

### Update inbound trunk

Update an existing trunk:

```bash
lk sip inbound update --id <trunk-id> inbound-trunk.json
```

## SIP outbound trunk commands

Outbound trunks are used for making calls. Commands are prefixed with `lk sip outbound`.

### List outbound trunks

List all outbound trunks:

```bash
lk sip outbound list
```

## SIP dispatch rule commands

Dispatch rules control how callers are added to rooms. Commands are prefixed with `lk sip dispatch`.

### Create dispatch rule

Create a dispatch rule from a JSON file:

```bash
lk sip dispatch create dispatch-rule.json
```

**Individual dispatch rule** (creates a new room per caller):
```json
{
  "dispatch_rule": {
    "rule": {
      "dispatchRuleIndividual": {
        "roomPrefix": "call-"
      }
    },
    "name": "My dispatch rule",
    "roomConfig": {
      "agents": [{
        "agentName": "inbound-agent",
        "metadata": "job dispatch metadata"
      }]
    }
  }
}
```

**Direct dispatch rule** (all callers join the same room):
```json
{
  "dispatch_rule": {
    "rule": {
      "dispatchRuleDirect": {
        "roomName": "open-room"
      }
    },
    "name": "My dispatch rule"
  }
}
```

**Pin-protected room**:
```json
{
  "dispatch_rule": {
    "rule": {
      "dispatchRuleDirect": {
        "roomName": "safe-room",
        "pin": "12345"
      }
    },
    "name": "My dispatch rule"
  }
}
```

**Callee dispatch rule** (room based on called number):
```json
{
  "dispatch_rule": {
    "rule": {
      "dispatchRuleCallee": {
        "roomPrefix": "number-",
        "randomize": false
      }
    },
    "name": "My dispatch rule"
  }
}
```

### List dispatch rules

List all dispatch rules:

```bash
lk sip dispatch list
```

### Update dispatch rule

Update an existing dispatch rule:

```bash
lk sip dispatch update --id <dispatch-rule-id> --trunks "[]" dispatch-rule.json
```

**Options**:
- `--id STRING`: Dispatch rule ID to update
- `--trunks STRING`: Comma-separated trunk IDs (use `"[]"` for all trunks)

## Setting up inbound calling

Complete setup for accepting inbound calls:

1. **Purchase a phone number**:
   ```bash
   lk number search --country-code US --area-code 415
   lk number purchase --numbers +14155550100
   ```

2. **Create a dispatch rule** (save as `dispatch-rule.json`):
   ```json
   {
     "dispatch_rule": {
       "rule": {
         "dispatchRuleIndividual": {
           "roomPrefix": "call-"
         }
       },
       "name": "Inbound calls",
       "roomConfig": {
         "agents": [{
           "agentName": "my-voice-agent"
         }]
       }
     }
   }
   ```
   ```bash
   lk sip dispatch create dispatch-rule.json
   ```

3. **Assign the dispatch rule to your number**:
   ```bash
   lk number list  # Get the phone number ID
   lk number update --id <PHONE_NUMBER_ID> --sip-dispatch-rule-id <DISPATCH_RULE_ID>
   ```

4. **Deploy your agent** with the name specified in the dispatch rule:
   ```bash
   lk agent create
   ```

## Dispatch rule types

| Type | Behavior | Use case |
|------|----------|----------|
| `dispatchRuleIndividual` | Creates a new room per caller | Most voice AI agents |
| `dispatchRuleDirect` | All callers join the same room | Conference calls, support queues |
| `dispatchRuleCallee` | Room based on called number | Multi-tenant setups |

## SIP trunk providers

If you're using a third-party SIP provider instead of LiveKit Phone Numbers, you'll need to create inbound/outbound trunks. Supported providers include:
- Twilio
- Telnyx
- Plivo
- Wavix

See the LiveKit telephony documentation for provider-specific setup guides.
