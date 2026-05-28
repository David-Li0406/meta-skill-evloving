---
name: analyze-transaction
description: Parse decoded V2 transaction CBORs from Atlas API and create/update documentation YAML files
---

<introduction>
This skill parses decoded Cardano transaction CBORs from the Atlas API and creates/updates transaction YAML documentation in this repository. Focus exclusively on Andamio V2 transactions.

**Important**: We are currently migrating to a new instance of the Andamio V2 Preprod network. All addresses in the address-registry.json will be updated as we analyze each transaction. When processing a new transaction CBOR, the addresses in the CBOR are canonical and should replace any existing registry entries.

**Key Resources:**
- `public/yaml/transactions/v2/SESSION-NOTES.md` - Validator mappings, patterns, and context
- `public/yaml/transactions/v2/address-registry.json` - Discovered validators, policies, observers
- `public/yaml/transactions/v2/endpoint-registry.json` - API endpoint schemas
- `public/yaml/transactions/v2/cost-registry.json` - Transaction costs and fees
- `.claude/skills/analyze-transaction/hex-patterns.md` - Hex encoding patterns for token names
- Existing YAMLs in `public/yaml/transactions/v2/` as templates
</introduction>

<workflow>
## Phase 1: Analyze the Decoded CBOR

1. **Read the decoded transaction** supplied by the user (JSON format from Atlas API)
2. **Read SESSION-NOTES.md** to understand existing validator mappings and patterns
3. **Read address-registry.json** to identify known validators/policies by address
4. **Identify transaction components:**
   - Inputs: Which validators are being spent? What redeemers?
   - Outputs: Which validators receive UTxOs? What datum schemas?
   - Mints: Which policies? Token names? Quantities?
   - Withdrawals: Which observers? What redeemers?
   - Reference inputs: Which script references are used?
   - Fees: Tx fee + any protocol fees to treasuries

5. **Map addresses to validators** using address-registry.json
   - If an address is unknown, note it for registry update
   - Decode hex token names to identify patterns (u{alias}, g{alias}, etc.)

## Phase 2: Create/Update YAML Documentation

1. **Determine file path:** `public/yaml/transactions/v2/{system}/{role}/{tx-name}.yaml`
   - Use endpoint-registry.json to confirm the correct system/role/action

2. **Create or update the YAML file** with these sections:
   - `name`, `id`, `metadata` (role, system, description, api_endpoint)
   - `costs` (txFee, protocolFee, minUtxo, executionUnits)
   - `inputs` (validator, address, redeemer, datum reference)
   - `reference_inputs` (UTxO references for scripts)
   - `outputs` (validator, address, value, datum)
   - `mints` (policy, tokens, redeemer)
   - `withdraws` (observer, redeemer) if applicable
   - `registry` (local summary of validators/policies used)

3. **Update registries if new validators/policies discovered:**
   - Add to address-registry.json with `inferredFrom` tracking
   - Add to cost-registry.json if new fee patterns found
   - Update endpoint-registry.json if schema differs from documented

## Phase 3: Align with TypeScript Definitions (Required)

After completing the YAML documentation, verify and update the monorepo transaction definition:

1. **Locate the definition file:**
   - Path: `~/projects/01-projects/andamio-platform/andamio-platform-monorepo/packages/andamio-transactions/src/definitions/v2/{system}/{role}/{tx-name}.ts`
   - If the file doesn't exist, create it following existing patterns

2. **Verify alignment between YAML and TypeScript:**
   - `txParams` schema matches the API request body from YAML
   - `endpoint` matches `metadata.api_endpoint` from YAML
   - `estimatedCost` aligns with `costs` section from YAML
   - `docs.protocolDocs` points to the correct MDX documentation path

3. **Do NOT modify:**
   - `onSubmit` and `onConfirmation` side effects (separate concern)
   - `ui` section (unless specifically requested)

4. **Update index.ts exports** if creating a new definition file

## Phase 4: Handle Metadata (If Present)

If the transaction includes `auxiliary_data.metadata`, document it:

1. **CIP-25 NFT Metadata (label 721)**:
   - Extract the policy ID and asset name
   - Document the metadata fields (name, image, description, etc.)
   - Add a `metadata` section to the YAML:
   ```yaml
   metadata_721:
     policy: "{policy-name}"
     asset: "{token-name}"
     fields:
       name: "{NFT name}"
       description: "{description}"
       image: "{IPFS URI}"
       # ... other fields
   ```

2. **Other metadata labels**:
   - Document the label number and structure
   - Note any protocol-specific conventions

3. **Update hex-patterns.md** if new token naming patterns are discovered in metadata

## Phase 5: Ask Clarifying Questions

When you find ambiguities, ask about:
- Redeemer action names (e.g., "Is this SpendIndex or UpdateIndex?")
- Datum field semantics (e.g., "What does the third field represent?")
- Token name patterns (e.g., "Is this a hash or an alias?")
- Optional vs required inputs (e.g., "Is this input always present?")
</workflow>

<yaml-format>
## YAML Structure Example

```yaml
# V2 Transaction: {Transaction Name}
# Source: Decoded from CBOR transaction

name: {TransactionName}V2
id: {system}.{role}.{action}

metadata:
  role: "{role}"
  system: "{system}"
  description: "{What the transaction does}"
  api_endpoint: "/v2/tx/{path}"

costs:
  txFee: {lovelace}         # Network fee
  protocolFee: {lovelace}   # Fee to treasury (if any)
  minUtxo:
    {output_type}: {lovelace}
  executionUnits:
    spend: { mem: X, steps: Y }
    mint: { mem: X, steps: Y }

inputs:
  - id: {unique_id}
    type: script | wallet
    validator: {validator-name}  # from address-registry
    address: "{bech32_address}"
    redeemer:
      action: "{ActionName}"
      data: "{constructor: N, fields: [...]}"
    description: "{What this input provides}"

reference_inputs:
  - id: {unique_id}
    utxo: "{txHash}#{index}"
    description: "{What script this holds}"

outputs:
  - id: {unique_id}
    type: script | wallet
    validator: {validator-name}
    address: "{bech32_address}"
    value:
      - "{amount} lovelace"
      - "1 {policy-name}.{token-name}"
    datum:
      constructor: N
      fields:
        - field_name: "description or value"

mints:
  - id: {unique_id}
    policy: {policy-name}
    policyId: "{56-char hex}"
    redeemer:
      data: "{redeemer_value}"
    tokens:
      - quantity: 1
        name: "{token_name}"
        description: "{What this token represents}"

withdraws:
  - id: {unique_id}
    validator: {observer-name}
    stakeAddress: "{stake_address}"
    redeemer:
      data: "{redeemer_value}"
    amount: 0

registry:
  {validator-name}:
    address: "{address}"
  {policy-name}:
    policyId: "{policyId}"
```
</yaml-format>

<example>
## Full Example

See `.claude/skills/analyze-transaction/example-tx.md` for a complete worked example showing:
- API request to Atlas API
- Decoded CBOR response
- Resulting YAML file structure

**Input**: User provides decoded CBOR JSON from Atlas API

**Outputs (all required):**
1. YAML file at `public/yaml/transactions/v2/{system}/{role}/{tx-name}.yaml`
2. TypeScript definition at `~/projects/01-projects/andamio-platform/andamio-platform-monorepo/packages/andamio-transactions/src/definitions/v2/{system}/{role}/{tx-name}.ts`
3. Registry updates (if new validators/policies discovered)
</example>

<notes>
## Important Notes

1. **Complete all phases** - YAML documentation AND TypeScript alignment are both required
2. **Use registries as source of truth** - Always check address-registry.json before guessing validator names
3. **Track provenance** - When adding to registries, include `inferredFrom` to track which transactions revealed each validator
4. **Decode hex token names** - Refer to `hex-patterns.md` for encoding patterns; update it when new patterns are discovered
5. **Handle metadata** - If 721 or other metadata labels exist, document them in the YAML
6. **Ask questions when uncertain** - Better to clarify than guess incorrectly
7. **File path alignment**:
   - YAML: `public/yaml/transactions/v2/{system}/{role}/{tx-name}.yaml`
   - TS: `~/projects/01-projects/andamio-platform/andamio-platform-monorepo/packages/andamio-transactions/src/definitions/v2/{system}/{role}/{tx-name}.ts`
   - MDX: `content/docs/protocol/v2/transactions/{system}/{role}/{tx-name}.mdx`

## Existing Transactions (as templates)

| ID | YAML Path | Description |
|----|-----------|-------------|
| global.general.access-token.mint | global/general/access-token/mint.yaml | Entry point - mint access tokens |
| course.admin.create | course/admin/create.yaml | Create a new course |
| course.admin.teachers-update | course/admin/teachers-update.yaml | Update course teachers |
| course.teacher.modules-manage | course/teacher/modules-manage.yaml | Mint/update/burn modules |
| course.teacher.assignments-assess | course/teacher/assignments-assess.yaml | Assess student submissions |
| course.student.assignment.commit | course/student/assignment/commit.yaml | Student enrolls and commits to assignment |
| course.student.assignment-update | course/student/assignment-update.yaml | Student updates submission |
| course.student.credential-claim | course/student/credential-claim.yaml | Claim credential (burn) |

**Note**: File paths match API URL structure. For `/v2/tx/global/general/access-token/mint`, the YAML is at `global/general/access-token/mint.yaml`.
</notes>