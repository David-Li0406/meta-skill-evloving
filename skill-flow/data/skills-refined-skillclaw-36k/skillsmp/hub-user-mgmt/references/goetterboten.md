# Götterboten Pool

Pre-configured user endpoints named after mythological messengers.

## Default Pool

| Name | Mythology | Description | Status |
|------|-----------|-------------|--------|
| hermes | Greek | Messenger of the gods | Admin (default) |
| iris | Greek | Rainbow messenger | Available |
| mercury | Roman | Messenger god | Available |
| thoth | Egyptian | God of writing/messages | Available |
| gabriel | Abrahamic | Archangel messenger | Available |
| angelos | Greek | Generic messenger | Available |
| arke | Greek | Titan messenger | Available |
| jibril | Islamic | Angel Gabriel | Available |

## Expansion Candidates

More messengers from world mythology:

**Norse:**
- `hugin` - Odin's thought raven
- `munin` - Odin's memory raven

**Hindu:**
- `narada` - Divine sage messenger

**Japanese:**
- `tengu` - Mountain messenger spirits

**Celtic:**
- `pwyll` - Otherworld messenger

## Reserved Names

Cannot be used as user endpoints:
- `admin` - Admin endpoint
- `system` - System endpoints
- `test` - Test endpoints
- `health` - Health check endpoint

## Naming Rules

- Lowercase letters only: `[a-z]+`
- Must be added to GOETTERBOTEN_POOL in config
- One user per endpoint name

## Customization

Feel free to replace this naming scheme with your own:
- Team member names
- Project codenames
- Department names
- Sequential IDs (user1, user2, ...)

Update `services/hub/src/config/users.cjs` accordingly.
