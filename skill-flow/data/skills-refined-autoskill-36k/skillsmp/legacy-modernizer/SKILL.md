---
name: legacy-modernizer
description: Modernização de código PHP legado para padrões atuais (PHP 7.4-8.3). Usar para converter código procedural para OOP, atualizar sintaxe deprecated, implementar type hints, substituir arrays por objetos/collections, modernizar callbacks para closures/arrow functions, converter globals para dependency injection, e preparar código para migração de frameworks.
---

# Legacy Modernizer

Skill para transformação de código PHP legado em código moderno e maintainable.

## Checklist de Modernização

1. **Sintaxe PHP 8.x** - Type hints, named arguments, match, enums
2. **OOP** - Classes, interfaces, traits, composition
3. **SOLID** - Single responsibility, dependency injection
4. **PSR** - Autoload, coding style, interfaces
5. **Error Handling** - Exceptions em vez de error codes
6. **Testing** - Código testável e desacoplado

## Transformações Comuns

### 1. Sintaxe Moderna

```php
// ❌ ANTES: PHP 5.x
function getUser($id) {
    global $db;
    $result = mysql_query("SELECT * FROM users WHERE id = " . $id);
    if ($result) {
        return mysql_fetch_assoc($result);
    }
    return false;
}

// ✅ DEPOIS: PHP 8.x
function getUser(int $id): ?array
{
    return DB::table('users')->find($id)?->toArray();
}
```

### 2. Type Declarations

```php
// ❌ ANTES
function calcularTotal($items, $desconto) {
    $total = 0;
    foreach ($items as $item) {
        $total += $item['valor'];
    }
    return $total - $desconto;
}

// ✅ DEPOIS
function calcularTotal(array $items, float $desconto = 0): float
{
    $total = array_sum(array_column($items, 'valor'));
    return max(0, $total - $desconto);
}

// ✅ MELHOR: Com objetos
function calcularTotal(Collection $items, float $desconto = 0): float
{
    return max(0, $items->sum('valor') - $desconto);
}
```

### 3. Procedural para OOP

```php
// ❌ ANTES: Funções soltas
function criar_contrato($dados) { ... }
function atualizar_contrato($id, $dados) { ... }
function buscar_contrato($id) { ... }
function listar_contratos($filtros) { ... }

// ✅ DEPOIS: Service Class
class ContractService
{
    public function __construct(
        private ContractRepository $repository,
        private EventDispatcher $events
    ) {}

    public function create(array $data): Contract
    {
        $contract = $this->repository->create($data);
        $this->events->dispatch(new ContractCreated($contract));
        return $contract;
    }

    public function update(int $id, array $data): Contract
    {
        $contract = $this->repository->findOrFail($id);
        $contract->update($data);
        return $contract;
    }

    public function find(int $id): ?Contract
    {
        return $this->repository->find($id);
    }

    public function list(array $filters = []): Collection
    {
        return $this->repository->filter($filters);
    }
}
```

### 4. Global State para DI

```php
// ❌ ANTES: Globals
function enviarEmail($para, $assunto, $corpo) {
    global $config;
    $mail = new PHPMailer();
    $mail->Host = $config['smtp_host'];
    // ...
}

// ✅ DEPOIS: Dependency Injection
class EmailService
{
    public function __construct(
        private readonly MailerInterface $mailer,
        private readonly MailConfig $config
    ) {}

    public function send(string $to, string $subject, string $body): void
    {
        $this->mailer
            ->to($to)
            ->subject($subject)
            ->body($body)
            ->send();
    }
}
```

### 5. Arrays para Value Objects

```php
// ❌ ANTES: Array associativo
$contrato = [
    'cliente' => 'João',
    'valor' => 1500.00,
    'data' => '2024-01-15',
    'status' => 'ativo'
];

// ✅ DEPOIS: DTO/Value Object
readonly class Contract
{
    public function __construct(
        public string $cliente,
        public float $valor,
        public DateTimeImmutable $data,
        public ContractStatus $status
    ) {}

    public static function fromArray(array $data): self
    {
        return new self(
            cliente: $data['cliente'],
            valor: (float) $data['valor'],
            data: new DateTimeImmutable($data['data']),
            status: ContractStatus::from($data['status'])
        );
    }
}

enum ContractStatus: string
{
    case Ativo = 'ativo';
    case Cancelado = 'cancelado';
    case Finalizado = 'finalizado';

    public function label(): string
    {
        return match($this) {
            self::Ativo => 'Ativo',
            self::Cancelado => 'Cancelado',
            self::Finalizado => 'Finalizado',
        };
    }
}
```

### 6. Callbacks para Arrow Functions

```php
// ❌ ANTES: Callback verbose
$ativos = array_filter($contratos, function($c) {
    return $c['status'] == 'ativo';
});

$valores = array_map(function($c) {
    return $c['valor'];
}, $ativos);

$total = array_reduce($valores, function($carry, $v) {
    return $carry + $v;
}, 0);

// ✅ DEPOIS: Arrow functions + Collection
$total = collect($contratos)
    ->filter(fn($c) => $c['status'] === 'ativo')
    ->sum('valor');
```

### 7. Switch para Match

```php
// ❌ ANTES
switch ($status) {
    case 'pending':
        $label = 'Pendente';
        $color = 'yellow';
        break;
    case 'active':
        $label = 'Ativo';
        $color = 'green';
        break;
    case 'cancelled':
        $label = 'Cancelado';
        $color = 'red';
        break;
    default:
        $label = 'Desconhecido';
        $color = 'gray';
}

// ✅ DEPOIS
[$label, $color] = match($status) {
    'pending' => ['Pendente', 'yellow'],
    'active' => ['Ativo', 'green'],
    'cancelled' => ['Cancelado', 'red'],
    default => ['Desconhecido', 'gray'],
};
```

### 8. Error Handling

```php
// ❌ ANTES: Error codes
function processarPagamento($dados) {
    if (!isset($dados['valor'])) {
        return ['erro' => true, 'mensagem' => 'Valor obrigatório'];
    }
    if ($dados['valor'] <= 0) {
        return ['erro' => true, 'mensagem' => 'Valor inválido'];
    }
    // processar...
    return ['erro' => false, 'id' => 123];
}

// ✅ DEPOIS: Exceptions
class PaymentService
{
    public function process(PaymentData $data): Payment
    {
        $this->validate($data);
        
        try {
            return $this->gateway->charge($data);
        } catch (GatewayException $e) {
            throw new PaymentFailedException(
                "Falha no pagamento: {$e->getMessage()}",
                previous: $e
            );
        }
    }

    private function validate(PaymentData $data): void
    {
        if ($data->valor <= 0) {
            throw new InvalidArgumentException('Valor deve ser positivo');
        }
    }
}
```

## Padrão de Migração Incremental

```
1. Criar interfaces para código existente
2. Implementar nova versão atrás da interface
3. Usar feature flags para alternar
4. Remover código antigo após validação
```

```php
// Interface de abstração
interface ContractRepositoryInterface
{
    public function find(int $id): ?Contract;
    public function save(Contract $contract): void;
}

// Implementação legada (wrapper)
class LegacyContractRepository implements ContractRepositoryInterface
{
    public function find(int $id): ?Contract
    {
        $data = buscar_contrato($id); // função legada
        return $data ? Contract::fromArray($data) : null;
    }
}

// Nova implementação
class EloquentContractRepository implements ContractRepositoryInterface
{
    public function find(int $id): ?Contract
    {
        return ContractModel::find($id)?->toDomain();
    }
}

// Service Provider com feature flag
$this->app->bind(
    ContractRepositoryInterface::class,
    config('features.new_repository') 
        ? EloquentContractRepository::class 
        : LegacyContractRepository::class
);
```

## Scripts Úteis

- `scripts/analyze-legacy.php` - Análise de código legado
- `scripts/convert-array-to-dto.php` - Converter arrays em DTOs
