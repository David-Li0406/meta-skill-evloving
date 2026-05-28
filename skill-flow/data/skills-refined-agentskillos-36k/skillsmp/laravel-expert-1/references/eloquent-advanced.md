# Eloquent Advanced Reference

## Query Scopes Dinâmicos

```php
// Model
public function scopeFilter($query, array $filters)
{
    return $query
        ->when($filters['status'] ?? null, fn($q, $status) => $q->where('status', $status))
        ->when($filters['date_from'] ?? null, fn($q, $date) => $q->where('created_at', '>=', $date))
        ->when($filters['date_to'] ?? null, fn($q, $date) => $q->where('created_at', '<=', $date))
        ->when($filters['search'] ?? null, fn($q, $search) => 
            $q->where(fn($q) => 
                $q->where('name', 'like', "%{$search}%")
                  ->orWhere('email', 'like', "%{$search}%")
            )
        );
}

// Uso
Contract::filter($request->only(['status', 'date_from', 'date_to', 'search']))->paginate();
```

## Eager Loading Condicional

```php
// Com contagem
$users = User::withCount('posts')->get();
// $user->posts_count

// Com soma
$clients = Client::withSum('contracts', 'value')->get();
// $client->contracts_sum_value

// Condicional
$contracts = Contract::with(['payments' => fn($q) => $q->where('status', 'pending')])
    ->get();

// Eager load aninhado
$contracts = Contract::with([
    'client.address',
    'payments.transactions'
])->get();
```

## Subqueries

```php
// Última data de pagamento como subquery
$contracts = Contract::addSelect([
    'last_payment_date' => Payment::select('paid_at')
        ->whereColumn('contract_id', 'contracts.id')
        ->latest('paid_at')
        ->limit(1)
])->get();

// Ordenar por subquery
$clients = Client::orderByDesc(
    Contract::select('created_at')
        ->whereColumn('client_id', 'clients.id')
        ->latest()
        ->limit(1)
)->get();
```

## Query Builder Raw

```php
// Select raw
$stats = Contract::selectRaw('
    YEAR(event_date) as year,
    MONTH(event_date) as month,
    COUNT(*) as total,
    SUM(value) as total_value
')
->groupByRaw('YEAR(event_date), MONTH(event_date)')
->get();

// Where raw para performance
$contracts = Contract::whereRaw('DATEDIFF(event_date, NOW()) <= 7')->get();
```

## Chunking para Grandes Volumes

```php
// Chunk básico
Contract::chunk(1000, function ($contracts) {
    foreach ($contracts as $contract) {
        // processar
    }
});

// Chunk com ID (melhor para updates)
Contract::chunkById(1000, function ($contracts) {
    $contracts->each->markAsProcessed();
});

// Lazy collection (memory efficient)
Contract::lazy()->each(function ($contract) {
    // processar um por vez
});

// Cursor (mais eficiente em memória)
foreach (Contract::cursor() as $contract) {
    // processar
}
```

## Upsert e Batch Operations

```php
// Upsert (insert ou update)
Contract::upsert(
    [
        ['external_id' => 'ABC', 'value' => 1000, 'status' => 'active'],
        ['external_id' => 'DEF', 'value' => 2000, 'status' => 'pending'],
    ],
    ['external_id'],           // Unique keys
    ['value', 'status']        // Columns to update
);

// Insert ignorando duplicatas
Contract::insertOrIgnore([...]);

// Update em massa
Contract::where('status', 'pending')
    ->where('event_date', '<', now())
    ->update(['status' => 'expired']);
```

## Relacionamentos Polimórficos

```php
// Model Comment
class Comment extends Model
{
    public function commentable(): MorphTo
    {
        return $this->morphTo();
    }
}

// Model Contract
class Contract extends Model
{
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

// Uso
$contract->comments()->create(['body' => 'Observação...']);
```

## Query Caching

```php
// Cache manual
$contracts = Cache::remember('active-contracts', 3600, function () {
    return Contract::active()->with('client')->get();
});

// Invalidação
Cache::forget('active-contracts');

// Cache tags (Redis/Memcached)
Cache::tags(['contracts'])->remember('active', 3600, fn() => Contract::active()->get());
Cache::tags(['contracts'])->flush();
```
