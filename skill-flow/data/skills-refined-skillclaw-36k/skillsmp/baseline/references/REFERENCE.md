# Baseline Reference

**Architecture:**
- Service-oriented (BaseService, ExternalService)
- Component-based views (ViewComponent)
- Concern-driven models and controllers
- I18n-first approach

## Core Patterns

### Services

**BaseService** - Internal services with ActiveJob integration
- Sync/async execution: `.call()`, `.call_async()`, `.call_in()`, `.call_at()`
- Job status tracking, call logging, uniqueness checking
- See: [lib/baseline/base_service.rb](lib/baseline/base_service.rb)

**ExternalService** - Third-party API integrations
- HTTP requests, retries, pagination
- Pattern: `Baseline::External::ServiceName.call(:action_name, args)`
- See: [lib/baseline/external_service.rb](lib/baseline/external_service.rb)

**Dynamic Service Resolution**
- Models can call services via `._do_action_name(args)`
- Pattern: `user._do_send_email(params)` → `Users::SendEmail.call(user, params)`
- Async: `user._do_send_email(_async: true)`

### Model Concerns

All concerns are under `Baseline::` namespace.

**ModelCore** ([model_concerns/model_core.rb](lib/baseline/model_concerns/model_core.rb))
- Automatic association scopes (`with_X`, `without_X`)
- Automatic boolean scopes
- Service resolution via `_do_*` methods
- Remote attachment helpers: `remote_#{attachment}_url=`
- Cloning support, schema introspection

**Domain Models (acts_as_*)**
- **ActsAsUser** - Authentication, sessions, remember tokens, deactivation
- **ActsAsAdminUser** - Admin capabilities
- **ActsAsTask** - Task management with Todoist integration
- **ActsAsNotification** - User notifications
- **ActsAsMessage** - Messaging system
- **ActsAsEmailDelivery** - Email tracking with Postmark
- **ActsAsSubscription** - Subscription management
- **ActsAsInvoicingDetails** - Invoice addresses with VAT/IBAN validation
- **ActsAsCreditNote** - Credit note handling
- **ActsAsCategory** - Category taxonomy
- **ActsAsSection** - Content sections (headline + content)
- **ActsAsPdfFile** - PDF file attachments
- **ActsAsTodoistEvent** - Todoist webhook events
- **ActsAsEmailConfirmation** - Email verification tokens

See: [lib/baseline/model_concerns/acts_as_*.rb](lib/baseline/model_concerns/)

**Feature Modules (has_*)**

*Identity & Authentication:*
HasEmail, HasPassword, HasLoginToken, HasFirstAndLastName, HasFullName, HasGender

*Localization:*
HasLocale, HasCountry

*URLs & Content:*
HasFriendlyID, HasYoutubeId, HasSections, HasCategories, HasPdfFiles

*Structure:*
HasPosition, HasAssociationWithPosition, HasTimestamps

*Business Logic:*
HasChargeVat, HasDelivery, HasMessageable, HasEmailConfirmations

*Other:*
HasEnumArray, HasStartAndEnd, Deactivatable, TouchAsync, UserProxy, Wizardable

See: [lib/baseline/model_concerns/has_*.rb](lib/baseline/model_concerns/)

### Controller Concerns

All concerns are under `Baseline::` namespace (not `Baseline::ControllerConcerns::`).

**ApplicationControllerCore** - Foundation for all controllers
- PaperTrail tracking, Stimulus helpers, flash messages, Turbo frames

**Authentication** - Cookie-based session management
- `current_user`, `authenticated?`, `sign_in`, `sign_out`, `require_authentication`

**Base Controllers**
- WebBaseControllable, ApiControllerCore, AvoApplicationControllable

**Domain Controllers**
- ContactRequestControllable, PasswordsControllable, SubscriptionsControllable
- GoogleOauthControllable, ApiTodoistControllable

**Infrastructure**
- ErrorsControllable, EssentialsControllable, FramesControllable

**Patterns**
- **Wizardify** - Multi-step wizard forms with step progression
- I18nScopes, NamespaceLayout, PageTitle, SetLocale

See: [lib/baseline/controller_concerns/*.rb](lib/baseline/controller_concerns/)

## Services

### External Integrations

All under `Baseline::External::` namespace.

- **Cloudflare** - Turnstile, cache purging, R2 storage
- **GitHub** - Workflow dispatch, file commits (via Octokit)
- **Google::Oauth** - OAuth flow, token management
- **Todoist** - Task management, projects, webhooks
- **Lexoffice** - German invoicing software
- **Slack** - Simple notifications
- **Genderize** - Gender detection from names
- **HtmlCssToImage** - Screenshot generation
- **LogoDev** - Company logo fetching
- **Microlink** - URL metadata extraction
- **Pretix** - Event ticketing

See: [lib/baseline/services/external/*.rb](lib/baseline/services/external/)

### Domain Services

**Converters** - Format conversion (HTML↔Markdown↔Text)

**Sections** - Content rendering (HTML, Markdown, MJML, Text)

**Messages** - Message creation and I18n generation

**Email** - EmailConfirmations, EmailDeliveries

**Tasks** - Create, Todoist sync (CreateAll, Update, DeleteOld)

**Invoicing** - InvoicingDetails::UpsertLexoffice, Lexoffice::DownloadPdf

**Notifications** - Notifications::Create

**Sitemaps** - GenerateAll, Fetch

**Other** - AdminUsers, CreateAndSyncDbBackup, DownloadFile, ReportError, Toucher

See: [lib/baseline/services/](lib/baseline/services/)

## View Components

All under `Baseline::` namespace.

**Forms:** FormFieldComponent, FormActionsComponent, CopyableTextFieldComponent, ContactRequestFormComponent

**Layout:** NavbarComponent, CardComponent, ModalComponent, AccordionComponent, TabPanelsComponent, RowColsComponent

**Content:** IconComponent, AvatarBoxComponent, AttachmentImageComponent, PreviewCardComponent, IframeComponent, ItemListComponent, ListWithIconsComponent

**Interaction:** LoadMoreComponent, LoadingComponent, ToastComponent, ShareButtonComponent, WizardActionsComponent

See: [lib/baseline/components/*.rb](lib/baseline/components/)

## Avo Admin Integration

**Configuration:** [lib/baseline/initializers/avo.rb](lib/baseline/initializers/avo.rb)
- License key, current user method, authorization, default currency

**Helpers:** [lib/baseline/avo/action_helpers.rb](lib/baseline/avo/action_helpers.rb)
- `process_batch`, `success`, `error`, `pluralize_records`

**Filters:** Language, Search

**ActsAsAvoResource** - Avo resource associations for models

## Initializers

Third-party gem configurations in [lib/baseline/initializers/](lib/baseline/initializers/)

Avo, Cloudinary, EmailValidator, FriendlyId, MJML, Money, Namespaces, Octokit, PaperTrail, PgHero, Postmark, Sentry

## Utilities

**CallLogger** - Service call logging
**ExceptionWrapper** - Exception handling/reporting
**UniquenessChecker** - Duplicate job prevention
**Poller** - Retry logic with exponential backoff
**StimulusController** - Stimulus data attribute generation
**URLManager** - URL normalization and parsing
**ZstdCompressor** - Compression utilities
**Language** - Locale handling
**IdentifyUrl** - URL type identification
**Validators:** URLFormatValidator, ArrayUniquenessValidator
**Monkeypatches:** Object#if, Object#unless, I18n enhancements, ActiveRecord extensions

See: [lib/baseline/*.rb](lib/baseline/)

## Special Patterns

### Wizard Pattern

Multi-step forms via `Baseline::Wizardify` concern. Define steps, handle progression, validate per step.

See: [lib/baseline/controller_concerns/wizardify.rb](lib/baseline/controller_concerns/wizardify.rb)

### Stimulus Helper (`stimco`)

Always use the `stimco` helper for Stimulus data attributes in views instead of manual strings:

```haml
-# Just add data-controller attribute
%div{ data: stimco(:controller_name) }

-# For targets or actions, use to_h: false to get the object
- stimco = stimco(:controller_name, to_h: false)

%div{ data: stimco.target(:target_name) }
%button{ data: stimco.action(:action_name) }
%button{ data: stimco.action(:show, url: some_url) }
```

See: [lib/baseline/stimulus_controller.rb](lib/baseline/stimulus_controller.rb)

### Sections System

Flexible content with multiple render formats. Initialize from Markdown, render as HTML/Markdown/MJML/Text.

See: [lib/baseline/model_concerns/has_sections.rb](lib/baseline/model_concerns/has_sections.rb), [lib/baseline/services/sections/](lib/baseline/services/sections/)

## Testing

**RSpec Configuration**
- [lib/baseline/spec/rails_helper.rb](lib/baseline/spec/rails_helper.rb) - Rails setup with Database Cleaner, FactoryBot, Shoulda
- [lib/baseline/spec/spec_helper.rb](lib/baseline/spec/spec_helper.rb) - Base config with SimpleCov

**Test Helpers**
- ApiHelpers - `json_response`, `response_status`, `api_headers`
- CapybaraHelpers - `visit_and_wait`, `click_and_wait`, `fill_in_and_wait`, `wait_for_turbo`

## Code Conventions

**Namespaces:**
- Model concerns: `Baseline::HasEmail`, `Baseline::ActsAsUser`
- Controller concerns: `Baseline::Authentication`, `Baseline::Wizardify`
- External services: `Baseline::External::Todoist`
- Components: `Baseline::FormFieldComponent`

**File Organization:**
- Zeitwerk autoloading
- Concerns in `lib/baseline/model_concerns/` and `lib/baseline/controller_concerns/`
- Services in `lib/baseline/services/`
- Components in `lib/baseline/components/`

## External Dependencies

**Core:** Rails, ActiveRecord, ActiveJob, ActiveStorage, ViewComponent, Turbo, Stimulus
**Auth & Security:** BCrypt, Sentry, PaperTrail
**Admin:** Avo, Pundit
**UI:** Bootstrap, FontAwesome
**Content:** MJML, Markdown parsers, FriendlyId, Cloudinary
**Infrastructure:** PostgreSQL, PgHero, Redis, HTTP gem, Playwright, Zeitwerk

## Environment Variables

**Required:**
```bash
DATABASE_URL=postgresql://...
POSTMARK_API_TOKEN=...
SENTRY_DSN=...
AVO_LICENSE_KEY=...
```

**Optional (based on features):**
```bash
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
TODOIST_API_TOKEN=...
LEXOFFICE_API_KEY=...
CLOUDFLARE_API_KEY=...
CLOUDFLARE_ZONE_ID=...
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
GITHUB_ACCESS_TOKEN=...
SLACK_WEBHOOK_URL=...
```

## Quick Reference

**Include a model concern:**
```ruby
class User < ApplicationRecord
  include Baseline::ActsAsUser
  include Baseline::HasEmail
end
```

**Call a service:**
```ruby
Users::SendEmail.call(user)
Users::SendEmail.call_async(user)

# Preferred:
user._do_send_email
user._do_send_email(_async: true)
```

**External service:**
```ruby
Baseline::External::Todoist.call(token, :get_tasks)
Baseline::External::Cloudflare.call(:purge_cache, urls: ["https://..."])
```

**Render a component:**
```haml
= render Baseline::FormFieldComponent.new(form: f, field: :email, type: :text)
-# Preferred
= component :form_field, form: f, field: :email, type: :text
```

**Create wizard controller:**
```ruby
class Web::OnboardingController < Web::BaseController
  include Baseline::Wizardify
  wizard_steps :profile, :preferences, :confirmation
end
```

## Resources

- Source code: [lib/baseline/](lib/baseline/)
- Example app: [spec/dummy/](spec/dummy/)
- Tests for usage examples: [spec/](spec/)
