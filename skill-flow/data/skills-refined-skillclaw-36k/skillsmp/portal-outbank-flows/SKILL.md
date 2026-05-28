---
name: portal-outbank-flows
description: Mapa de fluxos de negócio do portal-outbank. Documenta hierarquias, dependências e integridade do sistema. Use para entender impactos antes de modificar código.
---

# Portal Outbank - Mapa de Fluxos de Negócio

> **Propósito:** Documentar os fluxos corretos do sistema para evitar quebras acidentais.
> **Protocolo de Validação:** Fluxos marcados com ✅ foram validados pelo usuário.
> **Última atualização:** 24/01/2026

---

## 🔄 FLUXO 1: Configuração de Taxas MDR (Portal Admin → ISO → Merchant)

### Status: ✅ VALIDADO

*(Detalhes do Fluxo 1 mantidos conformer versões anteriores...)*

---

## 🔄 FLUXO 2: Margens de Usuários (Portal → Fechamento → Repasse)

### Status: ✅ VALIDADO

*(Detalhes do Fluxo 2 mantidos conformer versões anteriores...)*

---

## 🔄 FLUXO 3: Usuários e Permissões (O Paradoxo do ISO Admin)

### Status: ✅ VALIDADO

*(Detalhes do Fluxo 3 mantidos conformer versões anteriores...)*

---

## 🔄 FLUXO 4: Estabelecimentos e Transações (Vida Real)

### Status: ✅ VALIDADO

### VISÃO GERAL DO FLUXO (Jornada do Dado)

```mermaid
graph TD
    classDef external fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef system fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef dash fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef all fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;

    subgraph MUNDO_FISICO ["1️⃣ Mundo Físico"]
        direction TB
        A[ISO/Consultor cadastra EC]:::external
        B[EC passa em KYC (Dock)]:::external
        C[Terminal Configurado (POS/TEF)]:::external
        D[EC Vende (Transaciona)]:::external
        
        A --> B --> C --> D
    end

    subgraph SISTEMA ["2️⃣ Ingestão e Processamento"]
        direction TB
        E[Dock API]:::system
        F[Sync Job (Portal)]:::system
        G[Banco de Dados]:::system
        click G "Tabela transactions (TODOS Status)"
        
        D --> E
        E --> F
        F --> G
    end

    subgraph VISUALIZACAO ["3️⃣ Consumo de Dados"]
        direction TB
        H[Dashboard (BI Financeiro)]:::dash
        click H "Filtra apenas: APPROVED"
        
        I[Página Vendas (BI Completo)]:::all
        click I "Mostra: APPROVED, DENIED, PENDING, ETC"
        
        J[Fechamento (Margens)]:::dash
        click J "Filtra apenas: APPROVED"
        
        G --> H
        G --> I
        G --> J
    end
```

### DETALHAMENTO TÉCNICO

#### 1️⃣ Cadastro e Ativação
- **Responsável**: ISO ou Consultor.
- **Processo**: Cadastro no Portal -> Envio para Dock (KYC) -> Ativação.
- **Vínculo**: O EC nasce vinculado ao `slug_customer` (ISO) que o cadastrou. Esse vínculo é imutável na origem (Dock).

#### 2️⃣ Transação (Critério de Sucesso)
- **Status Dock**: `AUTHORIZED`, `DENIED`, `PENDING`, etc.
- **Sincronização**: O job puxa **TUDO** para o banco.
- **Status Portal**: Mapeado internamente (ex: `AUTHORIZED` -> `APPROVED`).

#### 3️⃣ Diferenciação de BI (Dashboard x Vendas)
- **Página Vendas (`/transactions`)**:
  - **Propósito**: Auditoria e Conferência.
  - **Visibilidade**: Mostra **TODOS** os status (Negadas, Pendentes, Canceladas).
  - **Código**: `src/features/transactions/_components/transactions-list.tsx` (Possui badges para todos os status).
  
- **Dashboard (`/dashboard`) e Fechamento**:
  - **Propósito**: Visão Financeira e Comissionamento.
  - **Visibilidade**: Filtra estritamente transações **APROVADAS**.
  - **Regra**: Denied/Rejected não geram comissão, logo não poluem a visão financeira.

---

### ⚠️ PONTOS DE ATENÇÃO (Integridade)

1. **Alteração de Margem**: O sistema de repasse usa a margem vigente no momento da execução do job de consolidação (fim do mês). Alterações no meio do mês afetam o cálculo do mês todo retroativamente.

2. **Rateio de Margens (REGRA DE NEGÓCIO CORRETA)**:
   - Se houver **mais de 1 usuário** do mesmo perfil (ex: 2 Executivos) no mesmo ISO, a margem configurada será **dividida proporcionalmente** entre eles.
   - Ex: Se `margin_executivo` = 1% e há 2 Executivos no ISO Prisma, cada um recebe **0.5%**.

> [!CAUTION]
> **GAP DE IMPLEMENTAÇÃO**: O código atual em `repasse.ts` **NÃO** implementa esse rateio. Cada usuário recebe o % cheio, causando pagamento duplicado. Isso precisa ser corrigido.

---
