# MVP Application Categories Guide

This guide explains each category for MVP application design with focus on building the minimum viable version that tests core hypotheses.

**MVP Philosophy:** Build the absolute minimum to test if the core value proposition works. Cut ruthlessly. Ship fast, learn, iterate.

---

## MVP DEFINITION

### 1. Cel MVP

**What it is:** The specific hypothesis or problem the MVP is designed to test or solve.

**Why it matters:** Without a clear purpose, you build features nobody needs. MVP is NOT "the app but smaller" - it's a test vehicle.

**Key aspects:**
- **Core hypothesis:** What assumption are you testing? (e.g., "Users will pay $X for Y solution")
- **Problem focus:** Which ONE problem from business brief are you solving?
- **Success criteria:** How do you know if MVP worked?
- **Learning goals:** What do you need to learn from this version?

**Key questions:**
- "What's the ONE thing this MVP must prove?"
- "What happens if the MVP succeeds? What's next?"
- "What happens if it fails? What do you learn?"
- "Are you testing the problem, solution, or business model?"

**Red flags:**
- "We want to build everything" (not MVP thinking)
- Can't articulate what you're testing
- MVP has 20 features (way too much)
- "We'll learn what users want after we build it" (build to learn, not hope)

---

### 2. Użytkownicy MVP

**What it is:** The specific first users who will test the MVP - not all future users, just the first ones.

**Why it matters:** Can't build for "everyone". MVP is for early adopters who are desperate enough to use imperfect software.

**Key aspects:**
- **How many:** 5 users? 10? 50? 100? (Be specific)
- **Who specifically:** Named people if possible, or very narrow profile
- **Why them:** Why these users first?
- **Access:** How do you reach them? Do you already know them?
- **Tolerance:** Will they tolerate bugs and missing features?

**Key questions:**
- "Who are your first 5-10 users? Can you name them?"
- "Do you already have access to these users?"
- "Why will they try an imperfect MVP?"
- "What's their pain level? (desperate users = better for MVP)"
- "Will they give you honest feedback?"

**Red flags:**
- "We'll launch to everyone" (way too broad for MVP)
- Don't know specific first users
- Targeting users who need polish and perfection
- "We'll find users after we build" (backwards)

---

### 3. Must-have funkcjonalności

**What it is:** The absolute bare minimum features that must work for MVP to deliver any value.

**Why it matters:** Every feature adds time, cost, and complexity. Ruthlessly cut to essentials.

**How to identify must-haves:**
- Would MVP be useless without this feature? → Must-have
- Would it be less convenient but still work? → Nice-to-have (cut it)
- Can users achieve core value without it? → Cut it

**Key questions:**
- "Walk me through the absolute minimum user journey. What features are touched?"
- "If you removed [feature X], would MVP still work?"
- "What can users do manually as a workaround?"
- "What can you fake/simulate instead of building?"

**Red flags:**
- 10+ must-have features (way too many)
- "Users expect this feature" (they can wait for v2)
- Including features "because competitors have them"
- "It's easy to build so we should add it" (scope creep)

---

### 4. Out of scope

**What it is:** Explicit list of what you're NOT building in MVP - features consciously deferred to later.

**Why it matters:** Helps resist scope creep. Makes trade-offs explicit. Speeds up development.

**Common out-of-scope items for MVP:**
- Advanced features
- Nice-to-have polish
- Edge case handling
- Performance optimization
- Multiple platforms
- Admin tools (do it manually)
- Robust error handling (basic is OK)
- Integrations (build later)

**Key questions:**
- "What features do you WANT but can live without for MVP?"
- "What will users complain is missing? Can they wait?"
- "What can you do manually behind the scenes?"
- "What edge cases can you ignore for now?"

**Red flags:**
- Out-of-scope list is short or empty (not cutting enough)
- "We need everything" (wrong mindset)
- Can't articulate what's deferred

---

## UX MVP

### 5. Kluczowe user flows

**What it is:** The 2-3 most critical paths users must be able to complete in MVP.

**Why it matters:** Can't build all user journeys in MVP. Focus on core value delivery paths only.

**For each flow:**
- **Start point:** Where does it begin?
- **End point:** What's the outcome?
- **Steps:** Minimum steps to get there
- **Why critical:** Why this flow must work in MVP

**Key questions:**
- "What are the 2-3 flows that deliver core value?"
- "Walk me through each step. What can be simplified?"
- "What flows can you skip entirely for MVP?"
- "Do these flows test your core hypothesis?"

**Red flags:**
- More than 3-4 critical flows (too much for MVP)
- Flows include nice-to-have features
- No happy path defined
- Flows haven't been walked through step-by-step

---

### 6. Ekrany MVP

**What it is:** The minimum set of screens/views needed to support critical user flows.

**Why it matters:** Every screen takes time to design and build. Fewer screens = faster MVP.

**Screen inventory:**
- List each screen
- What it does
- Which user flow it supports
- Can it be combined with another screen?

**Key questions:**
- "How many screens do you need? Can you list them?"
- "Can any screens be combined?"
- "Do you need separate create/edit screens or one that does both?"
- "What screens can be text-only/no-design for MVP?"

**Red flags:**
- 20+ screens (way too many for MVP)
- Separate screens for things that could be one screen
- Admin screens (do admin work manually)
- Settings/preferences screens (hardcode settings for MVP)
- Beautiful design when ugly-but-functional would work

---

### 7. Platforma MVP

**What it is:** The ONE platform you build for first - web, iOS, Android, desktop.

**Why it matters:** Multi-platform = multiply complexity and cost. Pick one, ship fast.

**Platform options:**
- **Web:** Fastest to build, works everywhere, easiest to update
- **iOS:** If users are iOS-only and mobile-first is critical
- **Android:** If users are Android-only and mobile-first is critical
- **Desktop:** Rarely the right choice for MVP unless web won't work

**Key questions:**
- "Where do your first users spend time? Desktop or mobile?"
- "Can web work, even if mobile is eventual goal?"
- "Are users iOS or Android? Do you know?"
- "What's the minimum to test your hypothesis?"

**Red flags:**
- "We need iOS AND Android AND web" (no, pick one)
- Building native mobile when web would work
- "Users expect an app" (maybe, but not for MVP)
- Choosing platform based on what you know vs. what users need

---

## TECH MVP

### 8. Stack technologiczny

**What it is:** Languages, frameworks, libraries, tools for MVP.

**Why it matters:** Stack choice affects speed, cost, and scalability. For MVP: prioritize speed over "perfect" architecture.

**Stack considerations:**
- **Use what you know:** Fastest to build with familiar tools
- **Proven technologies:** Boring tech that works
- **Ecosystem:** Good libraries/tools available
- **Hiring:** Can you find help if needed?

**Common MVP stacks:**
- **Web:** React/Vue + Node/Python/Ruby + PostgreSQL/MySQL
- **No-code:** Webflow, Bubble, Airtable + Zapier
- **Low-code:** Retool, Softr, Glide

**Key questions:**
- "What tech do you/your team already know?"
- "What's the fastest way to build this?"
- "Are you overengineering? Could simpler work?"
- "Could no-code/low-code work for MVP?"

**Red flags:**
- Using bleeding-edge tech for MVP
- "Let's learn [new framework] while building MVP"
- Overengineered architecture (microservices, etc.)
- Building custom when off-the-shelf exists
- "We'll use this because it scales to 1M users" (you have 0 users)

---

### 9. Architektura MVP

**What it is:** How the application is structured - frontend, backend, database, services.

**Why it matters:** Complex architecture takes longer to build and maintain. MVP should be simple.

**MVP architecture principles:**
- **Monolith is OK:** Single codebase is faster for MVP
- **Serverless is great:** Less ops overhead
- **Managed services:** Use AWS RDS, not self-hosted database
- **Simple is better:** Avoid unnecessary complexity

**Key questions:**
- "Do you need backend or can frontend + Firebase/Supabase work?"
- "What's the simplest architecture that could work?"
- "Are you building for scale you don't have yet?"
- "What managed services can you use vs. building yourself?"

**Red flags:**
- Microservices for MVP (massive overkill)
- "We'll build it scalable from day 1" (premature optimization)
- Complex distributed systems
- Building infrastructure instead of product

---

### 10. Model danych

**What it is:** Core data structures, relationships, and storage for MVP.

**Why it matters:** Data model is hardest to change later. But for MVP, simple and flexible beats perfect.

**MVP data model principles:**
- **Core entities only:** User, main business object, relationships
- **Flexible schema:** NoSQL or loose schema OK for MVP
- **Defer optimization:** Don't worry about perfect normalization
- **Manual admin:** No need for complex admin UI

**Key questions:**
- "What data must you store?"
- "What are the core entities and relationships?"
- "Can you use a simple key-value store or do you need relational?"
- "What data can you NOT lose? (determines backup strategy)"

**Red flags:**
- Over-normalized schema for MVP
- "We need a data warehouse" (no, you have 10 users)
- Complex relationships before understanding domain
- Not thinking about data at all (equally bad)

---

### 11. Bezpieczeństwo minimum

**What it is:** Essential security measures for MVP - what you can't skip.

**Why it matters:** Security breaches kill startups. But perfect security takes time. Balance risk for MVP.

**MVP security must-haves:**
- **Authentication:** Users can log in securely (use Auth0/Clerk/Supabase, don't build your own)
- **Authorization:** Users can only access their own data
- **HTTPS:** SSL certificates (free with Let's Encrypt/CloudFlare)
- **Password handling:** Hashed, not plaintext (use bcrypt/library)
- **Input validation:** Basic protection against SQL injection, XSS

**MVP security nice-to-haves (defer if needed):**
- 2FA
- Advanced audit logs
- Rate limiting
- Penetration testing

**Key questions:**
- "How do users authenticate?"
- "How do you ensure users only see their own data?"
- "Are you using proven auth libraries or building your own?"
- "What happens if you get hacked?"

**Red flags:**
- Building authentication from scratch (use library!)
- Storing passwords in plaintext
- No HTTPS
- "We'll add security later" (for auth/data access, no)
- Overbuilding security before having users

---

## EXECUTION MVP

### 12. Timeline

**What it is:** How long to build MVP from now to first users can test it.

**Why it matters:** Long timelines = burning money before learning anything. Ship fast, learn, iterate.

**Timeline considerations:**
- **Realistic estimation:** Multiply initial guess by 2-3x
- **MVP should be weeks/months, not years**
- **Phases:** Design, build, test, deploy
- **Blockers:** What could delay you?

**Key questions:**
- "How long to build the must-have features?"
- "What's on the critical path?"
- "Have you built something like this before? How long did it take?"
- "What if it takes 2x longer? Can you still afford it?"
- "Can you release in phases? (week 1: core flow, week 2: add X)"

**Red flags:**
- "12 months to MVP" (way too long, not MVP thinking)
- No timeline at all
- Timeline assumes everything goes perfectly
- "We'll launch when it's perfect" (it never will be)

---

### 13. Koszty budowy

**What it is:** How much it costs to build and run MVP until you learn if it works.

**Why it matters:** Need to budget correctly. Running out of money before validation kills startups.

**Cost categories:**
- **Development:** Developers (salary or contractors), designers
- **Tools:** Development tools, subscriptions, licenses
- **Infrastructure:** Hosting, databases, services (AWS/Vercel/Supabase)
- **Third-party:** APIs, services (Auth0, Stripe, SendGrid)
- **Domain/SSL:** Domain name, certificates (cheap)

**Key questions:**
- "Who's building this? In-house or contractors?"
- "What does development cost per month?"
- "What tools/services do you need to pay for?"
- "What's hosting cost for 10 users? 100 users?"
- "What's total cost to get to 'done' and run for 3 months?"

**Red flags:**
- No budget/cost estimate
- Underestimating costs (especially hosting as you grow)
- Expensive enterprise tools for MVP
- "We'll figure out costs later" (wrong)

---

### 14. Deployment

**What it is:** How you get MVP from development to production where users can access it.

**Why it matters:** Complicated deployment slows iteration. For MVP, simple and fast beats perfect.

**MVP deployment principles:**
- **Managed hosting:** Vercel, Netlify, Railway, Render (not self-hosted servers)
- **Simple pipeline:** Push to main = deploy (Vercel/Netlify do this)
- **No complex CI/CD initially:** Can add later
- **Easy rollbacks:** Can revert if broken

**Common MVP deployment:**
- Frontend: Vercel, Netlify, CloudFlare Pages
- Backend: Railway, Render, Heroku, AWS Elastic Beanstalk
- Database: Managed service (AWS RDS, PlanetScale, Supabase)

**Key questions:**
- "Where will you host this?"
- "How do you deploy updates?"
- "What happens if you break production?"
- "Can you deploy daily? Weekly? (slower = bad for MVP)"

**Red flags:**
- Complex Kubernetes setup for MVP (massive overkill)
- "We'll build our own deployment pipeline" (no)
- Self-hosting everything
- No deployment plan

---

### 15. Success metrics

**What it is:** How you measure if MVP achieved its goal - did you learn what you needed?

**Why it matters:** Without metrics, you don't know if MVP succeeded. Can't iterate blindly.

**MVP metrics:**
- **Validation metrics:** Did core hypothesis prove true?
- **Usage metrics:** Are users using it? How much?
- **Feedback metrics:** What do users say?
- **Business metrics:** Revenue, conversion, retention (if relevant)

**Examples:**
- "5 out of 10 users complete core flow without help"
- "Users return 3+ times in first week"
- "3 users say they'd pay $X for this"
- "50% of invited users sign up"

**Key questions:**
- "How do you know if MVP succeeded?"
- "What number would make you confident to build more?"
- "What number would make you pivot or stop?"
- "What qualitative feedback do you need?"

**Red flags:**
- No metrics defined
- Only vanity metrics (signups, page views)
- No target values ("we'll see how it goes")
- Not measuring core hypothesis

---

## Using This Guide

**Critical MVP mindset:**
- **Cut ruthlessly:** When in doubt, cut it
- **Ship fast:** Weeks, not months
- **Learn quickly:** MVP is a learning tool
- **Ugly is OK:** Functional beats pretty
- **Manual is OK:** Do things by hand if it saves build time
- **Fake it:** Wizard of Oz testing (appear automated but human behind scenes)

**During dialogue:**
- Start with MVP Definition (1-4) - what are we testing?
- Cover UX MVP (5-7) - minimum interface
- Tech MVP (8-11) - simplest tech that works
- Execution (12-15) - can we actually build this?

**Red flag themes to watch:**
- Scope creep (too many features)
- Perfect over done (over-engineering)
- Building for scale that doesn't exist
- No learning plan (not testing hypotheses)
- Too long to market (should be fast)

**Remember:** MVP is not "version 1.0 but smaller." It's a test to validate core assumptions with minimum effort. Build only what's needed to learn.
