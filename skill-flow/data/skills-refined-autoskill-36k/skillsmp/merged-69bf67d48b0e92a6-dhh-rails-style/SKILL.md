---
name: dhh-rails-style
description: Use this skill when writing Ruby and Rails code in DHH's distinctive 37signals style, applying conventions for models, controllers, and architectural decisions.
---

# 37signals/DHH Rails Style Guide

## Core Philosophy

- **"Vanilla Rails is plenty."** Maximize what Rails gives you, minimize dependencies, resist abstractions until necessary.
- **Rich domain models** over service objects.
- **CRUD controllers** over custom actions.
- **Concerns** for horizontal code sharing.
- **Records as state** over boolean columns.
- **Database-backed everything** (no Redis).
- **Build it yourself** before reaching for gems.

## Objective

Apply 37signals/DHH Rails conventions to Ruby and Rails code. This skill provides comprehensive domain expertise extracted from analyzing production 37signals codebases (Fizzy/Campfire) and DHH's code review patterns.

## Intake

What are you working on?

1. **Controllers** - REST mapping, concerns, Turbo responses, API patterns.
2. **Models** - Concerns, state records, callbacks, scopes, POROs.
3. **Views & Frontend** - Turbo, Stimulus, CSS, partials.
4. **Architecture** - Routing, multi-tenancy, authentication, jobs, caching.
5. **Testing** - Minitest, fixtures, integration tests.
6. **Gems & Dependencies** - What to use vs avoid.
7. **Code Review** - Review code against DHH style.
8. **General Guidance** - Philosophy and conventions.

**Specify a number or describe your task.**

## Essential Principles

### Core Philosophy

"The best code is the code you don't write. The second best is the code that's obviously correct."

**Vanilla Rails is plenty:**
- Rich domain models over service objects.
- CRUD controllers over custom actions.
- Concerns for horizontal code sharing.
- Records as state instead of boolean columns.
- Database-backed everything (no Redis).
- Build solutions before reaching for gems.

**What they deliberately avoid:**
- `devise` (custom ~150-line auth instead).
- `pundit/cancancan` (simple role checks in models).
- `sidekiq` (Solid Queue uses database).
- `redis` (database for everything).
- `view_component` (partials work fine).
- `graphql` (REST with Turbo sufficient).
- `factory_bot` (fixtures are simpler).
- `rspec` (Minitest ships with Rails).
- `Tailwind` (native CSS with layers).

## Quick Reference

### Naming Conventions

**Verbs:** `card.close`, `card.gild`, `board.publish` (not `set_style` methods).

**Predicates:** `card.closed?`, `card.golden?` (derived from presence of related record).

**Concerns:** Adjectives describing capability (`Closeable`, `Publishable`, `Watchable`).

**Controllers:** Nouns matching resources (`Cards::ClosuresController`).

**Scopes:**
- `chronologically`, `reverse_chronologically`, `alphabetically`, `latest`.
- `preloaded` (standard eager loading name).
- `indexed_by`, `sorted_by` (parameterized).

### REST Mapping

Instead of custom actions, create new resources:

```ruby
POST /cards/:id/close    → POST /cards/:id/closure
DELETE /cards/:id/close  → DELETE /cards/:id/closure
POST /cards/:id/archive  → POST /cards/:id/archival
```

### Ruby Syntax Preferences

```ruby
# Symbol arrays with spaces inside brackets
before_action :set_message, only: %i[ show edit update destroy ]

# Private method indentation
  private
    def set_message
      @message = Message.find(params[:id])
    end

# Expression-less case for conditionals
case
when params[:before].present?
  messages.page_before(params[:before])
else
  messages.last_page
end

# Bang methods for fail-fast
@message = Message.create!(params)

# Ternaries for simple conditionals
@room.direct? ? @room.users : @message.mentionees
```

## Success Criteria

Code follows DHH style when:
- Controllers map to CRUD verbs on resources.
- Models use concerns for horizontal behavior.
- State is tracked via records, not booleans.
- No unnecessary service objects or abstractions.
- Database-backed solutions preferred over external services.
- Tests use Minitest with fixtures.
- Turbo/Stimulus for interactivity (no heavy JS frameworks).
- Native CSS with modern features (layers, OKLCH, nesting).
- Authorization logic lives on User model.
- Jobs are shallow wrappers calling model methods.

## Credits

Based on [The Unofficial 37signals/DHH Rails Style Guide](https://gist.github.com/marckohlbrugge/d363fb90c89f71bd0c816d24d7642aca) by [Marc Köhlbrugge](https://x.com/marckohlbrugge), generated through deep analysis of the Fizzy codebase.