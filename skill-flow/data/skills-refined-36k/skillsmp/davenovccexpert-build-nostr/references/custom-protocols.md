<overview>
Nostr can serve as infrastructure for custom application protocols beyond social media. This reference covers designing application-specific protocols on top of Nostr, including event schemas, coordination patterns, and interoperability considerations.
</overview>

<protocol_design>
## Protocol Design Principles

1. **Use standard kinds when possible** - Check NIPs first
2. **Version your schemas** - Include version in content
3. **Use tags for indexing** - Relays can only filter by tags
4. **Document everything** - Other developers need to understand
5. **Consider privacy** - Metadata is always visible
6. **Plan for evolution** - Protocols need to change
</protocol_design>

<schema_definition>
## Defining Event Schemas

```typescript
// Document your event kind
/**
 * Kind 30500: Game State
 *
 * Stores game state for a multiplayer game session.
 * Addressable event - latest per game ID.
 *
 * Tags:
 *   d: game-{gameId}
 *   t: game-state
 *   p: [player pubkeys...]
 *   game-type: {game type identifier}
 *
 * Content: JSON GameState object
 */

interface GameState {
  version: 1
  gameType: string
  turn: number
  players: Array<{
    pubkey: string
    score: number
  }>
  state: unknown  // Game-specific state
  updatedAt: number
}

const GAME_STATE_KIND = 30500

// Type guard for validation
function isValidGameState(data: unknown): data is GameState {
  if (typeof data !== 'object' || data === null) return false
  const obj = data as Record<string, unknown>
  return (
    obj.version === 1 &&
    typeof obj.gameType === 'string' &&
    typeof obj.turn === 'number' &&
    Array.isArray(obj.players)
  )
}
```
</schema_definition>

<coordination_patterns>
## Multi-Party Coordination

**Turn-based system:**
```typescript
interface TurnAction {
  version: 1
  gameId: string
  turn: number
  action: unknown
  previousStateHash: string  // For ordering
}

const TURN_ACTION_KIND = 25500  // Ephemeral

async function submitAction(gameId: string, turn: number, action: unknown) {
  const event = finalizeEvent({
    kind: TURN_ACTION_KIND,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['d', `game-${gameId}`],
      ['turn', String(turn)]
    ],
    content: JSON.stringify({
      version: 1,
      gameId,
      turn,
      action,
      previousStateHash: await getStateHash(gameId)
    })
  }, sk)

  await pool.publish(relays, event)
}

// Watch for actions
function watchActions(gameId: string, onAction: (action: TurnAction, from: string) => void) {
  return pool.subscribeMany(relays, [{
    kinds: [TURN_ACTION_KIND],
    '#d': [`game-${gameId}`]
  }], {
    onevent(event) {
      const action = JSON.parse(event.content) as TurnAction
      onAction(action, event.pubkey)
    }
  })
}
```

**Consensus pattern:**
```typescript
interface Vote {
  version: 1
  proposalId: string
  choice: string
  timestamp: number
}

const VOTE_KIND = 25501  // Ephemeral

// Collect votes and determine consensus
async function collectVotes(proposalId: string, timeoutMs: number): Promise<Map<string, string>> {
  const votes = new Map<string, string>()

  return new Promise(resolve => {
    const timeout = setTimeout(() => {
      sub.close()
      resolve(votes)
    }, timeoutMs)

    const sub = pool.subscribeMany(relays, [{
      kinds: [VOTE_KIND],
      '#proposal': [proposalId],
      since: Math.floor(Date.now() / 1000)
    }], {
      onevent(event) {
        const vote = JSON.parse(event.content) as Vote
        // Last vote wins per pubkey
        votes.set(event.pubkey, vote.choice)
      }
    })
  })
}
```
</coordination_patterns>

<discovery>
## Service Discovery

```typescript
// Announce a service
const SERVICE_KIND = 30600

interface ServiceAnnouncement {
  version: 1
  serviceType: string
  endpoints: string[]
  capabilities: string[]
  description: string
}

async function announceService(service: ServiceAnnouncement) {
  const event = finalizeEvent({
    kind: SERVICE_KIND,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['d', service.serviceType],
      ['t', 'service'],
      ['t', service.serviceType],
      ...service.capabilities.map(c => ['capability', c])
    ],
    content: JSON.stringify(service)
  }, sk)

  await pool.publish(relays, event)
}

// Discover services
async function discoverServices(serviceType: string): Promise<ServiceAnnouncement[]> {
  const events = await pool.querySync(relays, {
    kinds: [SERVICE_KIND],
    '#t': [serviceType]
  })

  return events.map(e => JSON.parse(e.content) as ServiceAnnouncement)
}
```
</discovery>

<rpc_pattern>
## RPC-like Patterns

```typescript
interface RPCRequest {
  version: 1
  method: string
  params: unknown
  id: string
}

interface RPCResponse {
  version: 1
  id: string
  result?: unknown
  error?: { code: number; message: string }
}

const RPC_REQUEST_KIND = 25600
const RPC_RESPONSE_KIND = 25601

class RPCClient {
  private pending = new Map<string, {
    resolve: (result: unknown) => void
    reject: (error: Error) => void
  }>()

  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array,
    private serverPk: string
  ) {
    this.listenForResponses()
  }

  private myPk = getPublicKey(this.sk)

  private listenForResponses() {
    this.pool.subscribeMany(this.relays, [{
      kinds: [RPC_RESPONSE_KIND],
      authors: [this.serverPk],
      '#p': [this.myPk]
    }], {
      onevent: (event) => {
        const response = JSON.parse(event.content) as RPCResponse
        const handler = this.pending.get(response.id)
        if (handler) {
          this.pending.delete(response.id)
          if (response.error) {
            handler.reject(new Error(response.error.message))
          } else {
            handler.resolve(response.result)
          }
        }
      }
    })
  }

  async call<T>(method: string, params: unknown): Promise<T> {
    const id = crypto.randomUUID()

    const request: RPCRequest = { version: 1, method, params, id }

    const event = finalizeEvent({
      kind: RPC_REQUEST_KIND,
      created_at: Math.floor(Date.now() / 1000),
      tags: [['p', this.serverPk]],
      content: JSON.stringify(request)
    }, this.sk)

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pending.delete(id)
        reject(new Error('RPC timeout'))
      }, 30000)

      this.pending.set(id, {
        resolve: (result) => {
          clearTimeout(timeout)
          resolve(result as T)
        },
        reject: (error) => {
          clearTimeout(timeout)
          reject(error)
        }
      })

      this.pool.publish(this.relays, event)
    })
  }
}

class RPCServer {
  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array,
    private handlers: Map<string, (params: unknown) => Promise<unknown>>
  ) {
    this.listen()
  }

  private myPk = getPublicKey(this.sk)

  private listen() {
    this.pool.subscribeMany(this.relays, [{
      kinds: [RPC_REQUEST_KIND],
      '#p': [this.myPk]
    }], {
      onevent: async (event) => {
        const request = JSON.parse(event.content) as RPCRequest
        await this.handleRequest(request, event.pubkey)
      }
    })
  }

  private async handleRequest(request: RPCRequest, clientPk: string) {
    const handler = this.handlers.get(request.method)

    let response: RPCResponse

    if (!handler) {
      response = {
        version: 1,
        id: request.id,
        error: { code: -32601, message: 'Method not found' }
      }
    } else {
      try {
        const result = await handler(request.params)
        response = { version: 1, id: request.id, result }
      } catch (err) {
        response = {
          version: 1,
          id: request.id,
          error: { code: -32000, message: String(err) }
        }
      }
    }

    const event = finalizeEvent({
      kind: RPC_RESPONSE_KIND,
      created_at: Math.floor(Date.now() / 1000),
      tags: [['p', clientPk]],
      content: JSON.stringify(response)
    }, this.sk)

    await this.pool.publish(this.relays, event)
  }
}
```
</rpc_pattern>

<interoperability>
## Interoperability Guidelines

1. **Prefix custom tags** - Use `x-myapp-` to avoid collisions
2. **Use standard tags when applicable** - `e`, `p`, `t`, `d`
3. **Document publicly** - Share your NIP-like specification
4. **Version everything** - In content and optionally in tags
5. **Fail gracefully** - Handle unknown fields/versions
6. **Consider encryption** - For private protocols
</interoperability>

<anti_patterns>
## Anti-Patterns

**Storing everything in content:**
```typescript
// BAD - can't query
{ content: JSON.stringify({ type: 'game', gameId: 'abc' }) }

// GOOD - queryable
{
  tags: [['d', 'abc'], ['t', 'game']],
  content: JSON.stringify({ ... })
}
```

**Not versioning:**
```typescript
// BAD
{ content: JSON.stringify({ data: 'value' }) }

// GOOD
{ content: JSON.stringify({ version: 1, data: 'value' }) }
```

**Using reserved kinds:**
```typescript
// BAD - conflicts with standard
const MY_KIND = 1  // Text note!

// GOOD - use unassigned range
const MY_KIND = 30500
```
</anti_patterns>
