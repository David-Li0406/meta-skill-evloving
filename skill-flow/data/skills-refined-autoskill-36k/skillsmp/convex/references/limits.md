# Limits You Must Design Around

You **must** avoid designs that hit these limits:

## Function Args + Return Values
- Max **8 MiB**

## Arrays
- Max **8192 elements**

## Objects
- Max **1024 entries**
- Keys must be ASCII, non-empty, not starting with `$` or `_`
- Nesting depth ≤ 16

## Documents
- Size < **1 MiB**

## Queries/Mutations
- Can **read** up to 8 MiB / 16384 docs
- Can **write** up to 8 MiB / 8192 docs
- Must finish within **1 second**

## Actions / HTTP Actions
- Up to **10 minutes** runtime

## HTTP Actions
- Response streaming max **20 MiB**

## Design Pattern

If you're tempted to store **huge time-series** or **entire datasets** per document, instead upload a blob to file storage and handle parsing client-side.
