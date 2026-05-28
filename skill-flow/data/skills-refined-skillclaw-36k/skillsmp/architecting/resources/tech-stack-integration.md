# Tech Stack Integration Strategy

How to glue `frontend-dev-guidelines` and `backend-dev-guidelines` together for maximum efficiency.

## 1. Type Sharing (The "Secret Weapon")

regardless of architecture (Indie vs Enterprise), sharing types prevents execution errors.

### Strategy
1. **Backend as Source of Truth**: Define Zod schemas in the Backend.
2. **Export for Frontend**:
   - **Monorepo**: Frontend imports `type { User }` and `UserSchema` directly from `@workspace/backend`.
   - **Polyrepo**: Backend publishes a plain `@my-org/types` npm package (versions synchronized).

## 2. Data Fetching & State

### Frontend (TanStack Query)
- **Query Keys**: Must mirror the Backend API URL structure. 
  - URL: `/api/v1/users/123` -> Key: `['users', '123']`
- **Error Handling**: Middleware in `useQuery` configuration should globally handle the standardized error responses defined in `BaseController`.

### Backend (Response Format)
- Must adhere strictly to the `BaseController` format so the Frontend `SuspenseLoader` and Error Boundaries work predictably.
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional toast message"
}
```

## 3. Deployment Pipelines

### Indie Mode
- **Git Push -> Deploy All**.
- Zero downtime not guaranteed but acceptable.
- Database migrations run *before* app startup commands.

### Enterprise Mode
- **Blue/Green Deployment**.
- Database migrations must be **non-breaking** (expand and contract pattern).
- Frontend assets deployed to CDN *before* Backend API switch.
