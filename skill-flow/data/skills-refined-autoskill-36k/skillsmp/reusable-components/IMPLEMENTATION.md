# Guia de Implementação de Componentes Reutilizáveis

## 🚀 Como Começar

Este guia prático ajuda a equipe de desenvolvimento a implementar e usar os componentes reutilizáveis no sistema Easy Budget Laravel.

## 📋 Checklist de Implementação

### **✅ Passo 1: Estrutura de Componentes**

```bash
# Verificar estrutura de componentes existente
resources/views/components/
├── button.blade.php
├── modal.blade.php
├── status-badge.blade.php
├── table-actions.blade.php
├── page-header.blade.php
└── [outros componentes existentes]
```

### **✅ Passo 2: Identificar Páginas para Refatorar**

Priorizar páginas com maior duplicação de código:

1. **Páginas de listagem** (Categories, Products, Customers, Budgets, Services, Invoices)
2. **Páginas de formulário** (Create, Edit)
3. **Páginas de detalhes** (Show)
4. **Dashboards** (Principal e específicos)

### **✅ Passo 3: Implementar Componentes Faltantes**

Baseado na skill, implementar componentes que ainda não existem:

#### **Componentes Prioritários (Nível 1)**

```php
// 1. Resource Table (Tabela de Recursos)
resources/views/components/resource-table.blade.php

// 2. Filter Field (Campo de Filtro)
resources/views/components/filter-field.blade.php

// 3. Table Header Actions (Cabeçalho de Ações)
resources/views/components/table-header-actions.blade.php

// 4. Confirm Modal (Modal de Confirmação)
resources/views/components/confirm-modal.blade.php

// 5. Stat Card (Card de Estatísticas)
resources/views/components/stat-card.blade.php
```

#### **Componentes de Suporte (Nível 2)**

```php
// 6. Resource Info (Informação de Recurso)
resources/views/components/resource-info.blade.php

// 7. Movement Type Badge (Badge de Tipo de Movimento)
resources/views/components/movement-type-badge.blade.php

// 8. Movement Quantity (Quantidade de Movimento)
resources/views/components/movement-quantity.blade.php

// 9. Empty State (Estado Vazio)
resources/views/components/empty-state.blade.php

// 10. File Upload (Upload de Arquivo)
resources/views/components/file-upload.blade.php
```

## 🔧 Implementação dos Componentes

### **1. Resource Table (Tabela de Recursos)**

```blade
{{-- resources/views/components/resource-table.blade.php --}}
@props([
    'items',                     // Coleção de itens
    'columns',                   // Definição de colunas
    'actions' => true,           // Exibir coluna de ações
    'mobileActions' => false,    // Ações em mobile
    'emptyMessage' => 'Nenhum registro encontrado', // Mensagem vazia
    'sortable' => true,          // Permite ordenação
])

<div {{ $attributes->merge(['class' => 'table-responsive']) }}>
    <table class="table table-hover {{ $sortable ? 'sortable-table' : '' }}">
        <thead>
            <tr>
                @foreach($columns as $column)
                    <th @if(isset($column['sortable']) && $column['sortable']) class="sortable" data-field="{{ $column['field'] }}" @endif>
                        {{ $column['label'] }}
                        @if(isset($column['sortable']) && $column['sortable'])
                            <i class="bi bi-arrow-down-up ms-1"></i>
                        @endif
                    </th>
                @endforeach
                @if($actions)
                    <th class="text-center">Ações</th>
                @endif
            </tr>
        </thead>
        <tbody>
            @if($items->isEmpty())
                <tr>
                    <td colspan="{{ count($columns) + ($actions ? 1 : 0) }}" class="text-center text-muted py-4">
                        <i class="bi bi-inbox" style="font-size: 2rem;"></i>
                        <p class="mt-2 mb-0">{{ $emptyMessage }}</p>
                    </td>
                </tr>
            @else
                {{ $slot }}
            @endif
        </tbody>
    </table>
</div>

{{-- Paginação --}}
@if($items->hasPages())
    <div class="d-flex justify-content-between align-items-center mt-3">
        <div class="text-muted">
            Mostrando {{ $items->firstItem() }} a {{ $items->lastItem() }} de {{ $items->total() }} registros
        </div>
        {{ $items->appends(request()->query())->links() }}
    </div>
@endif

@push('scripts')
<script>
document.addEventListener('DOMContentLoaded', function() {
    @if($sortable)
        // Lógica de ordenação
        document.querySelectorAll('.sortable').forEach(function(th) {
            th.addEventListener('click', function() {
                const field = this.getAttribute('data-field');
                const currentOrder = new URLSearchParams(window.location.search).get('order') || 'asc';
                const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';

                const url = new URL(window.location);
                url.searchParams.set('order_by', field);
                url.searchParams.set('order', newOrder);

                window.location.href = url.toString();
            });
        });
    @endif
});
</script>
@endpush
```

### **2. Filter Field (Campo de Filtro)**

```blade
{{-- resources/views/components/filter-field.blade.php --}}
@props([
    'name',                      // Nome do campo
    'label',                     // Rótulo do campo
    'value' => '',               // Valor atual
    'type' => 'text',            // Tipo do campo
    'options' => [],             // Opções para selects
    'placeholder' => '',         // Placeholder
    'class' => '',               // Classes CSS adicionais
    'clearable' => true,         // Mostrar botão de limpar
])

<div {{ $attributes->merge(['class' => 'filter-field ' . $class]) }}>
    @if($type === 'select')
        <select name="{{ $name }}" class="form-select" {{ $attributes }}>
            <option value="">{{ $placeholder ?: 'Selecione...' }}</option>
            @foreach($options as $value => $label)
                <option value="{{ $value }}" {{ ($value == $value) ? 'selected' : '' }}>
                    {{ $label }}
                </option>
            @endforeach
        </select>
    @elseif($type === 'date')
        <input
            type="date"
            name="{{ $name }}"
            value="{{ $value }}"
            class="form-control"
            {{ $attributes }}
        >
    @else
        <input
            type="{{ $type }}"
            name="{{ $name }}"
            value="{{ $value }}"
            placeholder="{{ $placeholder }}"
            class="form-control"
            {{ $attributes }}
        >
    @endif

    {{-- Botão de limpar --}}
    @if($clearable && $value)
        <button type="button" class="btn btn-outline-secondary btn-sm ms-2" onclick="clearFilter('{{ $name }}')">
            <i class="bi bi-x-circle"></i>
        </button>
    @endif
</div>

@push('scripts')
<script>
function clearFilter(fieldName) {
    const input = document.querySelector(`[name="${fieldName}"]`);
    if (input) {
        input.value = '';
        input.form.submit();
    }
}
</script>
@endpush
```

### **3. Table Header Actions (Cabeçalho de Ações)**

```blade
{{-- resources/views/components/table-header-actions.blade.php --}}
@props([
    'title' => '',               // Título da tabela
    'actions' => [],             // Botões de ação
    'filters' => false,          // Exibir filtros
    'search' => true,            // Exibir busca
])

<div class="d-flex justify-content-between align-items-center mb-3">
    <div>
        <h5 class="mb-0">{{ $title }}</h5>
        @if($slot->isNotEmpty())
            <div class="text-muted small">{{ $slot }}</div>
        @endif
    </div>

    <div class="d-flex gap-2 align-items-center">
        {{-- Busca rápida --}}
        @if($search)
            <div class="input-group" style="width: 300px;">
                <input type="text" class="form-control" placeholder="Buscar..." id="quickSearch">
                <button class="btn btn-outline-secondary" type="button">
                    <i class="bi bi-search"></i>
                </button>
            </div>
        @endif

        {{-- Botões de ação --}}
        @foreach($actions as $action)
            <x-button
                :type="$action['type'] ?? 'link'"
                :href="$action['url'] ?? '#'"
                :variant="$action['variant'] ?? 'primary'"
                :icon="$action['icon'] ?? null"
                :label="$action['label'] ?? ''"
                {{ $action['attributes'] ?? '' }}
            />
        @endforeach

        {{-- Ícone de filtros --}}
        @if($filters)
            <button class="btn btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#filtersCollapse">
                <i class="bi bi-funnel"></i>
            </button>
        @endif
    </div>
</div>

{{-- Área de filtros --}}
@if($filters)
    <div class="collapse mb-3" id="filtersCollapse">
        <div class="card card-body">
            {{ $filters }}
        </div>
    </div>
@endif

@push('scripts')
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Busca rápida
    const searchInput = document.getElementById('quickSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                // Implementar lógica de busca
                console.log('Buscando:', this.value);
            }
        });
    }
});
</script>
@endpush
```

### **4. Confirm Modal (Modal de Confirmação)**

```blade
{{-- resources/views/components/confirm-modal.blade.php --}}
@props([
    'id',                        // ID do modal
    'title',                     // Título do modal
    'message',                   // Mensagem de confirmação
    'confirmText' => 'Confirmar', // Texto do botão de confirmação
    'cancelText' => 'Cancelar',   // Texto do botão de cancelar
    'confirmClass' => 'btn-danger', // Classe do botão de confirmação
    'size' => 'modal-sm',        // Tamanho do modal
])

<div class="modal fade" id="{{ $id }}" tabindex="-1" aria-labelledby="{{ $id }}Label" aria-hidden="true">
    <div class="modal-dialog {{ $size }} modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="{{ $id }}Label">{{ $title }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>
            </div>
            <div class="modal-body">
                @if(str_contains($message, '<'))
                    {!! $message !!}
                @else
                    <p>{{ $message }}</p>
                @endif
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">{{ $cancelText }}</button>
                <button type="button" class="btn {{ $confirmClass }}" id="{{ $id }}ConfirmBtn">
                    {{ $confirmText }}
                </button>
            </div>
        </div>
    </div>
</div>

@push('scripts')
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Configurar ação de confirmação
    const confirmBtn = document.getElementById('{{ $id }}ConfirmBtn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', function() {
            // Evento personalizado para ser capturado pelo componente pai
            const event = new CustomEvent('{{ $id }}Confirmed', {
                detail: { confirmed: true }
            });
            window.dispatchEvent(event);

            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('{{ $id }}'));
            if (modal) {
                modal.hide();
            }
        });
    }
});
</script>
@endpush
```

### **5. Stat Card (Card de Estatísticas)**

```blade
{{-- resources/views/components/stat-card.blade.php --}}
@props([
    'title',
    'value',
    'description' => null,
    'icon' => null,
    'variant' => 'primary', // primary, success, info, warning, danger, secondary
    'gradient' => true,
    'isCustom' => false, // Para col-xl-5-custom
])

<div class="{{ $isCustom ? 'col-12 col-md-6 col-xl-5-custom' : 'col-12 col-md-6 col-lg-3' }}">
    <div @class([
        'card border-0 shadow-sm h-100',
        "bg-$variant" => $gradient && $variant === 'primary',
        "bg-gradient text-white" => $gradient && $variant === 'primary',
    ])>
        <div class="card-body p-3 d-flex flex-column justify-content-between">
            <div class="d-flex align-items-center mb-2">
                @if($icon)
                    <div @class([
                        'avatar-circle me-2',
                        'bg-white bg-opacity-25' => $variant === 'primary' && $gradient,
                        "bg-$variant bg-gradient" => !($variant === 'primary' && $gradient)
                    ]) style="width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; border-radius: 50%;">
                        <i class="bi bi-{{ $icon }} text-white" style="font-size: 0.9rem;"></i>
                    </div>
                @endif
                <h6 @class([
                    'mb-0 small fw-bold',
                    'text-white text-opacity-75' => $variant === 'primary' && $gradient,
                    'text-muted' => !($variant === 'primary' && $gradient)
                ])>{{ strtoupper($title) }}</h6>
            </div>
            <h3 @class([
                'mb-1 fw-bold',
                'text-white' => $variant === 'primary' && $gradient,
                "text-$variant" => !($variant === 'primary' && $gradient)
            ])>{{ $value }}</h3>
            @if($description)
                <p @class([
                    'small-text mb-0',
                    'text-white text-opacity-75' => $variant === 'primary' && $gradient,
                    'text-muted' => !($variant === 'primary' && $gradient)
                ])>{{ $description }}</p>
            @endif
        </div>
    </div>
</div>
```

## 🔄 Refatoração de Páginas Existentes

### **Processo de Refatoração**

#### **Passo 1: Analisar Página Atual**

```php
// Exemplo: resources/views/pages/product/index.blade.php
// Identificar:
// - Estrutura de cabeçalho
// - Formulário de filtros
// - Tabela de dados
// - Botões de ação
// - Modais
// - JavaScript
```

#### **Passo 2: Substituir por Componentes**

```blade
{{-- Antes --}}
<div class="d-flex justify-content-between align-items-center">
    <div>
        <h1 class="h3 mb-0">Gerenciar Produtos</h1>
        <p class="text-muted mb-0">Controle seu catálogo de produtos</p>
    </div>
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb mb-0">
            <li class="breadcrumb-item"><a href="{{ route('provider.dashboard') }}">Dashboard</a></li>
            <li class="breadcrumb-item active" aria-current="page">Produtos</li>
        </ol>
    </nav>
</div>

{{-- Depois --}}
<x-page-header
    title="Gerenciar Produtos"
    icon="box"
    :breadcrumb-items="[
        'Dashboard' => route('provider.dashboard'),
        'Produtos' => '#'
    ]">
    <p class="text-muted mb-0">Controle seu catálogo de produtos</p>
</x-page-header>
```

#### **Passo 3: Testar Funcionalidades**

```bash
# Testar:
# 1. Responsividade
# 2. Funcionalidade dos filtros
# 3. Paginação
# 4. Ações de botões
# 5. Modais de confirmação
# 6. JavaScript
```

## 🧪 Testes de Componentes

### **Testes Unitários**

```php
// tests/Feature/Components/ResourceTableTest.php
namespace Tests\Feature\Components;

use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

class ResourceTableTest extends TestCase
{
    public function test_resource_table_renders_correctly()
    {
        $response = $this->get('/provider/products');

        $response->assertStatus(200);
        $response->assertSee('Lista de Produtos');
        $response->assertSee('Nome');
        $response->assertSee('Preço');
        $response->assertSee('Status');
    }

    public function test_empty_state_displays_correctly()
    {
        // Testar quando não há registros
        $response = $this->get('/provider/products?search=nonexistent');

        $response->assertStatus(200);
        $response->assertSee('Nenhum produto encontrado');
    }
}
```

### **Testes de Integração**

```php
// tests/Feature/Components/FilterFieldTest.php
namespace Tests\Feature\Components;

use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

class FilterFieldTest extends TestCase
{
    public function test_filter_field_applies_filters()
    {
        $response = $this->get('/provider/products?status=1');

        $response->assertStatus(200);
        // Verificar se os filtros foram aplicados corretamente
    }

    public function test_filter_field_clears_filters()
    {
        $response = $this->get('/provider/products?search=test');

        $response->assertStatus(200);
        $response->assertSee('test');

        // Testar limpeza de filtros
        $response = $this->get('/provider/products');
        $response->assertDontSee('test');
    }
}
```

## 📊 Métricas de Sucesso

### **Indicadores de Performance**

```php
// Métricas a serem monitoradas:
// 1. Tempo de carregamento de páginas
// 2. Tamanho do bundle JavaScript
// 3. Tamanho do bundle CSS
// 4. Número de linhas de código duplicado
// 5. Tempo de desenvolvimento de novas funcionalidades
```

### **Indicadores de Qualidade**

```php
// Métricas de qualidade:
// 1. Cobertura de testes
// 2. Consistência visual
// 3. Experiência do usuário
// 4. Manutenibilidade do código
// 5. Satisfação da equipe de desenvolvimento
```

## 🚨 Problemas Comuns e Soluções

### **Problema 1: Componentes não são encontrados**

```bash
# Solução: Verificar a estrutura de diretórios
resources/views/components/
├── button.blade.php
├── modal.blade.php
└── [outros componentes]

# Verificar se o componente está no caminho correto
# O Laravel procura componentes em resources/views/components/
```

### **Problema 2: Props não estão funcionando**

```blade
{{-- Verificar a sintaxe das props --}}
<x-component
    :prop-name="$value"
    prop-string="valor"
    :prop-array="['a', 'b', 'c']"
/>

{{-- Verificar se as props estão definidas no componente --}}
@props([
    'propName' => 'default',
    'propString' => '',
    'propArray' => [],
])
```

### **Problema 3: Estilos não são aplicados**

```blade
{{-- Verificar a ordem dos imports no layout --}}
{{-- CSS deve vir antes de JavaScript --}}
<link href="{{ asset('css/app.css') }}" rel="stylesheet">
<script src="{{ asset('js/app.js') }}"></script>

{{-- Verificar se as classes CSS existem --}}
{{-- Usar classes do Bootstrap ou classes customizadas definidas no CSS --}}
```

### **Problema 4: JavaScript não funciona**

```blade
{{-- Verificar a ordem dos scripts --}}
{{-- Scripts devem ser carregados após o DOM --}}
@push('scripts')
<script>
    // Código JavaScript aqui
</script>
@endpush

{{-- Verificar se o script está no final do body --}}
{{-- Ou usar document.addEventListener('DOMContentLoaded') --}}
```

## 📚 Documentação e Treinamento

### **Documentação para a Equipe**

1. **Guia de Componentes** - Como usar cada componente
2. **Exemplos de Código** - Casos de uso reais
3. **Boas Práticas** - Padrões de desenvolvimento
4. **Troubleshooting** - Solução de problemas comuns

### **Treinamento da Equipe**

1. **Workshop de Componentes** - Sessão prática de implementação
2. **Code Review** - Revisão de código com foco em componentes
3. **Pair Programming** - Programação em dupla para aprendizado
4. **Mentoria** - Acompanhamento de desenvolvedores menos experientes

## 🎯 Próximos Passos

### **Fase 1: Implementação Básica (1-2 semanas)**

- [ ] Implementar componentes prioritários
- [ ] Refatorar páginas de listagem principais
- [ ] Testar funcionalidades básicas
- [ ] Documentar componentes implementados

### **Fase 2: Expansão (2-3 semanas)**

- [ ] Implementar componentes de upload
- [ ] Refatorar páginas de formulário
- [ ] Implementar componentes mobile
- [ ] Criar testes automatizados

### **Fase 3: Otimização (1-2 semanas)**

- [ ] Otimizar performance
- [ ] Melhorar acessibilidade
- [ ] Implementar temas
- [ ] Documentação completa

### **Fase 4: Manutenção (Contínuo)**

- [ ] Monitorar métricas de sucesso
- [ ] Corrigir bugs e melhorias
- [ ] Atualizar documentação
- [ ] Treinar novos desenvolvedores

---

**Última atualização:** 11/01/2026 - Guia completo de implementação dos componentes reutilizáveis
