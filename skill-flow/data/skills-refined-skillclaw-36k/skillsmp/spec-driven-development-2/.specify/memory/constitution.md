# PromiseKits Constitution

## Core Principles

### I. Rails Conventions Over Configuration
Follow Rails conventions religiously. The framework's opinions are battle-tested and enable team velocity. Deviations must be exceptional and well-documented.

**Rules:**
- RESTful routing is the default; custom routes require justification
- Use Rails naming conventions: `User`, `UsersController`, `users_path`
- Leverage Rails generators for consistency
- Active Record associations over manual SQL joins
- Rails form helpers over raw HTML forms

### II. Test-First Development (NON-NEGOTIABLE)
Write tests before implementation. No code reaches production without test coverage.

**Rules:**
- Write failing test → Implement → Make test pass → Refactor
- Minimum 90% code coverage for models and controllers
- Every bug fix starts with a failing test that reproduces the issue
- Test files mirror implementation structure: `app/models/user.rb` → `test/models/user_test.rb`

**Testing Hierarchy:**
1. **Unit Tests** (models, helpers, services) - Fast, isolated
2. **Integration Tests** (controllers, requests) - API contracts, params, responses
3. **System Tests** (full user workflows) - Critical paths only, expensive to maintain

### III. Hotwire-First Interactivity
Embrace HTML-over-the-wire. JavaScript is a last resort.

**Rules:**
- Turbo Frames for partial page updates
- Turbo Streams for real-time updates
- Stimulus controllers for progressive enhancement only
- No client-side state management (React, Vue, etc.)
- JavaScript complexity triggers reevaluation: "Can Turbo do this?"

**When JavaScript is acceptable:**
- Rich text editing (use Trix)
- Complex visualizations (charts, graphs)
- Third-party widget integration
- Mobile-specific touch interactions

### IV. Simplicity and YAGNI (You Aren't Gonna Need It)
Build for today's requirements. Future-proofing leads to over-engineering.

**Rules:**
- No abstractions until third use case appears
- Avoid premature optimization
- Question every dependency: "Can Rails do this?"
- Prefer boring technology over newest trends
- Duplicate code temporarily is better than wrong abstraction

**Red Flags:**
- "This will make it easier when we eventually..."
- Creating infrastructure for hypothetical scale
- Abstract base classes with single implementation
- Service objects with single method
- Introducing patterns from other languages/frameworks

### V. Data Integrity and Database Design
The database is the source of truth. Protect it fiercely.

**Rules:**
- Foreign keys with `dependent:` strategy on associations
- Database constraints for critical invariants (NOT NULL, UNIQUE, CHECK)
- Indexes on foreign keys and frequently queried columns
- Validations in both model AND database
- Migrations are immutable once merged to main branch

**SQLite Considerations:**
- Excellent for development and low-traffic production
- No concurrent writes - consider PostgreSQL if multiple workers needed
- Max database size ~281 TB (not a practical concern)
- Plan migration path to PostgreSQL for high-traffic scenarios

### VI. Performance and N+1 Query Prevention
Fast by default. Performance issues block deployment.

**Rules:**
- `includes`/`eager_load` to prevent N+1 queries (Bullet gem in development)
- Database indexes on foreign keys and search columns
- Counter caches for `has_many` counts
- Fragment caching for expensive view partials
- Solid Cache for application caching (Redis-like performance, SQLite storage)

**Performance Budget:**
- Page load < 200ms (server-side rendering)
- Turbo Frame updates < 100ms
- Database queries < 50ms per request

### VII. Security Standards
Security is not optional. Follow Rails security best practices.

**Rules:**
- Strong parameters for all controller actions
- CSRF protection enabled (Rails default)
- Mass assignment protection via `permit` whitelist
- SQL injection prevention: parameterized queries only
- XSS prevention: escape user input (Rails does this by default)
- Authentication with `has_secure_password` or industry-standard gem
- Authorization checks in every controller action

**Sensitive Data:**
- Credentials in encrypted credentials file (`rails credentials:edit`)
- Environment variables for deployment-specific config
- Never commit secrets to git
- Use `SecureRandom` for tokens, not `rand`

## Rails 8 Modern Stack

### Solid Gems Utilization
Rails 8 includes Solid Cache, Solid Queue, and Solid Cable. Leverage these.

**Solid Cache:**
- Application caching without Redis
- Fragment caching, Russian Doll caching
- Low-value cache for computed results

**Solid Queue:**
- Background job processing (replaces Sidekiq/Resque)
- Asynchronous emails, batch operations, scheduled tasks
- Reliable, no external dependencies

**Solid Cable:**
- WebSocket connections for Turbo Streams
- Real-time updates without ActionCable complexity
- Use for live notifications, collaborative features

### Active Storage
**Rules:**
- Use Active Storage for file uploads
- Variants for image processing (thumbnails, crops)
- Purge unused attachments (storage costs)
- Validate file types and sizes in model
- Use conditional variants: generate on-demand, cache result

## Development Workflow

### Feature Development
1. **Create branch** from `main`
2. **Write failing test** for new behavior
3. **Implement** minimal code to pass test
4. **Refactor** while keeping tests green
5. **System test** for user-facing features
6. **Manual QA** in browser (check console for JS errors)
7. **Create PR** with description and test evidence

### Code Review Requirements
- All tests passing (`rails test` and `rails test:system`)
- No Rubocop violations (`rubocop`)
- No N+1 queries (check Bullet gem logs)
- Performance budget met (check logs)
- Security review for user input, authentication, authorization

### Quality Gates
**Pre-Commit:**
- Tests must pass locally
- Rubocop must pass

**Pre-Merge:**
- PR approved by at least one reviewer
- CI pipeline green
- No unresolved comments

## Architectural Constraints

### Service Objects (Use Sparingly)
Service objects are for **complex business logic only**, not simple CRUD.

**When to create service object:**
- Logic spans multiple models
- Complex transaction coordination
- External API integration
- Multi-step wizard/workflow

**When NOT to create service object:**
- Simple CRUD operations (belongs in controller)
- Single model updates (belongs in model)
- "Clean architecture" dogma (Rails is not Java)

### File Organization
```
app/
├── controllers/     # Thin controllers, 7 RESTful actions
├── models/          # Business logic, validations, scopes
├── views/           # ERB templates, Turbo Frames/Streams
├── helpers/         # View-specific formatting logic
├── jobs/            # Background processing (Solid Queue)
├── mailers/         # Email sending
├── channels/        # WebSocket (Solid Cable)
├── javascript/      # Stimulus controllers only
└── assets/          # CSS, images (via Propshaft)

lib/                 # Reusable libraries, non-Rails code
test/                # Mirrors app/ structure
```

### Controller Patterns
```ruby
class ArticlesController < ApplicationController
  before_action :authenticate_user!, except: [:index, :show]
  before_action :set_article, only: [:show, :edit, :update, :destroy]
  before_action :authorize_article, only: [:edit, :update, :destroy]

  # Standard 7 RESTful actions
  def index; end
  def show; end
  def new; end
  def create; end
  def edit; end
  def update; end
  def destroy; end

  private

  def set_article
    @article = Article.find(params[:id])
  end

  def authorize_article
    redirect_to root_path unless @article.user == current_user
  end

  def article_params
    params.require(:article).permit(:title, :body, :published)
  end
end
```

## Anti-Patterns to Avoid

### ❌ God Models
Models with 500+ lines, 30+ methods. Break into concerns or separate models.

### ❌ Anemic Models
All logic in controllers or service objects. Models should contain business logic.

### ❌ Callback Hell
`before_save`, `after_create` chains 5+ levels deep. Use explicit service objects.

### ❌ Metaprogramming Abuse
`method_missing`, `define_method` for simple cases. Explicit code is better.

### ❌ Premature Extraction
Extracting gems/engines before code stabilizes. Wait for clear boundaries.

### ❌ Testing Implementation
Testing private methods directly. Test public interface only.

## Governance

### Constitution Authority
This constitution supersedes ad-hoc coding preferences. All technical decisions reference these principles.

### Amendment Process
1. Propose change with rationale in team meeting
2. Document trade-offs and impact
3. Update constitution with version bump
4. Communicate changes to team
5. Update existing code to comply (if breaking change)

### Compliance
- Code reviews verify adherence to constitution
- Violations require justification in PR description
- Repeated violations trigger constitution review
- Use `GUIDANCE.md` for implementation patterns not covered here

### Escalation
When principles conflict:
1. Security > Performance > Developer Experience
2. Simple > Clever
3. Boring > Exciting
4. Rails Way > Custom Solution

---

**Version**: 1.0.0  
**Ratified**: 2025-01-XX  
**Last Amended**: 2025-01-XX  
**Next Review**: 2025-06-XX