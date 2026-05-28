---
name: musubix-domain-inference
description: Guide for automatic domain detection and component inference. Use this when asked to identify the domain of a project and get recommended components for that domain.
license: MIT
---

# MUSUBIX Domain Inference Skill

This skill guides you through automatic domain detection and component recommendations.

## Overview

MUSUBIX supports **62 domains** with **224 predefined components**. The domain inference system automatically:

1. Detects project domain from requirements/descriptions
2. Recommends optimal components for that domain
3. Suggests architecture patterns

## Supported Domains (62)

### Business (8)
| Domain | Description | Key Components |
|--------|-------------|----------------|
| ecommerce | EC・通販 | CartService, ProductCatalog, OrderProcessor |
| finance | 金融 | AccountService, TransactionManager, LedgerService |
| crm | 顧客管理 | CustomerService, LeadManager, OpportunityTracker |
| hr | 人事 | EmployeeService, PayrollCalculator, AttendanceTracker |
| marketing | マーケティング | CampaignManager, AudienceSegmenter, AnalyticsService |
| inventory | 在庫管理 | StockManager, ReorderService, WarehouseController |
| payment | 決済 | PaymentGateway, RefundProcessor, InvoiceGenerator |
| subscription | サブスク | PlanManager, BillingService, RenewalProcessor |

### Healthcare (3)
| Domain | Description | Key Components |
|--------|-------------|----------------|
| healthcare | ヘルスケア | PatientService, DiagnosticService, AppointmentManager |
| pharmacy | 薬局 | PrescriptionManager, MedicineInventory, DosageCalculator |
| veterinary | 動物病院 | PetService, VetScheduleService, VaccinationTracker |

### Service (20+)
| Domain | Description | Key Components |
|--------|-------------|----------------|
| booking | 予約 | ReservationService, SlotManager, AvailabilityChecker |
| hotel | ホテル | RoomService, CheckInManager, HousekeepingScheduler |
| restaurant | 飲食店 | MenuManager, TableService, KitchenOrderSystem |
| gym | フィットネス | MembershipService, ClassScheduler, TrainerAssignment |
| delivery | 配送 | DeliveryService, RouteOptimizer, TrackingManager |
| parking | 駐車場 | SpaceManager, EntryExitController, FeeCalculator |

### Technology (8)
| Domain | Description | Key Components |
|--------|-------------|----------------|
| iot | IoT | DeviceManager, TelemetryProcessor, AlertService |
| security | セキュリティ | AuthService, PermissionManager, AuditLogger |
| ai | AI | ModelService, InferenceEngine, TrainingPipeline |
| analytics | 分析 | ReportGenerator, MetricsCollector, DashboardService |

## Domain Detection

### Automatic Detection

MUSUBIX analyzes text for domain keywords:

```typescript
import { domainDetector } from '@nahisaho/musubix-core';

const result = domainDetector.detect(`
  ペットの予約管理システムを作りたい。
  獣医師のスケジュール管理と、ワクチン接種記録も必要。
`);

// Result:
// {
//   primaryDomain: { id: 'veterinary', name: 'Veterinary', nameJa: '動物病院' },
//   confidence: 0.92,
//   matchedKeywords: ['ペット', '獣医', 'ワクチン', '予約'],
//   suggestedComponents: ['PetService', 'ReservationService', 'VetScheduleService']
// }
```

### CLI Usage

```bash
# Analyze requirements file
npx musubix design patterns --detect-domain storage/specs/REQ-001.md

# Get component recommendations
npx musubix design generate storage/specs/REQ-001.md --infer-components
```

## Component Inference

### Domain-Specific Components

Each domain has predefined components with:
- **Type**: Service, Repository, Controller, Factory, etc.
- **Layer**: Presentation, Application, Domain, Infrastructure
- **Dependencies**: Required collaborators
- **Patterns**: Recommended design patterns
- **Methods**: Domain-specific operations

### Example: Veterinary Domain

```typescript
const veterinaryComponents = [
  {
    name: 'PetService',
    type: 'service',
    layer: 'application',
    description: 'ペット管理のビジネスロジック',
    dependencies: ['PetRepository', 'PetHistoryRepository'],
    patterns: ['Service'],
    methods: [
      { name: 'register', returnType: 'Promise<Pet>' },
      { name: 'update', returnType: 'Promise<Pet>' },
      { name: 'getByOwner', returnType: 'Promise<Pet[]>' },
      { name: 'getHistory', returnType: 'Promise<PetHistory[]>' },
    ]
  },
  {
    name: 'ReservationService',
    type: 'service',
    layer: 'application',
    methods: [
      { name: 'create', returnType: 'Promise<Reservation>' },
      { name: 'confirm', returnType: 'Promise<Reservation>' },
      { name: 'cancel', returnType: 'Promise<Reservation>' },
      { name: 'getAvailableSlots', returnType: 'Promise<TimeSlot[]>' },
    ]
  },
  // ...more components
];
```

## Architecture Recommendations

Based on domain, MUSUBIX recommends:

| Domain Category | Architecture Style | Scaling Strategy |
|-----------------|-------------------|------------------|
| Business | Layered + DDD | Vertical with caching |
| Technology | Microservices | Horizontal scaling |
| Healthcare | Layered + Audit | Vertical with compliance |
| Service | Layered | Vertical with caching |

## Multi-Domain Projects

For projects spanning multiple domains:

```typescript
const result = domainDetector.detect(`
  ECサイトで商品を販売し、配送追跡も行いたい。
  在庫管理とサブスクリプション機能も必要。
`);

// Result:
// {
//   primaryDomain: { id: 'ecommerce' },
//   secondaryDomains: [
//     { id: 'delivery' },
//     { id: 'inventory' },
//     { id: 'subscription' }
//   ]
// }
```

## Using in Design Documents

```markdown
# DES-SHOP-001: ECサイト設計

## ドメイン分析
- **主ドメイン**: ecommerce
- **副ドメイン**: inventory, payment, delivery

## 推奨コンポーネント

### ecommerce ドメイン
| コンポーネント | 種別 | 責務 |
|---------------|------|------|
| CartService | Service | カート管理 |
| ProductCatalog | Service | 商品カタログ |
| OrderProcessor | Service | 注文処理 |

### inventory ドメイン
| コンポーネント | 種別 | 責務 |
|---------------|------|------|
| StockManager | Service | 在庫管理 |
| ReorderService | Service | 発注管理 |
```

## Related Skills

- `musubix-c4-design` - Create architecture with inferred components
- `musubix-code-generation` - Generate code for components
- `musubix-sdd-workflow` - Full workflow with domain awareness
