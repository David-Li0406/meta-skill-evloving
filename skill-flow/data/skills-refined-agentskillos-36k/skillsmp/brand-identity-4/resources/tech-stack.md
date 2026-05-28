# Preferred Tech Stack & Implementation Rules

When generating code or UI components for SpecsVibeCode, you **MUST** strictly adhere to the following technology choices and patterns.

## Core Stack

### Backend
* **Framework:** Ruby on Rails 8.x (Ruby 3.3.6)
* **Database:** PostgreSQL 14+ (with separate databases for cache/queue/cable via Solid stack)
* **Authentication:** Supabase Auth (OAuth via GitHub, Google)
* **Job Queue:** Solid Queue (background jobs)
* **Caching:** Solid Cache
* **WebSockets:** Solid Cable (via Action Cable)

### Frontend
* **JavaScript:** Importmap (native ES modules, no bundler)
* **Framework:** Hotwire (Turbo + Stimulus)
* **Styling Engine:** Tailwind CSS 3.x (Mandatory. Do not use plain CSS or styled-components.)
* **Icons:** Use SVG icons inline via `icons_helper.rb` or Heroicons
* **Forms:** Rails form helpers with Turbo Frames

### AI Integration
* **Provider:** OpenRouter API
* **Models:** Claude, GPT-4, and other models via unified interface

## Implementation Guidelines

### 1. Rails Conventions

#### Controllers
* Inherit from `ApplicationController`
* Use `before_action :authenticate_user!` (default behavior)
* Public pages must explicitly `skip_before_action :authenticate_user!`
* Prefer Turbo Stream responses for dynamic updates
* Use strong parameters for mass assignment protection

#### Models
* Use ActiveRecord validations
* Extract business logic to Service Objects in `app/services/`
* Background jobs go in `app/jobs/`
* Use concerns in `app/models/concerns/` for shared behavior

#### Views
* Use ERB templates (`.html.erb`)
* Partial names must start with underscore: `_partial.html.erb`
* Components live in `app/views/components/`
* Use Turbo Frames for partial page updates
* Use Turbo Streams for live updates

#### Routing
* RESTful routes preferred
* Namespace API endpoints under `/api/`
* Auth routes under `/auth/`
* Use shallow nesting (max 1 level)

### 2. Tailwind Usage

* **Always use utility classes directly in ERB templates**
* Refer to `design-tokens.json` for color values
* Use Tailwind's default spacing scale (based on 4px)
* **Dark Theme:** Primary theme is dark; always use dark background colors from design tokens
* **Color Contrast:** Ensure text has minimum 7:1 contrast ratio (white on black backgrounds)
* **Responsive Design:** Mobile-first approach using `sm:`, `md:`, `lg:`, `xl:` breakpoints

#### Component Patterns
```erb
<!-- Primary Button (Red Accent) -->
<button class="bg-primary hover:bg-primary-hover text-white font-medium py-3 px-6 rounded-xl transition-all duration-200 shadow-md hover:shadow-lg">
  Primary Action
</button>

<!-- Secondary Button (Dark) -->
<button class="bg-secondary hover:bg-secondary-hover text-white font-medium py-3 px-6 rounded-xl transition-all duration-200">
  Secondary Action
</button>

<!-- Card Container (Dark) -->
<div class="bg-background-card border border-border-subtle rounded-2xl shadow-md p-6">
  <!-- Content -->
</div>

<!-- Widget/Panel (Material Design Style) -->
<div class="bg-background-secondary rounded-2xl p-6 shadow-lg">
  <!-- Content -->
</div>

<!-- Form Input (Dark) -->
<input type="text" 
       class="w-full px-4 py-3 bg-input border border-input-border rounded-xl text-foreground placeholder:text-foreground-muted focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all">

<!-- Text Styles -->
<h1 class="text-foreground text-3xl font-bold">Main Heading</h1>
<p class="text-foreground-secondary text-base">Secondary text</p>
<span class="text-foreground-tertiary text-sm">Muted text</span>
```

### 3. Stimulus Controllers

* Place in `app/javascript/controllers/`
* Use data attributes for controller configuration
* Keep controllers small and focused
* Name controllers with `_controller.js` suffix
* Use Stimulus values for configuration
* Use Stimulus targets for DOM references

```javascript
// Example: app/javascript/controllers/dropdown_controller.js
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["menu"]
  static values = { open: Boolean }

  toggle() {
    this.openValue = !this.openValue
  }

  openValueChanged() {
    this.menuTarget.classList.toggle("hidden", !this.openValue)
  }
}
```

### 4. Hotwire (Turbo) Usage

* **Turbo Drive:** Enabled by default for all navigation
* **Turbo Frames:** Use for independent page sections that update separately
* **Turbo Streams:** Use for live updates (via WebSockets or form responses)

```erb
<!-- Turbo Frame Example -->
<%= turbo_frame_tag "project_#{@project.id}" do %>
  <%= render @project %>
<% end %>

<!-- Turbo Stream Response -->
<%= turbo_stream.replace "project_#{@project.id}", partial: "projects/project", locals: { project: @project } %>
```

### 5. Service Objects Pattern

* Place in `app/services/` with namespace folders
* One public method: `#call`
* Return a result object or raise errors
* Use for complex business logic

```ruby
# app/services/generation/create_document.rb
module Generation
  class CreateDocument
    def initialize(project:, user:)
      @project = project
      @user = user
    end

    def call
      # Business logic here
    end

    private

    attr_reader :project, :user
  end
end
```

### 6. Background Jobs

* Use Solid Queue (already configured)
* Place jobs in `app/jobs/` with namespace folders
* Inherit from `ApplicationJob`
* Use `perform_later` for async execution

```ruby
# app/jobs/ai/generate_specification_job.rb
module AI
  class GenerateSpecificationJob < ApplicationJob
    queue_as :default

    def perform(document_id)
      # Job logic here
    end
  end
end
```

### 7. Authentication Patterns

* Use `current_user` helper (available in controllers and views)
* Session managed via `Auth::SessionManager`
* JWT tokens stored in encrypted cookies
* Do NOT implement custom auth; use existing Supabase integration

### 8. Database Migrations

* Use descriptive names with timestamps
* Always include rollback (`down` method)
* For multi-DB migrations:
  - `db/migrate/` - main database
  - `db/queue_migrate/` - Solid Queue
  - `db/cache_migrate/` - Solid Cache
  - `db/cable_migrate/` - Solid Cable

## Forbidden Patterns

* ❌ **DO NOT** use jQuery or any external JavaScript libraries without approval
* ❌ **DO NOT** use Webpacker or any JavaScript bundler (we use Importmap)
* ❌ **DO NOT** use Bootstrap, Foundation, or any CSS framework besides Tailwind
* ❌ **DO NOT** create new CSS files; keep styles in Tailwind utilities
* ❌ **DO NOT** implement custom authentication; use existing Supabase integration
* ❌ **DO NOT** use inline styles; use Tailwind classes
* ❌ **DO NOT** bypass strong parameters in controllers
* ❌ **DO NOT** put business logic in controllers or models; use Service Objects

## Code Style & Linting

* **RuboCop:** Run `bin/rubocop` before committing
* **Brakeman:** Security scanning configured in CI
* Follow Rails conventions and idioms
* Use Ruby 3.3.6 syntax features
* Keep methods small (max 10-15 lines)
* Use descriptive variable names

## Testing

* **Framework:** RSpec
* Place specs in `spec/` matching `app/` structure
* Use FactoryBot for test data
* Mock external API calls
* Run tests with `bundle exec rspec`

## Deployment

* **Platform:** Render.com
* **Entry Point:** `bin/render-start` (runs migrations, starts jobs, runs Puma)
* **Environment Variables:** Defined in `.env.example`
* **Multi-Process:** Puma (web) + Solid Queue (jobs) run together in production
