# BSocial Schema Reference

Quick reference for BitcoinSchema.org social protocol schemas.

## Protocol Stack

```
[B Protocol] | [MAP Protocol] | [AIP Protocol]
   content       metadata         signature
```

**Protocol Prefixes:**
- B: `19HxigV4QyBv3tHpQVcUEQyq1pzZVdoAut`
- MAP: `1PuQa7K62MiKCtssSLKy1kh56WWU7MtUR5`
- AIP: `15PciHG22SNLQJXMoSUaWVi7WSqc7hCfva`

## Action Types

| Type | Description | Key Fields |
|------|-------------|------------|
| `post` | Create content | content, mediaType, encoding |
| `like` | Like a post | tx (txid of liked post) |
| `unlike` | Remove like | tx (txid of liked post) |
| `follow` | Follow user | bapId (identity key) |
| `unfollow` | Unfollow user | bapId (identity key) |
| `message` | Send message | content, context, contextValue |
| `repost` | Share content | tx (txid of original) |
| `friend` | Friend request | bapId, publicKey |

## Context Types

| Context | Use Case |
|---------|----------|
| `tx` | Reply to transaction |
| `channel` | Post/message to channel |
| `bapID` | Target specific identity |
| `url` | Associate with URL |
| `topic` | Categorize by topic |
| `geohash` | Location tagging |

## Post Schema

```
B <content> <mediaType> <encoding> |
MAP SET app bsocial type post [context <type> <type> <value>] |
AIP BITCOIN_ECDSA <address> <signature>
```

## Like Schema

```
MAP SET app bsocial type like tx <txid> |
AIP BITCOIN_ECDSA <address> <signature>
```

## Follow Schema

```
MAP SET app bsocial type follow bapId <bapId> |
AIP BITCOIN_ECDSA <address> <signature>
```

## Message Schema

```
B <content> <mediaType> <encoding> |
MAP SET app bsocial type message context <type> contextValue <value> |
AIP BITCOIN_ECDSA <address> <signature>
```

## Friend Schema

```
MAP SET app bsocial type friend bapID <bapId> publicKey <derivedPubKey> |
AIP BITCOIN_ECDSA <address> <signature>
```

## BMAP Query API

Base URL: `https://b.map.sv/q/{base64-query}`

Query format (v3):
```json
{
  "v": 3,
  "q": {
    "find": {
      "MAP.app": "bsocial",
      "MAP.type": "post",
      "AIP.address": "1xxx..."
    },
    "sort": { "blk.t": -1 },
    "limit": 20
  }
}
```

## Links

- [BitcoinSchema.org](https://bitcoinschema.org)
- [BMAP API](https://b.map.sv)
- [@bopen-io/templates](https://github.com/b-open-io/ts-templates)
