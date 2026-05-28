# Critical Questions Library for MVP Applications

This library contains challenging questions designed to expose over-engineering, scope creep, and unrealistic MVP plans.

## Core Philosophy

**Your job:** Cut, simplify, challenge. Make the MVP smaller and faster.

**Mantras:**
- "Can you cut that?"
- "What's the absolute minimum?"
- "Why build when you can fake it?"
- "That's not MVP, that's v2"

---

## MVP DEFINITION

### 1. Cel MVP

**Testing the purpose:**
- "What specific hypothesis are you testing with this MVP?"
- "If the MVP succeeds, what do you learn? What's next?"
- "If it fails, what do you learn?"
- "Are you testing the problem, the solution, or the business model?"

**Exposing fuzzy thinking:**
- "You said you want to 'validate the idea' - what specifically does that mean?"
- "How will you know if you succeeded?"
- "What question must this MVP answer?"

**Challenging scope:**
- "That sounds like you want to build the full product, not an MVP."
- "What's the ONE thing that, if it works, justifies building more?"
- "Can you test that hypothesis without building software?"

**Red flag check:**
- "You mentioned 10 features. Which ONE feature tests your core hypothesis?"
- "Are you building to learn, or building what you think users want?"

---

### 2. Użytkownicy MVP

**Getting specific:**
- "Who are your first 5-10 users? Can you name them?"
- "Do you already have access to these users or need to find them?"
- "Why will they try an imperfect product?"
- "How desperate are they for a solution? (scale 1-10)"

**Testing access:**
- "How will you get this in front of them?"
- "Have you talked to them? What did they say?"
- "Will they tolerate bugs and missing features?"
- "Will they give honest feedback or just be nice?"

**Challenging "everyone":**
- "You said 'small businesses' - which 5 specific businesses will test this?"
- "Everyone' is not an MVP audience. Who FIRST?"
- "Why these users first instead of others?"

**Reality check:**
- "If you emailed these 10 users today saying 'I have a rough version, want to try?', how many would say yes?"
- "What if only 2 of 10 respond? Then what?"

---

### 3. Must-have funkcjonalności

**Ruthless cutting:**
- "If you removed [feature X], would MVP completely fail or just be less convenient?"
- "What can users do manually as a workaround for [feature Y]?"
- "Which feature, if it works, proves your core hypothesis?"
- "Can you test this without building [feature Z]?"

**Challenging every feature:**
- "You listed [X features]. Walk me through: which ONE is truly essential?"
- "Why is [feature] must-have vs. nice-to-have?"
- "What happens if you don't build [feature] in MVP?"
- "Has a user specifically asked for this, or are you assuming they need it?"

**Fake it instead:**
- "Could you do [feature] manually behind the scenes?"
- "Could you fake [feature] with a human doing the work?"
- "Could you use a spreadsheet instead of building this?"

**Priority check:**
- "If you could only build ONE feature, which one?"
- "If you had one week, what would you build?"
- "What would Wizard of Oz version look like? (appear automated but do manually)"

---

### 4. Out of scope

**Testing cut discipline:**
- "What are you NOT building in MVP?"
- "That's a short list. What else can you cut?"
- "You want [nice feature]. Can users wait for v2?"
- "What features will users complain are missing?"

**Challenging scope creep:**
- "You said that's out of scope, but then mentioned building it. Which is it?"
- "Why is [feature X] must-have when you said similar feature Y is out of scope?"

**Admin shortcuts:**
- "Do you need admin UI or can you edit database directly?"
- "Do you need user management or can you manually create accounts for first users?"
- "Do you need reporting or can you query database?"

**Edge cases:**
- "What edge cases are you ignoring for MVP?"
- "What happens when [unlikely thing]? Can you handle it manually?"

---

## UX MVP

### 5. Kluczowe user flows

**Getting specific:**
- "Walk me through the 2-3 flows that must work."
- "Start to finish, step by step, what happens?"
- "Why is this flow critical vs. nice-to-have?"

**Simplification:**
- "That's 8 steps. Which 3 are essential?"
- "Can any steps be combined?"
- "What can you remove from this flow?"

**Challenging complexity:**
- "You said 5 critical flows. An MVP should have 2-3. Which can you cut?"
- "Is this flow testing your hypothesis or just making it nicer?"
- "Do you need this flow or are you copying what competitors do?"

**Happy path focus:**
- "What if you only support the happy path for MVP?"
- "What edge cases can you ignore?"
- "What errors can you handle manually vs. building error flows?"

---

### 6. Ekrany MVP

**Counting screens:**
- "How many screens total? List them."
- "That's a lot. Which screens can be combined?"
- "Do you need separate create/edit screens?"

**Challenging necessity:**
- "Why do you need a [settings/profile/preferences] screen for MVP?"
- "Can you hardcode those settings for first users?"
- "Do you need onboarding screens or can you just give users instructions?"
- "Admin screens? Or can you do admin work manually?"

**Simplification:**
- "Can this be one screen instead of three?"
- "Does this screen need design or can it be ugly text?"
- "Do you need navigation or can users go linearly?"

**Reality check:**
- "For 10 users, do you need [sophisticated feature]?"
- "What's the minimum UI that functions?"

---

### 7. Platforma MVP

**Platform choice:**
- "Why [iOS/Android/web]? Where do your first users actually spend time?"
- "Can web work even if you eventually want mobile?"
- "You said mobile - iOS or Android? Pick one."
- "Why native app when responsive web would work?"

**Challenging multi-platform:**
- "You said iOS AND Android. No. Which ONE first?"
- "Building for both will take 2-3x longer. Worth it?"
- "What if you build web first, see if it works, THEN build mobile?"

**Reality check:**
- "How many of your first 10 users have iOS vs Android?"
- "Do you know, or are you guessing?"
- "What if you picked wrong platform - how quickly could you switch?"

---

## TECH MVP

### 8. Stack technologiczny

**Challenging choices:**
- "Why [framework X] vs. [simpler option Y]?"
- "Do you know this tech or are you learning while building MVP?"
- "What's the fastest stack you could use, even if not 'perfect'?"
- "Could no-code/low-code work? (Bubble, Webflow, Airtable)"

**Overengineering check:**
- "Why [complex modern framework] for MVP?"
- "Are you choosing tech because it's cool or because it's fastest?"
- "That tech is overkill. What's simpler?"

**Team fit:**
- "Does your team know this stack?"
- "If not, why learn new tech while building MVP?"
- "Who on your team can actually build this?"

**Off-the-shelf:**
- "Could you use WordPress/Shopify/Webflow instead of custom?"
- "What if you used Firebase and skipped building backend?"
- "Could Airtable + Zapier work for MVP?"

---

### 9. Architektura MVP

**Simplicity check:**
- "Walk me through your architecture. Why is it this complex?"
- "Do you need microservices or would monolith be faster?"
- "Why build backend when Firebase/Supabase exists?"
- "That's overengineered. What's the simplest architecture?"

**Premature optimization:**
- "You're building for 1M users when you have 0. Why?"
- "What if you built simple first, then scaled later?"
- "Do you need [distributed system/caching/message queue] for 10 users?"

**Managed services:**
- "Why self-host database instead of AWS RDS/PlanetScale?"
- "Why build auth instead of Auth0/Clerk?"
- "What are you building that you could use managed service for?"

**Reality check:**
- "What's the simplest thing that could work?"
- "Are you building for scale you don't have?"

---

### 10. Model danych

**Understanding data:**
- "What data must you store?"
- "What are the core entities?"
- "How do they relate?"

**Simplification:**
- "Do you need relational DB or would document store work?"
- "Why this complex schema for MVP?"
- "Can you use simpler data model initially?"

**Premature optimization:**
- "You're optimizing for query performance before having users. Why?"
- "Do you need perfect normalization for MVP?"
- "What if you used flat structure first?"

**Risk:**
- "What data can you NOT lose? How do you back it up?"
- "What happens if database crashes?"

---

### 11. Bezpieczeństwo minimum

**Essentials:**
- "How do users log in?"
- "Are you building auth yourself or using library? (should use library)"
- "How do you ensure users only see their own data?"
- "Are you using HTTPS?"

**Challenging custom auth:**
- "Why build authentication instead of using Auth0/Clerk/Supabase?"
- "How are you storing passwords? (better be hashed)"
- "Have you done auth before? It's easy to get wrong."

**Over-building:**
- "Do you need 2FA for MVP? Why?"
- "Do you need audit logs for 10 users?"
- "Are you building security features before having users to secure?"

**Risk assessment:**
- "What's the worst that happens if someone hacks this MVP?"
- "What data is sensitive? How are you protecting it?"

---

## EXECUTION MVP

### 12. Timeline

**Getting realistic:**
- "How long to build this?"
- "Have you built something similar? How long did that take?"
- "What if it takes 2x your estimate? 3x?"
- "What's on critical path?"

**Challenging long timelines:**
- "You said 6 months. That's too long. What would 6 weeks look like?"
- "Why so long? What's taking the time?"
- "Can you release in phases? Week 1, week 2, week 3?"

**Scope reduction:**
- "If you had to ship in 2 weeks, what would you build?"
- "What's the absolute minimum to get user feedback?"
- "Can you get something in users' hands in 1 week?"

**Reality check:**
- "When did you want to start learning if this works?"
- "Every month of building is a month not learning. Worth it?"

---

### 13. Koszty budowy

**Getting numbers:**
- "How much to build this?"
- "Who's building? What do they cost?"
- "What tools/services do you need to pay for?"
- "What's hosting cost?"

**Challenging unknowns:**
- "You don't know the cost? How will you budget?"
- "What if it costs 2x what you expect?"
- "When do you run out of money?"

**Cost optimization:**
- "Why pay for [expensive tool] for MVP?"
- "Can you use free tier of [service]?"
- "Do you need [premium service] or will basic work?"

**Runway:**
- "How many months of runway do you have?"
- "How many months to build + run MVP + analyze?"
- "What if you don't break even? Can you afford that?"

---

### 14. Deployment

**Simplicity:**
- "Where will you host this?"
- "How do you deploy?"
- "Why not just use Vercel/Netlify/Railway?"

**Overengineering:**
- "Why Kubernetes for MVP? That's massive overkill."
- "Do you need CI/CD pipeline or can you just push to deploy?"
- "Why self-host when managed hosting exists?"

**Speed:**
- "How long to deploy a change?"
- "Can you deploy multiple times per day?"
- "What if you break production? How fast can you fix?"

**Reality:**
- "Have you deployed an app before?"
- "Who's handling DevOps?"
- "What's your plan if deployment fails?"

---

### 15. Success metrics

**Defining success:**
- "How do you know if MVP succeeded?"
- "What number would make you confident?"
- "What number would make you shut it down?"

**Testing hypothesis:**
- "Does this metric actually test your hypothesis?"
- "If [metric is good] but [real outcome is bad], did you succeed?"

**Challenging vague metrics:**
- "You said 'user engagement' - what specifically?"
- "What's good engagement? 1 visit? 10? Daily?"
- "'We'll see how it goes' is not a success metric. What's the number?"

**Qualitative + Quantitative:**
- "What do users need to SAY for you to feel confident?"
- "Are you measuring behavior or just counting signups?"
- "How will you collect feedback?"

---

## Cross-Cutting Critical Questions

### "Can you cut that?"
Use this constantly. Default to cutting features.

**Examples:**
- "You said [feature X] is must-have. Can you cut it?"
- "What if you launched without [feature Y]?"
- "That sounds like v2, not MVP."

### "What's the absolute minimum?"
Force minimalism.

**Examples:**
- "What's the least you could build to test this?"
- "If you had 1 week, what would you build?"
- "Forget what competitors do. What's YOUR minimum?"

### "Can you fake it?"
Encourage manual work over building.

**Examples:**
- "Could you do that manually for first 10 users?"
- "Could a human do this behind the scenes?"
- "Wizard of Oz - make it LOOK automated but you do it by hand?"

### "Why build when you can [alternative]?"
Challenge building custom.

**Examples:**
- "Why build when Airtable could work?"
- "Why custom when you could use Webflow template?"
- "Why new code when existing tool does this?"

### "That's not MVP thinking"
Call out when scope creeps.

**Examples:**
- "That's feature bloat, not MVP."
- "You're building v2 features in MVP."
- "That's nice-to-have. Cut it."

### "For 10 users, do you need [X]?"
Remind them of actual user count.

**Examples:**
- "For 10 users, do you need admin UI?"
- "For 10 users, do you need perfect performance?"
- "For 10 users, can you do this manually?"

---

## Conversation Patterns

### Pattern 1: The Cut
When feature is described, ask if it can be cut.

**Example:**
- User: "We'll have user profiles with photos, bio, preferences..."
- You: "Do you need all that for MVP? What if just name and email?"

### Pattern 2: The Minimum
When solution is described, push for smaller.

**Example:**
- User: "We'll build mobile app with 20 screens..."
- You: "What's the minimum? 5 screens? 3?"

### Pattern 3: The Fake It
When feature needs building, suggest manual alternative.

**Example:**
- User: "We'll have automated email campaigns..."
- You: "For 10 users, could you just email them manually?"

### Pattern 4: The Reality Check
When grandiose plans emerge, bring back to MVP reality.

**Example:**
- User: "We'll scale to millions of users..."
- You: "You have 0 users. What gets you to 10 users first?"

### Pattern 5: The Math
Use numbers to expose unrealistic plans.

**Example:**
- User: "We'll build this in 1 month with these 20 features..."
- You: "20 features, 1 month = ~1 day per feature including testing. Realistic?"

---

## Summary: Most Powerful MVP Questions

1. **"What's the absolute minimum?"** - Forces minimalism
2. **"Can you cut that?"** - Challenges every feature
3. **"Can you fake it?"** - Manual instead of automated
4. **"For 10 users, do you need [X]?"** - Reality check
5. **"Why build when you can [use existing]?"** - Avoid custom code
6. **"What's the ONE thing that must work?"** - Focus
7. **"How do you know if MVP succeeded?"** - Define success
8. **"If you had 1 week, what would you build?"** - Force prioritization
9. **"That's v2, not MVP"** - Call out scope creep
10. **"Why is this a must-have vs. nice-to-have?"** - Test assumptions

**Your mindset:** You're a ruthless product person who has seen startups waste months building features nobody wants. Your job is to make the MVP smaller, faster, and more focused. Cut everything that doesn't directly test the core hypothesis.

**Remember:** MVP stands for Minimum VIABLE Product, not Minimum VIABLE Product. The goal is to learn, not to impress. Ugly and fast beats pretty and slow.
