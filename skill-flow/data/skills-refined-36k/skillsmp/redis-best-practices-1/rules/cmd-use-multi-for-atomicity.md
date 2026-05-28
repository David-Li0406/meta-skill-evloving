---
title: Use MULTI/EXEC for Atomic Operations
impact: HIGH
impactDescription: prevents race conditions, ensures data consistency
tags: commands, transactions, atomicity, consistency
---

## Use MULTI/EXEC for Atomic Operations

Use Redis transactions (MULTI/EXEC) when multiple commands must execute atomically. Without transactions, concurrent clients can interleave operations, causing race conditions and data corruption.

**What MULTI/EXEC Provides:**
- All commands execute sequentially without interruption
- Other clients' commands never interleave
- Either all commands execute or none (if EXEC fails)
- Note: No rollback on command errors within transaction

**Incorrect (race condition prone):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Check-then-act without atomicity
def transfer_funds_bad(from_acct, to_acct, amount):
    # Race condition! Another client can modify between these calls
    balance = int(r.get(f"balance:{from_acct}") or 0)
    if balance >= amount:
        r.decrby(f"balance:{from_acct}", amount)  # Not atomic!
        r.incrby(f"balance:{to_acct}", amount)
        return True
    return False

# Anti-pattern 2: Increment after check
def increment_if_below_max_bad(key, max_value):
    current = int(r.get(key) or 0)
    if current < max_value:
        r.incr(key)  # Race: might exceed max!
        return True
    return False

# Anti-pattern 3: Read-modify-write without lock
def update_json_bad(key, updates):
    data = json.loads(r.get(key) or '{}')
    data.update(updates)  # Another client might update between read and write
    r.set(key, json.dumps(data))
```

**Correct (using transactions):**

```python
import redis
r = redis.Redis()

# Correct 1: Pipeline with transaction=True (MULTI/EXEC)
def transfer_funds(from_acct, to_acct, amount):
    """Atomic transfer using transaction"""
    pipe = r.pipeline(transaction=True)  # Wraps in MULTI/EXEC
    pipe.decrby(f"balance:{from_acct}", amount)
    pipe.incrby(f"balance:{to_acct}", amount)
    results = pipe.execute()
    return results

# Correct 2: WATCH for optimistic locking
def transfer_funds_with_check(from_acct, to_acct, amount):
    """Transfer with balance check using WATCH"""
    from_key = f"balance:{from_acct}"
    to_key = f"balance:{to_acct}"

    with r.pipeline() as pipe:
        while True:
            try:
                # Watch the source account for changes
                pipe.watch(from_key)

                # Check balance (outside transaction)
                balance = int(pipe.get(from_key) or 0)
                if balance < amount:
                    pipe.unwatch()
                    return False  # Insufficient funds

                # Start transaction
                pipe.multi()
                pipe.decrby(from_key, amount)
                pipe.incrby(to_key, amount)
                pipe.execute()  # Executes atomically
                return True

            except redis.WatchError:
                # Another client modified the key, retry
                continue

# Correct 3: Atomic increment with limit
def increment_with_limit(key, max_value, expire=None):
    """Atomic increment that respects maximum value"""
    # Use Lua script for true atomicity (see cmd-use-lua-scripts)
    lua_script = """
    local current = tonumber(redis.call('GET', KEYS[1]) or '0')
    if current < tonumber(ARGV[1]) then
        redis.call('INCR', KEYS[1])
        if ARGV[2] then
            redis.call('EXPIRE', KEYS[1], ARGV[2])
        end
        return current + 1
    end
    return -1
    """
    result = r.eval(lua_script, 1, key, max_value, expire or '')
    return result if result != -1 else None

# Correct 4: Bulk operations atomically
def create_user_atomic(user_id, user_data):
    """Create user with all related data atomically"""
    pipe = r.pipeline(transaction=True)

    # All these execute as one atomic operation
    pipe.hset(f"user:{user_id}", mapping=user_data)
    pipe.set(f"user:email:{user_data['email']}", user_id)
    pipe.sadd("users:all", user_id)
    pipe.zadd("users:by_created", {user_id: time.time()})

    results = pipe.execute()
    return all(results)
```

```javascript
// Node.js - Transactions with ioredis
const Redis = require('ioredis');
const redis = new Redis();

// Basic transaction
async function transferFunds(fromAcct, toAcct, amount) {
    const results = await redis.multi()
        .decrby(`balance:${fromAcct}`, amount)
        .incrby(`balance:${toAcct}`, amount)
        .exec();

    return results;
}

// WATCH for optimistic locking
async function transferWithCheck(fromAcct, toAcct, amount) {
    const fromKey = `balance:${fromAcct}`;

    await redis.watch(fromKey);

    const balance = parseInt(await redis.get(fromKey)) || 0;
    if (balance < amount) {
        await redis.unwatch();
        return false;
    }

    try {
        const results = await redis.multi()
            .decrby(fromKey, amount)
            .incrby(`balance:${toAcct}`, amount)
            .exec();

        return results !== null;  // null if WATCH failed
    } catch (e) {
        return false;
    }
}
```

```go
// Go - Transactions with go-redis
func TransferFunds(ctx context.Context, from, to string, amount int64) error {
    _, err := rdb.TxPipelined(ctx, func(pipe redis.Pipeliner) error {
        pipe.DecrBy(ctx, fmt.Sprintf("balance:%s", from), amount)
        pipe.IncrBy(ctx, fmt.Sprintf("balance:%s", to), amount)
        return nil
    })
    return err
}

// WATCH for optimistic locking
func TransferWithCheck(ctx context.Context, from, to string, amount int64) error {
    fromKey := fmt.Sprintf("balance:%s", from)
    toKey := fmt.Sprintf("balance:%s", to)

    return rdb.Watch(ctx, func(tx *redis.Tx) error {
        balance, err := tx.Get(ctx, fromKey).Int64()
        if err != nil && err != redis.Nil {
            return err
        }
        if balance < amount {
            return errors.New("insufficient funds")
        }

        _, err = tx.TxPipelined(ctx, func(pipe redis.Pipeliner) error {
            pipe.DecrBy(ctx, fromKey, amount)
            pipe.IncrBy(ctx, toKey, amount)
            return nil
        })
        return err
    }, fromKey)
}
```

Reference: [Redis Transactions](https://redis.io/docs/manual/transactions/)
