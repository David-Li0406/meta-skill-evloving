---
name: easy-budget-ui-components
description: Use this skill when you need to implement UI components for generating and visualizing PDFs, emails, invoices, and budgets in the Easy Budget system.
---

# Easy Budget UI Components

Esta skill define os componentes Blade específicos para a geração e visualização de PDFs, e-mails, faturas e orçamentos no Easy Budget, seguindo o padrão de components estabelecido no sistema.

## Estrutura de Components

```
resources/views/components/
├── pdf/
│   ├── pdf-header.blade.php         # Cabeçalho padrão de PDFs
│   ├── pdf-footer.blade.php         # Rodapé padrão de PDFs
│   ├── pdf-document.blade.php       # Estrutura base de documentos PDF
│   ├── pdf-budget.blade.php         # Template de orçamento em PDF
│   ├── pdf-invoice.blade.php        # Template de fatura em PDF
│   └── pdf-styles.blade.php         # Estilos CSS para PDFs
├── email/
│   ├── email-header.blade.php        # Cabeçalho padrão de e-mails
│   ├── email-footer.blade.php        # Rodapé padrão de e-mails
│   ├── email-layout.blade.php        # Layout base de e-mails
│   └── email-styles.blade.php        # Estilos CSS para e-mails
├── invoice/
│   ├── invoice-card.blade.php        # Card resumido de fatura
│   ├── invoice-details.blade.php     # Detalhes completos da fatura
│   └── invoice-status.blade.php      # Badge de status da fatura
└── budget/
    ├── budget-card.blade.php          # Card resumido de orçamento
    ├── budget-details.blade.php      # Detalhes completos do orçamento
    └── budget-status.blade.php       # Badge de status do orçamento
```

## 1. PDF Header Component

Componente para cabeçalho padrão de documentos PDF.

### Uso Básico

```blade
<x-pdf.pdf-header :title="$title" :company="$company" :date="$date" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título do documento | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `date` | `string` | Data do documento | `now()` |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |

## 2. Email Header Component

Componente para cabeçalho padrão de e-mails.

### Uso Básico

```blade
<x-email.email-header :title="$title" :company="$company" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `title` | `string` | Título do e-mail | Obrigatório |
| `company` | `array` | Dados da empresa | `[]` |
| `showLogo` | `bool` | Exibir logo da empresa | `true` |

## 3. Invoice Card Component

Componente para exibição resumida de faturas em listas e dashboards.

### Uso Básico

```blade
<x-invoice.invoice-card :invoice="$invoice" :showCustomer="true" :showDueDate="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `invoice` | `Invoice` | Modelo da fatura | Obrigatório |
| `showCustomer` | `bool` | Exibir informações do cliente | `true` |
| `showDueDate` | `bool` | Exibir data de vencimento | `true` |
| `variant` | `string` | Estilo do card (primary, secondary, etc.) | `primary` |

## 4. Budget Card Component

Componente para exibição resumida de orçamentos em listas e dashboards.

### Uso Básico

```blade
<x-budget.budget-card :budget="$budget" :showCustomer="true" :showActions="true" />
```

### Parâmetros

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|--------|
| `budget` | `Budget` | Modelo do orçamento | Obrigatório |
| `showCustomer` | `bool` | Exibir informações do cliente | `true` |
| `showActions` | `bool` | Exibir botões de ação | `true` |
| `variant` | `string` | Estilo do card (primary, secondary, etc.) | `primary` |

## Conclusão

Esses componentes são projetados para facilitar a implementação de funcionalidades de geração e visualização de documentos, e-mails, faturas e orçamentos no sistema Easy Budget, seguindo um padrão consistente e reutilizável.