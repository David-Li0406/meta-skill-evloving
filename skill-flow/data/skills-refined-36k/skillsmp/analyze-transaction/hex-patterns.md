# Hex Encoding Patterns for Andamio V2 Tokens

This file documents the hex encoding patterns used in Andamio V2 token names. Update this file as new patterns are discovered.

## Token Name Prefixes

| Prefix | Hex | Description | Example |
|--------|-----|-------------|---------|
| `u` | `75` | User access token | `75616c696365` = `ualice` |
| `g` | `67` | Global state token | `67616c696365` = `galice` |
| (space) | `20` | Index linked list marker | `20` = single space character |

## Common Token Names (Literal)

| Token Name | Hex | Used In |
|------------|-----|---------|
| `LocalStateNFT` | `4c6f63616c53746174654e4654` | course-create |
| `LocalStateToken` | `4c6f63616c5374617465546f6b656e` | course-create |

## Hash-Based Token Names

Some tokens use hashes as their names:

| Pattern | Length | Description |
|---------|--------|-------------|
| SLT Hash | 64 hex chars (32 bytes) | Module token name = Blake2b-256 hash of SLT strings |
| Course State | Variable | Student alias as token name |

## Decoding Hex to ASCII

```javascript
// Hex to ASCII
function hexToAscii(hex) {
  let str = '';
  for (let i = 0; i < hex.length; i += 2) {
    str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
  }
  return str;
}

// Example: hexToAscii("736f6d65616c696173") => "somealias"
```

## Policy ID Reference

| Policy Name | Policy ID | Token Patterns |
|-------------|-----------|----------------|
| index-policy | `4758613867a8a7aa500b5d57a0e877f01a8e63c1365469589b12063c` | u{alias}, g{alias}, 0x20 |
| local-state-token-policy | `1b4d9c2a523f5042f3b188cedfe07aadee1151e418bf578819dc4b5a` | LocalStateToken |
| local-state-nft-policy | (parameterized per course) | LocalStateNFT |
| course-governance-policy | `60e72e5ee056545fcb37f2d3f9b853daede356516ab5c80f886a652a` | {courseId} |
| module-policy | `0881d005d4301748df5aab08fbd302ad62f06a1b6b154664c96b9ba7` | {slt_hash} |
| course-state-policy | `91e18edd20667deaa1e40e0891b99f2b18ec4d6823d553abecc5ef18` | {student_alias} |

## Notes

- Token names in CBOR are hex-encoded
- When the hex decodes to readable ASCII, document the pattern
- When the hex is a hash (32+ bytes of seemingly random data), note it as a hash
- The `inferredFrom` field in address-registry.json tracks which transactions revealed each pattern
