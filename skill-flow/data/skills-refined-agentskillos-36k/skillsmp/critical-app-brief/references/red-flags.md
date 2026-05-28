# Red Flags in MVP Planning

This guide catalogs common warning signs that indicate the "MVP" is actually too big, too complex, or not focused on learning.

---

## Critical Red Flags (Fatal for MVP)

### "We want to build everything"

**Symptoms:**
- 15+ must-have features
- "Users expect all these features"
- "We need feature parity with competitors"

**Why it's fatal:** That's not an MVP, that's a full product. Will take months/years and burn through money before learning anything.

**What to probe:**
- "Which ONE feature tests your hypothesis?"
- "What can you cut and still test the core idea?"
- "Competitors spent years building that. You have weeks. What's YOUR minimum?"

---

### No clear hypothesis being tested

**Symptoms:**
- "We want to validate the idea" (vague)
- Can't articulate what they're testing
- "We'll build it and see if users like it"

**Why it's fatal:** MVP without hypothesis = random building. You won't know what to measure or if you succeeded.

**What to probe:**
- "What specific question must this MVP answer?"
- "If MVP succeeds, what did you learn? If it fails, what did you learn?"
- "Are you testing the problem, solution, or business model?"

---

### Building for imagined future scale

**Symptoms:**
- "We'll need to handle 1M users..."
- Microservices architecture
- Complex distributed systems
- "We need to build it scalable from day 1"

**Why it's fatal:** Premature optimization. Wastes months building for scale that may never come. Delays learning.

**What to probe:**
- "You have 0 users. What gets you to 10 users?"
- "What if you built simple first, scaled if it works?"
- "Why over-engineer before knowing if anyone wants this?"

---

### "6-12 months to MVP"

**Symptoms:**
- Multi-month timeline
- "We'll launch when it's perfect"
- No interim milestones

**Why it's fatal:** That's too long. Competitor ships, market changes, you run out of money. MVP should be weeks, not months.

**What to probe:**
- "What would 6 weeks look like instead?"
- "Can you ship something in 2 weeks to get early feedback?"
- "What's stopping you from releasing iteratively?"

---

### No specific first users identified

**Symptoms:**
- "We'll launch to everyone"
- "We'll find users after we build"
- Can't name 5-10 specific first users

**Why it's fatal:** Building in vacuum. Don't know who to build for. MVP needs specific early users who give feedback.

**What to probe:**
- "Who are your first 10 users? Can you name them?"
- "How will you reach them?"
- "Have you talked to them?"

---

## Serious Red Flags (Major Problems)

### Building authentication from scratch

**Symptoms:**
- "We'll build our own auth system"
- Custom login/signup flows
- Rolling own password hashing

**Why it's risky:** Auth is hard to get right. Security vulnerabilities. Takes time. Auth0/Clerk/Supabase exist.

**What to probe:**
- "Why not use Auth0/Clerk/Supabase?"
- "Have you built secure auth before?"
- "How are you handling password hashing? (better be bcrypt/argon2)"

---

### Perfect design before testing concept

**Symptoms:**
- Spending weeks on design
- "We need beautiful UI"
- Hiring designers before developers

**Why it's risky:** Design doesn't test hypotheses. Ugly MVP can validate problem/solution. Pretty doesn't mean people want it.

**What to probe:**
- "Can you test with ugly-but-functional first?"
- "What if you used basic forms and tested core flow?"
- "Are you designing to learn or designing to impress?"

---

### Building for multiple platforms at once

**Symptoms:**
- "We need iOS AND Android AND web"
- "Users expect native apps"
- Can't pick one platform

**Why it's risky:** 3x the work, 3x the complexity, 3x the time. Pick one, validate, then expand.

**What to probe:**
- "Where do your first users actually spend time?"
- "Can web work first, mobile later?"
- "Why not pick one platform, test, THEN build others?"

---

### Feature list that matches competitors

**Symptoms:**
- "Competitor X has feature Y, so we need it"
- Building feature parity
- Not questioning if features are needed

**Why it's risky:** Competitors took years to build those features. You don't need all of them to test your unique value.

**What to probe:**
- "Competitors have 100 features. Which 3 do YOU need?"
- "What's YOUR unique value? What tests that?"
- "Are you copying features or solving your customer's problem?"

---

### No success metrics defined

**Symptoms:**
- "We'll see how it goes"
- "We'll know if users like it"
- No specific numbers

**Why it's risky:** Can't tell if MVP worked without metrics. Will argue forever about whether to pivot or persevere.

**What to probe:**
- "What number would make you confident this works?"
- "What number would make you shut it down?"
- "How are you measuring success?"

---

### Complex tech stack "to learn"

**Symptoms:**
- "Let's use [bleeding edge framework]"
- "Good opportunity to learn [new tech]"
- Using tech nobody on team knows

**Why it's risky:** Learning tech while building MVP = way slower. Delays learning about product.

**What to probe:**
- "What tech does your team already know?"
- "Why learn new tech while validating idea?"
- "What's fastest, even if boring?"

---

### Building admin tools before having users

**Symptoms:**
- "We need admin dashboard"
- "We need user management UI"
- Building internal tools

**Why it's risky:** For first 10 users, you can manually create accounts, edit database, do admin work by hand.

**What to probe:**
- "For 10 users, can you just edit the database?"
- "Do you need UI or can you do it manually?"
- "Why build admin tools before having users to manage?"

---

## Scope Creep Red Flags

### "While we're at it, let's add..."

**Symptoms:**
- Features keep getting added
- "It's easy, so why not?"
- Scope growing, not shrinking

**Why it's risky:** Classic scope creep. MVP gets bigger and slower. Never ships.

**What to probe:**
- "Is that must-have or nice-to-have?"
- "Does that test your hypothesis?"
- "Can you defer to v2?"

---

### "Users will expect..."

**Symptoms:**
- Adding features based on assumptions
- "Modern apps have [X]"
- "Users won't use it without [Y]"

**Why it's risky:** Assumptions, not validated needs. MVP is for desperate early adopters who tolerate imperfection.

**What to probe:**
- "Have users told you they need this?"
- "What if they use it without this feature?"
- "Can you test that assumption before building?"

---

### Edge case handling

**Symptoms:**
- "What if user does [unlikely thing]?"
- Building flows for rare scenarios
- "We need to handle all cases"

**Why it's risky:** Edge cases take time. For MVP, happy path + manual handling of exceptions is fine.

**What to probe:**
- "How often will that happen?"
- "Can you handle that manually for MVP?"
- "Does that test your core hypothesis?"

---

## Technical Red Flags

### Overengineered architecture

**Symptoms:**
- Microservices
- Event-driven architecture
- Message queues, caching layers, load balancers
- "Building for scale"

**Why it's risky:** Massive overkill for MVP. Takes much longer to build and maintain.

**What to probe:**
- "Do you need that complexity for 10 users?"
- "What's the simplest architecture that works?"
- "Why not monolith for MVP, split later if needed?"

---

### Building what exists as service

**Symptoms:**
- Building auth (Auth0 exists)
- Building payments (Stripe exists)
- Building notifications (SendGrid exists)

**Why it's risky:** Reinventing wheel. Takes time. Managed services are better.

**What to probe:**
- "Why build when [service] exists?"
- "What's the cost of using managed service?"
- "Is building this core to your value prop?"

---

### No-code could work but building custom

**Symptoms:**
- Building CRUD app from scratch
- Simple app that Bubble/Webflow could handle
- Not considering no-code

**Why it's risky:** Could ship in days with no-code instead of weeks/months with custom code.

**What to probe:**
- "Could Bubble/Webflow/Airtable work?"
- "Why custom code vs. no-code for MVP?"
- "What if you tested with no-code first?"

---

### Perfect database design

**Symptoms:**
- Weeks designing schema
- "Need perfect normalization"
- Complex relationships before understanding domain

**Why it's risky:** Premature optimization. Don't know domain well enough yet. Flexible beats perfect for MVP.

**What to probe:**
- "What's minimum data model that works?"
- "Can you use simple schema now, optimize later?"
- "Why spend time optimizing for scale you don't have?"

---

## UX Red Flags

### 20+ screens

**Symptoms:**
- Large screen count
- Separate screens for everything
- Complex navigation

**Why it's risky:** Takes too long to build. Too complex for MVP. Users get lost.

**What to probe:**
- "Can screens be combined?"
- "Do you need [settings/preferences/profile] for MVP?"
- "What's minimum screen count?"

---

### Onboarding flows

**Symptoms:**
- Multi-step onboarding
- Tutorial screens
- "We need to educate users"

**Why it's risky:** Takes time to build. For 10 users, you can onboard manually (call, email, Loom video).

**What to probe:**
- "For first 10 users, can you onboard them personally?"
- "Do you need UI or can you send instructions?"
- "Why build onboarding before knowing if core product works?"

---

### Beautiful design required

**Symptoms:**
- "It needs to look professional"
- "Users won't use ugly apps"
- Weeks on visual design

**Why it's risky:** Pretty doesn't validate hypotheses. Ugly can work for desperate early users.

**What to probe:**
- "Are you testing problem/solution or testing design?"
- "Can you use basic UI library? (Material/Tailwind/Bootstrap)"
- "What if you tested ugly first, prettified later?"

---

## Timeline Red Flags

### No buffer in timeline

**Symptoms:**
- "2 months if everything goes perfectly"
- No contingency
- Assumes no problems

**Why it's risky:** Things ALWAYS take longer. Always.

**What to probe:**
- "What if it takes 2x longer?"
- "What's on critical path?"
- "What could delay you?"

---

### "We'll launch when it's done"

**Symptoms:**
- No hard deadline
- "When it's ready"
- Feature-complete mindset

**Why it's risky:** "Done" never happens. Perfection is enemy of learning.

**What to probe:**
- "What if you released in 2 weeks with less?"
- "What's good enough to test hypothesis?"
- "Can you set hard deadline?"

---

## Cost Red Flags

### No budget

**Symptoms:**
- "We haven't calculated costs"
- "It won't cost much"
- No breakdown

**Why it's risky:** Will run out of money. Surprised by costs.

**What to probe:**
- "What does hosting cost at 10 users? 100? 1000?"
- "What tools/services cost money?"
- "What's total to build + run for 3 months?"

---

### Expensive tools for MVP

**Symptoms:**
- Enterprise tools
- Expensive subscriptions
- Premium services

**Why it's risky:** Burning money before validation. Free/cheap alternatives exist.

**What to probe:**
- "Do you need enterprise tier for 10 users?"
- "What's the free/cheap alternative?"
- "Can you use free tier?"

---

## How to Use These Red Flags

### Severity levels

**🔴 Critical (likely fatal):**
- No hypothesis
- Building everything
- 6-12 month timeline
- Building for imaginary scale

**🟡 Serious (major problems):**
- Multiple platforms
- Perfect design first
- Building auth from scratch
- No success metrics

**🟢 Caution (watch these):**
- Scope creep starting
- Some overengineering
- Admin tools for MVP

### Intervention strategies

**For critical red flags:**
Be very direct. These kill MVPs.

"That's not an MVP. That's a full product. You'll spend a year building features nobody wants. What's the absolute minimum to test if anyone cares?"

**For serious red flags:**
Challenge strongly but offer alternatives.

"Building for iOS AND Android AND web will take 3x longer. Pick one. Which platform are your first 10 users on?"

**For caution flags:**
Point out, suggest simpler, move on if they insist.

"You're adding admin UI before having users. For 10 users you can edit database directly. But if you want to build it, OK."

### Conversation tactics

**1. The Minimum Challenge:**
Constantly push for less.
- "That's 15 features. What's the minimum? 5? 3? 1?"

**2. The Reality Check:**
Remind them of actual user count.
- "For 10 users, do you really need [complex feature]?"

**3. The Alternative:**
Suggest simpler options.
- "Why build when [service/no-code] exists?"

**4. The Math:**
Use numbers to expose problems.
- "20 features × 1 week each = 5 months. Too long for MVP."

**5. The Hypothesis Test:**
Link back to core purpose.
- "Does [feature] test your hypothesis? No? Cut it."

---

## Example Red Flag Conversations

### Example 1: Too Many Features

**User:** "MVP needs profiles, search, filters, messaging, notifications, payments, admin dashboard..."

**You:** "That's 7+ major features. Not an MVP. Which ONE feature, if it works, proves your core idea?"

**User:** "Well, they all work together..."

**You:** "No. If you could build ONE thing this week, what tests your hypothesis?"

**User:** "I guess... messaging?"

**You:** "OK. MVP is basic messaging. Everything else is v2. Can you test your idea with just messaging?"

---

### Example 2: Building for Scale

**User:** "We're using microservices so it scales to millions of users."

**You:** "How many users do you have?"

**User:** "We're pre-launch, but we expect rapid growth..."

**You:** "You have 0 users. Microservices for 0 users? That's massive overengineering."

**User:** "But we want to build it right from the start..."

**You:** "Right' for MVP is fast and simple. Ship monolith, get users, scale IF needed. Why waste months on architecture for users that don't exist?"

---

### Example 3: Perfect Design

**User:** "We're spending 4 weeks on design before coding."

**You:** "Why?"

**User:** "We want it to look professional. Users won't use ugly apps."

**You:** "Are you testing if users want the solution, or testing if they like pretty design?"

**User:** "Both?"

**You:** "Test solution first with ugly-but-functional. If they use ugly version, THEN make it pretty. If they don't, pretty doesn't matter."

---

### Example 4: Long Timeline

**User:** "We'll have MVP ready in 6 months."

**You:** "That's not an MVP timeline. What would 6 WEEKS look like?"

**User:** "We couldn't build everything in 6 weeks..."

**You:** "Exactly. What's the minimum you COULD build in 6 weeks?"

**User:** "I guess just the core flow..."

**You:** "That's your MVP. Not 'everything', just core flow. 6 weeks, not 6 months."

---

## Summary: Top 20 MVP Red Flags

1. **No clear hypothesis** - Don't know what testing
2. **15+ features** - Way too much
3. **6-12 month timeline** - Too long
4. **Building for scale** - Premature optimization
5. **No first users identified** - Building in vacuum
6. **Building auth from scratch** - Use library/service
7. **iOS AND Android AND web** - Pick one
8. **Perfect design first** - Test solution before prettifying
9. **Microservices** - Overkill for MVP
10. **No success metrics** - Can't tell if it worked
11. **Admin tools before users** - Do manually
12. **Learning new tech** - Use what you know
13. **Feature parity with competitors** - You're not them
14. **"Users will expect..."** - Assumptions, not facts
15. **20+ screens** - Too many
16. **No budget** - Will run out of money
17. **Onboarding flows** - Onboard manually
18. **Building what exists as service** - Use Auth0/Stripe/etc
19. **"We'll launch when done"** - Done never comes
20. **Scope creep** - Features keep getting added

When you see these, intervene strongly. Your job is to make the MVP smaller, faster, and more focused on learning.
