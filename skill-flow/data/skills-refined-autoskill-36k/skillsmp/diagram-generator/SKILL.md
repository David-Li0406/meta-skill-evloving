---
name: diagram-generator
description: Geração de diagramas técnicos usando Mermaid e PlantUML incluindo ERD (Entity Relationship), fluxogramas, diagramas de sequência, arquitetura de sistemas, e class diagrams. Usar para documentar estrutura de banco de dados, fluxos de processos, arquitetura de aplicações, e comunicação entre sistemas.
---

# Diagram Generator

Skill para criação de diagramas técnicos em Mermaid e PlantUML.

## Entity Relationship Diagram (ERD)

### Mermaid ERD

```mermaid
erDiagram
    CLIENTS ||--o{ CONTRACTS : has
    CLIENTS {
        int id PK
        string name
        string email UK
        string document UK
        string phone
        datetime created_at
    }
    
    CONTRACTS ||--o{ PAYMENTS : has
    CONTRACTS ||--o{ CONTRACT_ITEMS : contains
    CONTRACTS {
        int id PK
        int client_id FK
        date event_date
        decimal value
        string status
        text notes
        datetime created_at
    }
    
    PAYMENTS {
        int id PK
        int contract_id FK
        decimal amount
        date due_date
        date paid_at
        string status
        string payment_method
    }
    
    CONTRACT_ITEMS {
        int id PK
        int contract_id FK
        string description
        int quantity
        decimal unit_price
        decimal total
    }
    
    ARTISTS ||--o{ CONTRACT_ITEMS : performs
    ARTISTS {
        int id PK
        string name
        string genre
        decimal cache_value
    }
```

### PlantUML ERD

```plantuml
@startuml
!define Table(name) entity name << (T,#FFAAAA) >>
!define PK(x) <b><u>x</u></b>
!define FK(x) <i>x</i>

Table(clients) {
  PK(id) : INT
  name : VARCHAR(255)
  email : VARCHAR(255)
  document : VARCHAR(20)
  created_at : TIMESTAMP
}

Table(contracts) {
  PK(id) : INT
  FK(client_id) : INT
  event_date : DATE
  value : DECIMAL(10,2)
  status : VARCHAR(20)
}

Table(payments) {
  PK(id) : INT
  FK(contract_id) : INT
  amount : DECIMAL(10,2)
  due_date : DATE
  status : VARCHAR(20)
}

clients ||--o{ contracts
contracts ||--o{ payments
@enduml
```

## Fluxogramas

### Processo de Contrato

```mermaid
flowchart TD
    A[Início] --> B{Cliente existe?}
    B -->|Não| C[Cadastrar Cliente]
    C --> D[Criar Contrato]
    B -->|Sim| D
    D --> E[Definir Itens]
    E --> F[Calcular Valor Total]
    F --> G{Aprovação necessária?}
    G -->|Sim| H[Enviar para Aprovação]
    H --> I{Aprovado?}
    I -->|Não| J[Revisar Contrato]
    J --> E
    I -->|Sim| K[Gerar Pagamentos]
    G -->|Não| K
    K --> L[Enviar para Cliente]
    L --> M{Cliente assinou?}
    M -->|Não| N[Aguardar]
    N --> M
    M -->|Sim| O[Ativar Contrato]
    O --> P[Fim]
```

### Fluxo com Subgrafos

```mermaid
flowchart TB
    subgraph Frontend
        A[Usuário] --> B[Interface Web]
    end
    
    subgraph API
        B --> C[API Gateway]
        C --> D[Autenticação]
        D --> E[Controller]
        E --> F[Service]
    end
    
    subgraph Data
        F --> G[(MySQL)]
        F --> H[(Redis Cache)]
    end
    
    subgraph External
        F --> I[Payment Gateway]
        F --> J[Email Service]
    end
```

## Diagrama de Sequência

### Fluxo de Pagamento

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuário
    participant F as Frontend
    participant A as API
    participant S as PaymentService
    participant G as Gateway
    participant D as Database
    
    U->>F: Solicita pagamento
    F->>A: POST /payments
    A->>A: Valida request
    A->>S: processPayment(data)
    S->>D: Busca contrato
    D-->>S: Contrato
    S->>G: Processa cobrança
    
    alt Pagamento aprovado
        G-->>S: Sucesso
        S->>D: Atualiza status
        S-->>A: Payment created
        A-->>F: 201 Created
        F-->>U: Confirmação
    else Pagamento recusado
        G-->>S: Erro
        S-->>A: PaymentFailedException
        A-->>F: 422 Error
        F-->>U: Mensagem de erro
    end
```

## Diagrama de Classes

```mermaid
classDiagram
    class Contract {
        +int id
        +int client_id
        +date event_date
        +decimal value
        +string status
        +create(data)
        +update(data)
        +cancel(reason)
        +calculateTotal()
    }
    
    class Client {
        +int id
        +string name
        +string email
        +getContracts()
        +getTotalValue()
    }
    
    class Payment {
        +int id
        +int contract_id
        +decimal amount
        +string status
        +process()
        +refund()
    }
    
    class ContractService {
        -ContractRepository repository
        -PaymentService payments
        +create(dto)
        +cancel(contract, reason)
    }
    
    class ContractRepository {
        <<interface>>
        +find(id)
        +create(data)
        +update(contract, data)
    }
    
    Client "1" --> "*" Contract : has
    Contract "1" --> "*" Payment : has
    ContractService --> ContractRepository : uses
    ContractService --> Contract : manages
```

## Diagrama de Arquitetura

```mermaid
graph TB
    subgraph Client Layer
        WEB[Web App<br/>Vue.js]
        MOBILE[Mobile App<br/>React Native]
    end
    
    subgraph Gateway
        LB[Load Balancer<br/>Nginx]
    end
    
    subgraph Application Layer
        API1[API Server 1<br/>Laravel]
        API2[API Server 2<br/>Laravel]
        WORKER[Queue Worker<br/>Laravel]
    end
    
    subgraph Data Layer
        DB[(MySQL<br/>Primary)]
        DB_R[(MySQL<br/>Replica)]
        REDIS[(Redis<br/>Cache/Queue)]
    end
    
    subgraph External Services
        MAIL[SendGrid]
        PAY[Payment Gateway]
        STORAGE[S3 Storage]
    end
    
    WEB --> LB
    MOBILE --> LB
    LB --> API1
    LB --> API2
    API1 --> DB
    API2 --> DB
    API1 --> REDIS
    API2 --> REDIS
    DB --> DB_R
    WORKER --> REDIS
    WORKER --> MAIL
    API1 --> PAY
    API1 --> STORAGE
```

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft: Criar
    Draft --> Pending: Submeter
    Pending --> Active: Aprovar
    Pending --> Draft: Rejeitar
    Active --> Completed: Finalizar
    Active --> Cancelled: Cancelar
    Completed --> [*]
    Cancelled --> [*]
    
    state Active {
        [*] --> InProgress
        InProgress --> AwaitingPayment: Evento realizado
        AwaitingPayment --> Paid: Pagamento recebido
        Paid --> [*]
    }
```

## Gantt Chart

```mermaid
gantt
    title Cronograma de Migração
    dateFormat YYYY-MM-DD
    
    section Preparação
    Análise de código       :a1, 2024-01-01, 2w
    Documentação            :a2, after a1, 1w
    
    section Desenvolvimento
    Refatoração módulo A    :b1, after a2, 3w
    Refatoração módulo B    :b2, after b1, 3w
    Integração Laravel      :b3, after b2, 2w
    
    section Testes
    Testes unitários        :c1, after b3, 2w
    Testes integração       :c2, after c1, 1w
    UAT                     :c3, after c2, 1w
    
    section Deploy
    Deploy staging          :d1, after c3, 3d
    Deploy produção         :d2, after d1, 2d
```

## Dicas de Uso

```markdown
## Mermaid
- Suportado nativamente no GitHub, GitLab, Notion
- Usar para diagramas simples e médios
- Sintaxe mais limpa

## PlantUML
- Mais poderoso para diagramas complexos
- Requer servidor ou extensão
- Melhor para ERDs detalhados e UML completo

## Exportação
- Mermaid: mermaid.live
- PlantUML: plantuml.com/plantuml
```
