---
name: code-explainer
description: Explicação detalhada de código complexo ou legado, incluindo análise linha por linha, identificação de padrões, documentação de fluxos, e tradução de lógica para linguagem natural. Usar para entender código de terceiros, documentar sistemas legados, onboarding de novos desenvolvedores, e criar documentação técnica.
---

# Code Explainer

Skill para análise e explicação de código complexo.

## Metodologia de Análise

### 1. Visão Geral

```markdown
## Sumário do Código
- **Arquivo**: path/to/file.php
- **Propósito**: [O que este código faz em uma frase]
- **Tipo**: [Controller/Service/Model/Helper/etc]
- **Dependências**: [Outras classes/funções utilizadas]
- **Complexidade**: [Baixa/Média/Alta]
```

### 2. Análise por Blocos

```php
<?php
// ============================================================
// BLOCO 1: Configuração e Dependências
// ============================================================
namespace App\Services;

use App\Models\Contract;           // Model de contratos
use App\Repositories\PaymentRepo;  // Repositório de pagamentos
use Illuminate\Support\Facades\DB; // Facade de database
use Carbon\Carbon;                 // Manipulação de datas

// ============================================================
// BLOCO 2: Definição da Classe
// ============================================================
class ContractBillingService
{
    // Injeção de dependência via construtor (padrão DI)
    public function __construct(
        private PaymentRepo $payments,  // Acesso a pagamentos
        private NotificationService $notify  // Envio de notificações
    ) {}

    // ============================================================
    // BLOCO 3: Método Principal
    // ============================================================
    /**
     * Gera cobranças para contratos ativos
     * 
     * FLUXO:
     * 1. Busca contratos elegíveis
     * 2. Para cada contrato, calcula valor
     * 3. Cria registro de pagamento
     * 4. Notifica cliente
     */
    public function generateMonthlyBillings(): int
    {
        // Inicia transação para garantir atomicidade
        // Se algo falhar, tudo é revertido
        return DB::transaction(function () {
            
            // Query complexa explicada:
            // - active(): scope que filtra status='active'
            // - whereDoesntHave(): contratos SEM pagamento neste mês
            // - with(): eager load para evitar N+1
            $contracts = Contract::active()
                ->whereDoesntHave('payments', function ($q) {
                    $q->whereMonth('due_date', now()->month)
                      ->whereYear('due_date', now()->year);
                })
                ->with(['client', 'items'])
                ->get();

            $count = 0;

            foreach ($contracts as $contract) {
                // Calcula valor com base nos itens
                // Método privado abaixo
                $amount = $this->calculateAmount($contract);

                // Cria pagamento via repositório
                // Abstração que esconde a implementação
                $payment = $this->payments->create([
                    'contract_id' => $contract->id,
                    'amount' => $amount,
                    'due_date' => now()->addDays(10),
                    'status' => 'pending',
                ]);

                // Dispara notificação assíncrona (queue)
                $this->notify->billingGenerated($contract->client, $payment);

                $count++;
            }

            return $count;
        });
    }

    // ============================================================
    // BLOCO 4: Métodos Auxiliares
    // ============================================================
    
    /**
     * Calcula valor total do contrato
     * Soma itens + aplica taxa administrativa de 5%
     */
    private function calculateAmount(Contract $contract): float
    {
        // items->sum('total'): soma coluna 'total' de todos os itens
        $subtotal = $contract->items->sum('total');
        
        // Taxa administrativa fixa de 5%
        $adminFee = $subtotal * 0.05;
        
        return round($subtotal + $adminFee, 2);
    }
}
```

## Padrões de Explicação

### Para Código Legado

```php
// CÓDIGO ORIGINAL (difícil de entender)
function proc_ctr($d, $f = 1) {
    global $conn;
    $r = mysql_query("SELECT * FROM ctr WHERE st = 'A' AND dt < '" . date('Y-m-d') . "'", $conn);
    while ($row = mysql_fetch_assoc($r)) {
        if ($f) {
            $v = $row['vl'] * 1.1;
            mysql_query("INSERT INTO pg VALUES (NULL, {$row['id']}, $v, NOW())", $conn);
        }
    }
    return mysql_affected_rows();
}

// EXPLICAÇÃO DETALHADA:
/*
┌─────────────────────────────────────────────────────────────┐
│ FUNÇÃO: proc_ctr (processar contratos)                      │
├─────────────────────────────────────────────────────────────┤
│ PARÂMETROS:                                                 │
│   $d - [NÃO UTILIZADO - possível código morto]              │
│   $f - Flag para gerar pagamentos (default: 1 = sim)        │
├─────────────────────────────────────────────────────────────┤
│ O QUE FAZ:                                                  │
│   1. Busca contratos com status 'A' (Ativo)                 │
│   2. Filtra por data anterior a hoje                        │
│   3. Para cada contrato encontrado:                         │
│      - Se flag $f = true:                                   │
│        - Calcula valor com 10% de acréscimo                 │
│        - Insere novo pagamento                              │
│   4. Retorna quantidade de registros afetados               │
├─────────────────────────────────────────────────────────────┤
│ PROBLEMAS IDENTIFICADOS:                                    │
│   ❌ SQL Injection vulnerável                               │
│   ❌ Variável global $conn                                  │
│   ❌ mysql_* funções deprecated                             │
│   ❌ Parâmetro $d não utilizado                             │
│   ❌ Nomes de variáveis não descritivos                     │
│   ❌ Sem tratamento de erros                                │
│   ❌ Número mágico 1.1 (10% hardcoded)                      │
└─────────────────────────────────────────────────────────────┘
*/

// VERSÃO REFATORADA EQUIVALENTE:
class ContractProcessor
{
    private const ADMIN_FEE_PERCENTAGE = 0.10; // 10%

    public function processActiveContracts(bool $generatePayments = true): int
    {
        $contracts = Contract::where('status', 'active')
            ->where('date', '<', now())
            ->get();

        $count = 0;

        foreach ($contracts as $contract) {
            if ($generatePayments) {
                $amount = $contract->value * (1 + self::ADMIN_FEE_PERCENTAGE);
                
                Payment::create([
                    'contract_id' => $contract->id,
                    'amount' => $amount,
                    'created_at' => now(),
                ]);
                
                $count++;
            }
        }

        return $count;
    }
}
```

### Para Regex Complexo

```php
// REGEX ORIGINAL
$pattern = '/^(?:(?:\+|00)55\s?)?(?:\(?0?[1-9]{2}\)?\s?)?(?:9\s?)?[6-9]\d{3}[\s.-]?\d{4}$/';

// EXPLICAÇÃO DETALHADA:
/*
┌─────────────────────────────────────────────────────────────┐
│ REGEX: Validação de telefone brasileiro                     │
├─────────────────────────────────────────────────────────────┤
│ ESTRUTURA:                                                  │
│                                                             │
│ ^                      Início da string                     │
│ (?:(?:\+|00)55\s?)?   Código país opcional (+55 ou 0055)   │
│ (?:\(?0?[1-9]{2}\)?\s?)?  DDD opcional (11-99, com/sem 0)  │
│ (?:9\s?)?             Nono dígito opcional                  │
│ [6-9]\d{3}            Primeiro bloco (começa com 6-9)       │
│ [\s.-]?               Separador opcional (espaço/ponto/-)   │
│ \d{4}                 Segundo bloco (4 dígitos)             │
│ $                     Fim da string                         │
├─────────────────────────────────────────────────────────────┤
│ EXEMPLOS VÁLIDOS:                                           │
│   ✅ 11999998888                                            │
│   ✅ (11) 99999-8888                                        │
│   ✅ +55 11 99999-8888                                      │
│   ✅ 0055 (011) 9 9999-8888                                 │
│   ✅ 99999-8888                                             │
├─────────────────────────────────────────────────────────────┤
│ EXEMPLOS INVÁLIDOS:                                         │
│   ❌ 1199999888 (9 dígitos)                                 │
│   ❌ 11199998888 (DDD 111)                                  │
│   ❌ 11599998888 (começa com 5)                             │
└─────────────────────────────────────────────────────────────┘
*/
```

### Para Query SQL Complexa

```sql
-- QUERY ORIGINAL
SELECT c.*, 
       cl.name as client_name,
       COALESCE(SUM(p.amount), 0) as total_paid,
       c.value - COALESCE(SUM(p.amount), 0) as balance
FROM contracts c
LEFT JOIN clients cl ON c.client_id = cl.id
LEFT JOIN payments p ON p.contract_id = c.id AND p.status = 'paid'
WHERE c.status = 'active'
  AND c.event_date BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY c.id
HAVING balance > 0
ORDER BY balance DESC, c.event_date ASC;

-- EXPLICAÇÃO:
/*
┌─────────────────────────────────────────────────────────────┐
│ PROPÓSITO: Listar contratos ativos com saldo em aberto      │
├─────────────────────────────────────────────────────────────┤
│ ESTRUTURA:                                                  │
│                                                             │
│ SELECT:                                                     │
│   c.*                     Todas colunas do contrato         │
│   cl.name AS client_name  Nome do cliente (join)            │
│   COALESCE(SUM(p.amount), 0)  Total pago (0 se null)       │
│   c.value - ...           Saldo restante calculado          │
│                                                             │
│ FROM contracts c          Tabela principal                  │
│                                                             │
│ LEFT JOIN clients         Traz cliente mesmo sem match      │
│ LEFT JOIN payments        Traz pagamentos APENAS 'paid'     │
│                                                             │
│ WHERE:                                                      │
│   status = 'active'       Apenas contratos ativos           │
│   event_date BETWEEN      Eventos do ano de 2024            │
│                                                             │
│ GROUP BY c.id             Agrupa pagamentos por contrato    │
│                                                             │
│ HAVING balance > 0        Filtra APÓS agregação             │
│                           (só com saldo positivo)           │
│                                                             │
│ ORDER BY:                                                   │
│   balance DESC            Maiores saldos primeiro           │
│   event_date ASC          Eventos mais próximos primeiro    │
└─────────────────────────────────────────────────────────────┘
*/
```

## Template de Documentação

```markdown
# Documentação: [Nome do Arquivo/Classe]

## Visão Geral
[Descrição em 2-3 frases do propósito deste código]

## Responsabilidades
- [Responsabilidade 1]
- [Responsabilidade 2]

## Dependências
| Classe/Função | Propósito |
|---------------|-----------|
| Class1 | Descrição |
| Class2 | Descrição |

## Métodos Públicos

### methodName(params): ReturnType
**Propósito**: [O que faz]
**Parâmetros**:
- `param1`: Descrição
- `param2`: Descrição
**Retorno**: Descrição
**Exceções**: ExceptionType - quando ocorre

## Fluxo Principal
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Notas Importantes
- [Nota sobre comportamento específico]
- [Nota sobre edge cases]
```
