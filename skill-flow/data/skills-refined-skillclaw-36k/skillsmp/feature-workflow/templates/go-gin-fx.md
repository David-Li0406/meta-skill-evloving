---
name: feature-workflow
description: Use when implementing features after plan approval. Automates TDD with git worktree, parallel subagents, Uber fx DI, table-driven tests, mock generation, and code review loop until no issues.
---

## AUTO-ROUTING TO feature-dev (MANDATORY)

**When this skill is invoked with a feature description, ALWAYS route to feature-dev first:**

```
User: "Implement user settings"
     |
     v
+---------------------------------------------------+
|  STEP 1: Invoke feature-dev skill IMMEDIATELY     |
|                                                   |
|  /feature-dev:feature-dev "{feature description}" |
+---------------------------------------------------+
     |
     v
feature-dev orchestrates -> feature-workflow phases 1-7
```

### Routing Rule
| User Request | Action |
|--------------|--------|
| "Implement X" / "Add Y" / "Create Z" | -> `/feature-dev:feature-dev "{request}"` |
| Phase-specific work (e.g., "fix Phase 3") | -> Continue in current phase |

---

# Feature Implementation Workflow (Go + Gin + Uber fx)

> **Version**: 1.5.0 (Uber fx DI throughout)

Go + Gin 백엔드 프로젝트를 위한 7단계 Feature 구현 워크플로우.
**모든 의존성은 uber fx로 관리.**

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Go 1.21+ |
| Framework | Gin |
| **DI** | **uber fx (go.uber.org/fx)** |
| ORM | Bun (uptrace/bun) |
| Database | PostgreSQL |
| Cache/Queue | Redis (optional) |

---

## Uber fx DI Architecture

### Core Concepts

```go
// fx.Provide: 의존성 등록 (생성자 함수)
fx.Provide(NewUserRepository)

// fx.Invoke: 앱 시작 시 실행 (부수효과)
fx.Invoke(RegisterRoutes)

// fx.Options: 모듈 그룹화
fx.Options(
    fx.Provide(...),
    fx.Invoke(...),
)

// fx.Module: 네임스페이스 모듈 (Go 1.18+)
fx.Module("user",
    fx.Provide(NewUserRepository),
    fx.Provide(NewUserService),
)
```

### Dependency Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        fx.App                                │
├─────────────────────────────────────────────────────────────┤
│  cmd/server/main.go                                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ fx.New(                                                 ││
│  │     config.Module,      // Config 로드                  ││
│  │     database.Module,    // DB 연결                      ││
│  │     repository.Module,  // Repository 등록              ││
│  │     service.Module,     // Service 등록                 ││
│  │     handler.Module,     // Handler 등록                 ││
│  │     router.Module,      // Routes 등록 (fx.Invoke)      ││
│  │ )                                                       ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Dependency Resolution (자동)                               │
│                                                             │
│  Config → DB → Repository → Service → Handler → Router     │
└─────────────────────────────────────────────────────────────┘
```

---

## MANDATORY Rules

### 1. Worktree Isolation (MANDATORY)

```bash
# 1. develop에서 feature branch 생성
git checkout develop
git checkout -b feature/<feature-name>

# 2. develop으로 돌아가서 worktree 생성
git checkout develop
git worktree add .worktrees/<feature-name> feature/<feature-name>

# 3. worktree에서만 작업
cd .worktrees/<feature-name>
```

### 2. LSP-First (MANDATORY)

| Task | Use LSP | NOT This |
|------|---------|----------|
| Find definition | `goToDefinition` | grep/glob |
| File symbols | `documentSymbol` | read entire file |
| Search symbols | `workspaceSymbol` | grep |
| Find references | `findReferences` | grep |

### 3. Subagent Parallel Processing (MANDATORY)

```go
// GOOD: 병렬 실행
Task(Explore, "find handler files") || Task(Explore, "find service files")

// BAD: 순차 실행
Task(Explore, "find handler files")
... wait ...
Task(Explore, "find service files")
```

### 4. Code Review Loop (MANDATORY)

```
Implement → Build → Code Review → Issues? → Fix → Re-review (반복)
                                    ↓ No
                                 Complete
```

---

## Phase Enforcement (MANDATORY - 절대 건너뛰기 금지)

### STRICT PHASE ORDERING - NEVER SKIP PHASES

**Phases MUST be executed in exact order. Skipping is BLOCKED by system.**

```
┌─────────────────────────────────────────────────────────────────┐
│  ❌ BLOCKED: Phase 순서 무시                                      │
│     - Phase 1 완료 전 Phase 2 시작 → BLOCKED                      │
│     - Phase 2 완료 전 Phase 3 시작 → BLOCKED                      │
│     - Phase 6 (Code Review) 전 Phase 7 (Commit) → BLOCKED        │
│                                                                   │
│  ✅ ALLOWED: 순차 진행만 허용                                      │
│     Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → 7│
└─────────────────────────────────────────────────────────────────┘
```

### Phase Enforcement Commands

```bash
# At workflow start - ALWAYS initialize first
${CLAUDE_PLUGIN_ROOT}/plugins/feature-workflow/scripts/phase-enforcer.sh init "feature-name"

# Before starting each phase - WILL BLOCK IF NOT READY
${CLAUDE_PLUGIN_ROOT}/plugins/feature-workflow/scripts/phase-enforcer.sh start <phase-number>

# Mark phase as complete
${CLAUDE_PLUGIN_ROOT}/plugins/feature-workflow/scripts/phase-enforcer.sh complete <phase-number>

# Check current status anytime
${CLAUDE_PLUGIN_ROOT}/plugins/feature-workflow/scripts/phase-enforcer.sh status

# Check if phase can be started (returns yes/no)
${CLAUDE_PLUGIN_ROOT}/plugins/feature-workflow/scripts/phase-enforcer.sh can-start <phase-number>
```

### Enforcement Behavior Table
| Attempt | Current Phase | Result | Reason |
|---------|---------------|--------|--------|
| Start Phase 2 | Phase 1 done | ✅ OK | Sequential |
| Start Phase 3 | Phase 1 done | ❌ BLOCKED | Phase 2 skipped |
| Start Phase 5 | Phase 4 done | ✅ OK | Sequential |
| Start Phase 7 | Phase 5 done | ❌ BLOCKED | Phase 6 skipped |

### Self-Check Before Each Phase

```
⚠️ 각 Phase 시작 전 확인:
□ 이전 Phase가 완료되었는가?
□ Gate 조건이 충족되었는가?
□ phase-enforcer.sh start <N> 실행했는가?
```

---

## 7-Phase Checkpoint System

### Phase 1: Planning & Setup

```
□ Feature 요구사항 분석
□ LSP로 기존 fx 모듈 구조 파악
  - documentSymbol: 모듈 구조 확인
  - findReferences: 의존성 확인
□ 새 Feature의 fx 모듈 설계
□ Git worktree 생성
```

### Phase 2: Schema & Models

```
□ Bun ORM 모델 정의 (internal/model/)
□ 마이그레이션 파일 생성 (migrations/)
□ DTO 정의 (internal/dto/)
```

**Model 패턴:**
```go
// internal/model/<feature>.go
package model

import (
    "time"
    "github.com/uptrace/bun"
)

type Feature struct {
    bun.BaseModel `bun:"table:features"`

    ID        string    `bun:"id,pk,type:uuid,default:gen_random_uuid()"`
    Name      string    `bun:"name,notnull"`
    CreatedAt time.Time `bun:"created_at,notnull,default:current_timestamp"`
    UpdatedAt time.Time `bun:"updated_at,notnull,default:current_timestamp"`
}
```

**DTO 패턴:**
```go
// internal/dto/<feature>.go
package dto

type CreateFeatureRequest struct {
    Name string `json:"name" binding:"required"`
}

type FeatureResponse struct {
    ID        string `json:"id"`
    Name      string `json:"name"`
    CreatedAt string `json:"created_at"`
}
```

### Phase 3: TDD - Test First

```
□ Repository 테스트 (실패 확인 - Red)
□ Service 테스트 (실패 확인 - Red)
□ Handler 테스트 (실패 확인 - Red)
□ go test ./... 실행하여 실패 확인
```

**Test with fx 패턴:**
```go
// internal/handler/<feature>_test.go
package handler

import (
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/gin-gonic/gin"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
    "go.uber.org/fx"
    "go.uber.org/fx/fxtest"
)

func TestFeatureHandler_Create(t *testing.T) {
    gin.SetMode(gin.TestMode)

    var handler *FeatureHandler

    app := fxtest.New(t,
        fx.Provide(func() FeatureService {
            m := NewMockFeatureService(t)
            m.EXPECT().Create(mock.Anything, mock.Anything).
                Return(&model.Feature{ID: "test-id", Name: "Test"}, nil)
            return m
        }),
        fx.Provide(NewFeatureHandler),
        fx.Populate(&handler),
    )
    app.RequireStart()
    defer app.RequireStop()

    w := httptest.NewRecorder()
    c, _ := gin.CreateTestContext(w)
    c.Request = httptest.NewRequest("POST", "/", strings.NewReader(`{"name":"Test"}`))
    c.Request.Header.Set("Content-Type", "application/json")

    handler.Create(c)

    assert.Equal(t, http.StatusCreated, w.Code)
}
```

### Phase 4: Implementation (fx 모듈 구조)

```
□ Repository 구현 + fx.Provide 등록
□ Service 구현 + fx.Provide 등록
□ Handler 구현 + fx.Provide 등록
□ 테스트 통과 확인 (Green)
```

#### Repository Layer

```go
// internal/repository/<feature>.go
package repository

import (
    "context"

    "github.com/uptrace/bun"
    "go.uber.org/fx"

    "your-project/internal/model"
)

// Interface 정의
type FeatureRepository interface {
    Create(ctx context.Context, feature *model.Feature) error
    FindByID(ctx context.Context, id string) (*model.Feature, error)
    FindAll(ctx context.Context, limit, offset int) ([]*model.Feature, error)
    Update(ctx context.Context, feature *model.Feature) error
    Delete(ctx context.Context, id string) error
}

// Implementation
type featureRepository struct {
    db *bun.DB
}

// Constructor (fx가 호출)
func NewFeatureRepository(db *bun.DB) FeatureRepository {
    return &featureRepository{db: db}
}

func (r *featureRepository) Create(ctx context.Context, feature *model.Feature) error {
    _, err := r.db.NewInsert().Model(feature).Exec(ctx)
    return err
}

func (r *featureRepository) FindByID(ctx context.Context, id string) (*model.Feature, error) {
    feature := new(model.Feature)
    err := r.db.NewSelect().Model(feature).Where("id = ?", id).Scan(ctx)
    if err != nil {
        return nil, err
    }
    return feature, nil
}
```

```go
// internal/repository/module.go
package repository

import "go.uber.org/fx"

var Module = fx.Options(
    fx.Provide(NewFeatureRepository),
    // 다른 repository 추가
)
```

#### Service Layer

```go
// internal/service/<feature>.go
package service

import (
    "context"

    "go.uber.org/fx"

    "your-project/internal/dto"
    "your-project/internal/model"
    "your-project/internal/repository"
)

// Interface 정의
type FeatureService interface {
    Create(ctx context.Context, req *dto.CreateFeatureRequest) (*model.Feature, error)
    GetByID(ctx context.Context, id string) (*model.Feature, error)
    List(ctx context.Context, limit, offset int) ([]*model.Feature, error)
    Update(ctx context.Context, id string, req *dto.UpdateFeatureRequest) (*model.Feature, error)
    Delete(ctx context.Context, id string) error
}

// Implementation
type featureService struct {
    repo repository.FeatureRepository
}

// Constructor (fx가 호출) - interface를 받음
func NewFeatureService(repo repository.FeatureRepository) FeatureService {
    return &featureService{repo: repo}
}

func (s *featureService) Create(ctx context.Context, req *dto.CreateFeatureRequest) (*model.Feature, error) {
    feature := &model.Feature{
        Name: req.Name,
    }
    if err := s.repo.Create(ctx, feature); err != nil {
        return nil, err
    }
    return feature, nil
}
```

```go
// internal/service/module.go
package service

import "go.uber.org/fx"

var Module = fx.Options(
    fx.Provide(NewFeatureService),
    // 다른 service 추가
)
```

#### Handler Layer

```go
// internal/handler/<feature>.go
package handler

import (
    "net/http"
    "strconv"
    "time"

    "github.com/gin-gonic/gin"
    "go.uber.org/fx"

    "your-project/internal/dto"
    "your-project/internal/service"
)

type FeatureHandler struct {
    service service.FeatureService
}

// Constructor (fx가 호출) - interface를 받음
func NewFeatureHandler(service service.FeatureService) *FeatureHandler {
    return &FeatureHandler{service: service}
}

// Create godoc
// @Summary      Create a new feature
// @Tags         features
// @Accept       json
// @Produce      json
// @Param        request body dto.CreateFeatureRequest true "Create request"
// @Success      201 {object} dto.FeatureResponse
// @Failure      400 {object} dto.ErrorResponse
// @Router       /api/v1/features [post]
// @Security     BearerAuth
func (h *FeatureHandler) Create(c *gin.Context) {
    var req dto.CreateFeatureRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    feature, err := h.service.Create(c.Request.Context(), &req)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusCreated, dto.FeatureResponse{
        ID:        feature.ID,
        Name:      feature.Name,
        CreatedAt: feature.CreatedAt.Format(time.RFC3339),
    })
}

// List godoc
// @Summary      List all features
// @Tags         features
// @Produce      json
// @Param        limit query int false "Limit" default(10)
// @Param        offset query int false "Offset" default(0)
// @Success      200 {array} dto.FeatureResponse
// @Router       /api/v1/features [get]
// @Security     BearerAuth
func (h *FeatureHandler) List(c *gin.Context) {
    limit := c.DefaultQuery("limit", "10")
    offset := c.DefaultQuery("offset", "0")

    limitInt, _ := strconv.Atoi(limit)
    offsetInt, _ := strconv.Atoi(offset)

    features, err := h.service.List(c.Request.Context(), limitInt, offsetInt)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    response := make([]dto.FeatureResponse, len(features))
    for i, f := range features {
        response[i] = dto.FeatureResponse{
            ID:        f.ID,
            Name:      f.Name,
            CreatedAt: f.CreatedAt.Format(time.RFC3339),
        }
    }

    c.JSON(http.StatusOK, response)
}
```

```go
// internal/handler/module.go
package handler

import "go.uber.org/fx"

var Module = fx.Options(
    fx.Provide(NewFeatureHandler),
    // 다른 handler 추가
)
```

### Phase 5: Integration (fx.Invoke로 라우트 등록)

```
□ Router에서 fx.Invoke로 핸들러 라우트 등록
□ Swagger 문서 업데이트 (swag init)
□ Middleware 연동
□ Local Testing
```

#### Router with fx.Invoke

```go
// internal/router/router.go
package router

import (
    "github.com/gin-gonic/gin"
    "go.uber.org/fx"

    "your-project/internal/handler"
    "your-project/internal/middleware"
)

// RouterParams: fx가 주입할 의존성들
type RouterParams struct {
    fx.In

    Engine         *gin.Engine
    AuthMiddleware *middleware.AuthMiddleware

    // Handlers
    FeatureHandler *handler.FeatureHandler
    // 다른 handler 추가...
}

// RegisterRoutes: fx.Invoke로 호출됨
func RegisterRoutes(p RouterParams) {
    // Protected routes
    api := p.Engine.Group("/api/v1")
    api.Use(p.AuthMiddleware.Handler())
    {
        // Feature routes
        features := api.Group("/features")
        {
            features.POST("", p.FeatureHandler.Create)
            features.GET("", p.FeatureHandler.List)
            features.GET("/:id", p.FeatureHandler.GetByID)
            features.PUT("/:id", p.FeatureHandler.Update)
            features.DELETE("/:id", p.FeatureHandler.Delete)
        }
    }
}
```

```go
// internal/router/module.go
package router

import "go.uber.org/fx"

var Module = fx.Options(
    fx.Invoke(RegisterRoutes),
)
```

#### Main Entry Point

```go
// cmd/server/main.go
package main

import (
    "context"
    "net/http"

    "github.com/gin-gonic/gin"
    "go.uber.org/fx"

    "your-project/internal/config"
    "your-project/internal/database"
    "your-project/internal/handler"
    "your-project/internal/middleware"
    "your-project/internal/repository"
    "your-project/internal/router"
    "your-project/internal/service"
)

func main() {
    fx.New(
        // Infrastructure
        config.Module,
        database.Module,

        // Gin Engine
        fx.Provide(NewGinEngine),

        // Middleware
        middleware.Module,

        // Application layers
        repository.Module,
        service.Module,
        handler.Module,

        // Routes (fx.Invoke)
        router.Module,

        // HTTP Server lifecycle
        fx.Invoke(StartHTTPServer),
    ).Run()
}

func NewGinEngine() *gin.Engine {
    engine := gin.Default()
    return engine
}

func StartHTTPServer(lc fx.Lifecycle, engine *gin.Engine, cfg *config.Config) {
    server := &http.Server{
        Addr:    ":" + cfg.Port,
        Handler: engine,
    }

    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error {
            go server.ListenAndServe()
            return nil
        },
        OnStop: func(ctx context.Context) error {
            return server.Shutdown(ctx)
        },
    })
}
```

### Phase 6: Build & Verify

```bash
go build ./...           # Build 성공
go vet ./...             # 정적 분석 통과
golangci-lint run        # 린트 통과
go test ./...            # 테스트 통과
go test -cover ./...     # 커버리지 >80%
```

### Phase 7: Test & Review (Loop)

```
□ Integration 테스트 통과
□ Code Review Loop (이슈 없을 때까지 반복)
□ Commit & Push
```

---

## fx Advanced Patterns

### fx.In / fx.Out (여러 의존성)

```go
// 여러 의존성을 한 번에 주입받기
type ServiceParams struct {
    fx.In

    UserRepo    repository.UserRepository
    FeatureRepo repository.FeatureRepository
    Cache       *redis.Client
    Logger      *zap.Logger
}

func NewComplexService(p ServiceParams) *ComplexService {
    return &ComplexService{
        userRepo:    p.UserRepo,
        featureRepo: p.FeatureRepo,
        cache:       p.Cache,
        logger:      p.Logger,
    }
}
```

### Named Provides

```go
// 같은 타입의 여러 인스턴스 제공
fx.Provide(
    fx.Annotate(
        NewPrimaryDB,
        fx.ResultTags(`name:"primary"`),
    ),
    fx.Annotate(
        NewReplicaDB,
        fx.ResultTags(`name:"replica"`),
    ),
)

// 사용
type Params struct {
    fx.In

    PrimaryDB *bun.DB `name:"primary"`
    ReplicaDB *bun.DB `name:"replica"`
}
```

### Group (여러 핸들러 수집)

```go
// 핸들러를 그룹으로 등록
fx.Provide(
    fx.Annotate(NewUserHandler, fx.ResultTags(`group:"handlers"`)),
    fx.Annotate(NewFeatureHandler, fx.ResultTags(`group:"handlers"`)),
)

// 그룹으로 수집
type RouterParams struct {
    fx.In
    Handlers []Handler `group:"handlers"`
}

func RegisterRoutes(p RouterParams) {
    for _, h := range p.Handlers {
        h.RegisterRoutes(engine)
    }
}
```

### Optional Dependencies

```go
type ServiceParams struct {
    fx.In

    Repo   repository.FeatureRepository
    Cache  *redis.Client `optional:"true"` // 없어도 됨
}
```

---

## Project Structure (fx 기반)

```
your-project/
├── cmd/server/
│   └── main.go              # fx.New() 진입점
├── internal/
│   ├── config/
│   │   └── module.go        # fx.Provide(NewConfig)
│   ├── database/
│   │   └── module.go        # fx.Provide(NewBunDB)
│   ├── dto/
│   │   └── <feature>.go     # Request/Response DTOs
│   ├── handler/
│   │   ├── module.go        # fx.Provide(NewXHandler, ...)
│   │   └── <feature>.go
│   ├── middleware/
│   │   └── module.go        # fx.Provide(NewAuthMiddleware, ...)
│   ├── model/
│   │   └── <feature>.go     # Bun ORM 모델
│   ├── repository/
│   │   ├── module.go        # fx.Provide(NewXRepository, ...)
│   │   └── <feature>.go
│   ├── router/
│   │   └── module.go        # fx.Invoke(RegisterRoutes)
│   └── service/
│       ├── module.go        # fx.Provide(NewXService, ...)
│       └── <feature>.go
├── migrations/
├── docs/                    # Swagger
└── go.mod
```

---

## Gate Verification Commands

```bash
# Gate 1: Worktree
git worktree list | grep "feature-name"

# Gate 2: Tests Written
test -f "internal/handler/{feature}_test.go"

# Gate 3: Implementation
go build ./...

# Gate 4: Build & Test
go test ./... -short

# Gate 5: Swagger
make swagger 2>&1 | grep -v "error"

# Gate 6: Code Review
# Run code-reviewer agent

# Gate 7: Commit
git status --porcelain | wc -l
```

---

## Red Flags - STOP

- Using grep/glob when LSP can do it (LSP FIRST!)
- Implementing before writing tests
- Sequential execution for independent files
- Committing without code review passing
- Missing mock implementations for new interface methods
- Missing fx.Provide registration
- Missing router registration
- Swagger "cannot find type definition" errors
- N+1 query patterns (loop 내 DB 호출)
- Proceeding to next phase without gate verification
- Skipping code review re-run after fixes
- Not updating TodoWrite status between phases
