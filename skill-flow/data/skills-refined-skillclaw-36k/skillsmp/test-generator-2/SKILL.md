---
name: test-generator
description: Geração de testes automatizados em PHP usando PHPUnit e Pest, incluindo testes unitários, de integração, feature tests, e mocks. Usar para criar testes para Models, Services, Controllers, APIs, validar regras de negócio, e aumentar cobertura de código em projetos Laravel.
---

# Test Generator

Skill para criação de testes automatizados em PHPUnit e Pest.

## Estrutura de Testes Laravel

```
tests/
├── Unit/
│   ├── Models/
│   ├── Services/
│   └── Actions/
├── Feature/
│   ├── Api/
│   ├── Http/
│   └── Console/
├── TestCase.php
└── CreatesApplication.php
```

## Testes Unitários

### Model Test

```php
<?php

namespace Tests\Unit\Models;

use App\Models\Contract;
use App\Models\Client;
use App\Models\Payment;
use App\Enums\ContractStatus;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ContractTest extends TestCase
{
    use RefreshDatabase;

    public function test_contract_belongs_to_client(): void
    {
        $client = Client::factory()->create();
        $contract = Contract::factory()->create(['client_id' => $client->id]);

        $this->assertInstanceOf(Client::class, $contract->client);
        $this->assertEquals($client->id, $contract->client->id);
    }

    public function test_contract_has_many_payments(): void
    {
        $contract = Contract::factory()->create();
        Payment::factory()->count(3)->create(['contract_id' => $contract->id]);

        $this->assertCount(3, $contract->payments);
        $this->assertInstanceOf(Payment::class, $contract->payments->first());
    }

    public function test_contract_calculates_total_paid(): void
    {
        $contract = Contract::factory()->create(['value' => 1000]);
        Payment::factory()->create([
            'contract_id' => $contract->id,
            'amount' => 300,
            'status' => 'paid'
        ]);
        Payment::factory()->create([
            'contract_id' => $contract->id,
            'amount' => 200,
            'status' => 'paid'
        ]);
        Payment::factory()->create([
            'contract_id' => $contract->id,
            'amount' => 500,
            'status' => 'pending'
        ]);

        $this->assertEquals(500, $contract->totalPaid());
        $this->assertEquals(500, $contract->remainingBalance());
    }

    public function test_contract_scope_active(): void
    {
        Contract::factory()->count(3)->create(['status' => ContractStatus::Active]);
        Contract::factory()->count(2)->create(['status' => ContractStatus::Pending]);

        $this->assertCount(3, Contract::active()->get());
    }

    public function test_contract_can_be_cancelled_when_pending(): void
    {
        $contract = Contract::factory()->create(['status' => ContractStatus::Pending]);
        
        $this->assertTrue($contract->canBeCancelled());
    }

    public function test_contract_cannot_be_cancelled_when_completed(): void
    {
        $contract = Contract::factory()->create(['status' => ContractStatus::Completed]);
        
        $this->assertFalse($contract->canBeCancelled());
    }
}
```

### Service Test

```php
<?php

namespace Tests\Unit\Services;

use App\Services\ContractService;
use App\Repositories\Contracts\ContractRepositoryInterface;
use App\DTOs\CreateContractDTO;
use App\Models\Contract;
use App\Events\ContractCreated;
use Illuminate\Support\Facades\Event;
use Mockery;
use Tests\TestCase;

class ContractServiceTest extends TestCase
{
    private ContractService $service;
    private $repository;

    protected function setUp(): void
    {
        parent::setUp();
        
        $this->repository = Mockery::mock(ContractRepositoryInterface::class);
        $this->service = new ContractService($this->repository);
    }

    public function test_create_contract_successfully(): void
    {
        Event::fake();

        $dto = new CreateContractDTO(
            clientId: 1,
            value: 1000.00,
            eventDate: new \DateTimeImmutable('2024-06-15')
        );

        $expectedContract = new Contract([
            'id' => 1,
            'client_id' => 1,
            'value' => 1000.00,
            'event_date' => '2024-06-15'
        ]);

        $this->repository
            ->shouldReceive('create')
            ->once()
            ->with($dto->toArray())
            ->andReturn($expectedContract);

        $result = $this->service->create($dto);

        $this->assertInstanceOf(Contract::class, $result);
        $this->assertEquals(1000.00, $result->value);
        Event::assertDispatched(ContractCreated::class);
    }

    public function test_cancel_contract_throws_exception_when_not_cancellable(): void
    {
        $contract = Mockery::mock(Contract::class);
        $contract->shouldReceive('canBeCancelled')->once()->andReturn(false);

        $this->expectException(\App\Exceptions\ContractCannotBeCancelledException::class);

        $this->service->cancel($contract, 'Motivo');
    }

    protected function tearDown(): void
    {
        Mockery::close();
        parent::tearDown();
    }
}
```

## Feature Tests (API)

```php
<?php

namespace Tests\Feature\Api;

use App\Models\User;
use App\Models\Client;
use App\Models\Contract;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Sanctum\Sanctum;
use Tests\TestCase;

class ContractApiTest extends TestCase
{
    use RefreshDatabase;

    private User $user;

    protected function setUp(): void
    {
        parent::setUp();
        $this->user = User::factory()->create();
    }

    public function test_can_list_contracts(): void
    {
        Sanctum::actingAs($this->user);
        Contract::factory()->count(5)->create();

        $response = $this->getJson('/api/contracts');

        $response
            ->assertOk()
            ->assertJsonStructure([
                'data' => [
                    '*' => ['id', 'client_id', 'value', 'status', 'event_date']
                ],
                'meta' => ['current_page', 'total']
            ])
            ->assertJsonCount(5, 'data');
    }

    public function test_can_create_contract(): void
    {
        Sanctum::actingAs($this->user);
        $client = Client::factory()->create();

        $payload = [
            'client_id' => $client->id,
            'event_date' => '2024-06-15',
            'value' => 5000.00,
            'notes' => 'Teste'
        ];

        $response = $this->postJson('/api/contracts', $payload);

        $response
            ->assertCreated()
            ->assertJsonPath('data.client_id', $client->id)
            ->assertJsonPath('data.value', 5000.00);

        $this->assertDatabaseHas('contracts', [
            'client_id' => $client->id,
            'value' => 5000.00
        ]);
    }

    public function test_create_contract_validates_required_fields(): void
    {
        Sanctum::actingAs($this->user);

        $response = $this->postJson('/api/contracts', []);

        $response
            ->assertUnprocessable()
            ->assertJsonValidationErrors(['client_id', 'event_date', 'value']);
    }

    public function test_can_update_contract(): void
    {
        Sanctum::actingAs($this->user);
        $contract = Contract::factory()->create(['value' => 1000]);

        $response = $this->putJson("/api/contracts/{$contract->id}", [
            'value' => 2000.00
        ]);

        $response
            ->assertOk()
            ->assertJsonPath('data.value', 2000.00);

        $this->assertDatabaseHas('contracts', [
            'id' => $contract->id,
            'value' => 2000.00
        ]);
    }

    public function test_can_delete_contract(): void
    {
        Sanctum::actingAs($this->user);
        $contract = Contract::factory()->create();

        $response = $this->deleteJson("/api/contracts/{$contract->id}");

        $response->assertNoContent();
        $this->assertSoftDeleted('contracts', ['id' => $contract->id]);
    }

    public function test_returns_404_for_nonexistent_contract(): void
    {
        Sanctum::actingAs($this->user);

        $response = $this->getJson('/api/contracts/99999');

        $response->assertNotFound();
    }

    public function test_unauthenticated_user_cannot_access(): void
    {
        $response = $this->getJson('/api/contracts');

        $response->assertUnauthorized();
    }
}
```

## Pest Syntax

```php
<?php

use App\Models\Contract;
use App\Models\Client;
use App\Models\User;

beforeEach(function () {
    $this->user = User::factory()->create();
    $this->actingAs($this->user);
});

describe('Contract API', function () {
    
    it('lists contracts with pagination', function () {
        Contract::factory()->count(20)->create();

        $response = $this->getJson('/api/contracts?per_page=10');

        expect($response->json('data'))->toHaveCount(10)
            ->and($response->json('meta.total'))->toBe(20);
    });

    it('creates a contract', function () {
        $client = Client::factory()->create();

        $response = $this->postJson('/api/contracts', [
            'client_id' => $client->id,
            'event_date' => '2024-06-15',
            'value' => 5000.00,
        ]);

        expect($response->status())->toBe(201)
            ->and($response->json('data.value'))->toBe(5000.00);
    });

    it('validates required fields', function () {
        $response = $this->postJson('/api/contracts', []);

        expect($response->status())->toBe(422)
            ->and($response->json('errors'))->toHaveKeys(['client_id', 'event_date', 'value']);
    });

});

describe('Contract Model', function () {

    it('belongs to a client', function () {
        $contract = Contract::factory()->create();

        expect($contract->client)->toBeInstanceOf(Client::class);
    });

    it('calculates remaining balance', function () {
        $contract = Contract::factory()
            ->has(Payment::factory()->state(['amount' => 300, 'status' => 'paid']))
            ->create(['value' => 1000]);

        expect($contract->remainingBalance())->toBe(700.0);
    });

});
```

## Data Providers

```php
<?php

/**
 * @dataProvider invalidContractDataProvider
 */
public function test_validation_fails_for_invalid_data(array $data, string $expectedError): void
{
    Sanctum::actingAs($this->user);

    $response = $this->postJson('/api/contracts', $data);

    $response->assertJsonValidationErrors([$expectedError]);
}

public static function invalidContractDataProvider(): array
{
    return [
        'missing client_id' => [
            ['event_date' => '2024-06-15', 'value' => 1000],
            'client_id'
        ],
        'invalid date format' => [
            ['client_id' => 1, 'event_date' => 'invalid', 'value' => 1000],
            'event_date'
        ],
        'negative value' => [
            ['client_id' => 1, 'event_date' => '2024-06-15', 'value' => -100],
            'value'
        ],
        'past event date' => [
            ['client_id' => 1, 'event_date' => '2020-01-01', 'value' => 1000],
            'event_date'
        ],
    ];
}
```

## Comandos

```bash
# Executar todos os testes
php artisan test

# Executar com coverage
php artisan test --coverage

# Executar grupo específico
php artisan test --group=api

# Executar arquivo específico
php artisan test tests/Feature/Api/ContractApiTest.php

# Pest com filtro
./vendor/bin/pest --filter="creates a contract"
```
