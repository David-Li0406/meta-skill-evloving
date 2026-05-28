# Context Gathering Examples

## Example 1: HTTP Handler Change (Go)
Changed file: `api/handlers/order_handler.go` (adds new endpoint)

Discovery:
- Grep for imports → finds "internal/service/order"
- Grep for "OrderService" → definitions in service and mock
- Glob for tests → finds order_handler_test.go

Selected:
- api/handlers/order_handler.go (changed)
- internal/service/order/service.go (interface + impl)
- internal/service/order/types.go (request/response structs)
- api/handlers/order_handler_test.go (existing tests)
- config/router.go (route registration)

## Example 2: React Component Refactor
Changed: `components/Table/PaginatedTable.tsx`

Discovery:
- Imports useTable hook from `@/hooks/useTable`
- Renders <Row> component
- Used in dashboard/pages/UsersPage.tsx

Selected:
- components/Table/PaginatedTable.tsx
- hooks/useTable.ts
- components/Table/Row.tsx
- types/table.ts (shared types)
- dashboard/pages/UsersPage.tsx (usage context)
- components/Table/PaginatedTable.test.tsx

## Example 3: Bug Fix in Business Logic (Python)
Changed: `services/payment/processor.py`

Discovery:
- Uses PaymentProvider abstract base
- Two implementations: stripe/, paypal/
- Integration tests in tests/integration/

Selected:
- services/payment/processor.py
- services/payment/base.py (ABC)
- services/payment/stripe/provider.py (active impl)
- config/settings.py (which provider is enabled)
- tests/integration/test_payment_flow.py
