# Website Type-Specific Rules

Different website types (Source Contexts) require different Topical Map configurations, attribute priorities, and content strategies. This guide provides specialized rules for each major website type.

## Table of Contents

### Commercial / Transactional
1. [E-commerce Websites](#e-commerce-websites)
2. [SaaS Websites](#saas-websites)
3. [Marketplace Websites](#marketplace-websites)
4. [Events / Ticketing Websites](#events--ticketing-websites)

### Lead Generation / Local
5. [B2B Service Websites](#b2b-service-websites)
6. [Lead Generation / Local Websites](#lead-generation--local-websites)
7. [Real Estate Websites](#real-estate-websites)
8. [Healthcare Websites](#healthcare-websites)
9. [Hospitality / Travel Websites](#hospitality--travel-websites)

### Content / Informational
10. [Blog/Informational Websites](#bloginformational-websites)
11. [Affiliate / Review Websites](#affiliate--review-websites)
12. [News / Media Websites](#news--media-websites)
13. [Education / Course Websites](#education--course-websites)

### Specialized / Niche
14. [Recruitment / Job Websites](#recruitment--job-websites)
15. [Directory / Listing Websites](#directory--listing-websites)
16. [Community / Forum Websites](#community--forum-websites)
17. [Nonprofit / Charity Websites](#nonprofit--charity-websites)

18. [Comparison Matrix](#comparison-matrix)

---

## E-commerce Websites

E-commerce sites must balance commercial intent with informational depth, handling complex entity attributes (size, color, material).

### Topical Map Configuration

| Component | E-commerce Specification |
|-----------|-------------------------|
| Central Entity | Product category or brand |
| Source Context | Selling products |
| CSI Predicates | buy, compare, choose, find, order |
| Core Section | Product pages, category pages |
| Author Section | Buying guides, comparisons, how-tos |

### Attribute Coverage

Cover products, brands, services, and dimensions:

| Attribute Type | Examples | Priority |
|---------------|----------|----------|
| Transactional | Price, availability, shipping | Highest |
| Specification | Size, weight, material, color | High |
| Comparison | Alternatives, pros/cons | Medium |
| Usage | How to use, maintenance | Medium |
| Trust | Reviews, ratings, warranty | High |

### Content Structure Rules

| Rule | Implementation |
|------|----------------|
| Use LIFT Model | Order: Buy -> Compare -> Reviews -> Statistics |
| Mixed formats | Prose definitions + Tables for specs + Lists for features |
| Social proof | Brand review + Expert review + Customer review |
| Responsiveness | Transactional content above fold |

### Link Structure

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Ontology-based linking | Link "holster" to "nylon material" page | Random category links |
| Limit filter URLs | Curated facet combinations only | Millions of filter URLs |
| Product-to-guide | Products link to buying guides | Orphaned product pages |

### E-commerce Checklist

```
[ ] Product specifications in tables
[ ] Multiple review types present
[ ] Transactional elements above fold
[ ] Category pages have prose introductions
[ ] Filter combinations limited
[ ] Products link to material/brand pages
[ ] Buying guides link to products
```

---

## SaaS Websites

SaaS websites must connect technical products to real-world user needs and search behaviors.

### Topical Map Configuration

| Component | SaaS Specification |
|-----------|-------------------|
| Central Entity | The software product/platform |
| Source Context | Selling software/services |
| CSI Predicates | generate, automate, manage, track, integrate |
| Core Section | Feature pages, pricing, use cases |
| Author Section | Tutorials, industry content, thought leadership |

### Connecting to User Needs

The TM must link the product to external search activities:

| Product | Connected User Needs |
|---------|---------------------|
| Gym Management SaaS | Martial arts, personal trainers, membership tracking |
| Email Marketing Tool | Newsletter templates, subscriber management |
| Project Management | Team collaboration, deadline tracking |

### Template Flexibility

Different features need different attribute priorities:

| Feature Type | Template Configuration |
|--------------|----------------------|
| Core features | Benefits -> Use cases -> How it works |
| Integrations | Compatible tools -> Setup -> Benefits |
| Comparisons | Feature matrix -> Pricing -> Verdict |

### Link Flow Rules

| Rule | Implementation |
|------|----------------|
| Homepage most linked | Service pages link to homepage |
| Feature-to-use-case | Each feature links to relevant use cases |
| CSI predicates in anchors | "generate reports" not "click here" |

### Competitor Intelligence

Use competitor forums and review platforms as attribute sources:

| Source | What to Extract |
|--------|-----------------|
| G2/Capterra reviews | Feature requests, pain points |
| Competitor forums | User questions, common issues |
| Competitor content | Attribute gaps to exploit |

### SaaS Checklist

```
[ ] Product connected to user search behaviors
[ ] Features linked to use cases
[ ] Homepage receives most internal links
[ ] CSI predicates in anchor texts
[ ] Competitor attributes analyzed
[ ] Templates flexible per feature type
[ ] Free trial/demo prominently placed
```

---

## Marketplace Websites

Marketplace sites handle user-generated listings with two-sided networks (buyers and sellers).

### Topical Map Configuration

| Component | Marketplace Specification |
|-----------|--------------------------|
| Central Entity | The item category or marketplace niche |
| Source Context | Facilitating buyer-seller transactions |
| CSI Predicates | buy, sell, list, bid, browse, negotiate |
| Core Section | Category pages, trending listings, seller profiles |
| Author Section | Market insights, selling tips, fraud prevention |

### Two-Sided Content Strategy

Content must serve both buyers and sellers:

| Audience | Content Focus |
|----------|--------------|
| Buyers | Quality guides, price comparisons, how to evaluate |
| Sellers | How to list, pricing strategies, photography tips |
| Both | Category trends, market reports, safety guides |

### Category Taxonomy

| Rule | Implementation |
|------|----------------|
| Deep taxonomy | 3-4 levels of category nesting |
| Faceted search | Filterable attributes per category |
| Category pages | Informational intro + listings + guides |

### Trust & Safety Content

| Content Type | Purpose |
|-------------|---------|
| Seller verification | How verification works, badges meaning |
| Fraud prevention | How to spot scams, safe payment methods |
| Dispute resolution | What to do if problems arise |

### Marketplace Checklist

```
[ ] Category pages have informational introductions
[ ] Seller guides for listing optimization
[ ] Buyer guides for quality evaluation
[ ] Trust/safety content prominent
[ ] Category-specific attribute filters
[ ] Market trend content published regularly
[ ] Seller rating system explained
```

---

## Events / Ticketing Websites

Event sites handle time-bound inventory with urgency signals and performer/venue relationships.

### Topical Map Configuration

| Component | Events Specification |
|-----------|---------------------|
| Central Entity | Event type, performer, or venue |
| Source Context | Selling event access/tickets |
| CSI Predicates | attend, book, experience, discover, see |
| Core Section | Event pages, performer profiles, venue pages |
| Author Section | Event previews, artist news, what-to-expect guides |

### Time-Sensitive Content

| Content Type | Timing Strategy |
|-------------|-----------------|
| Event announcements | Published when tickets go on sale |
| Preview content | 2-4 weeks before event |
| What-to-expect | 1 week before event |
| Reviews/recaps | After event (builds authority for future) |

### Entity Relationships

```
Performer
|---- Past events -> links to -> Venue pages
|---- Genre -> links to -> Similar performers
|---- Upcoming events -> links to -> Ticket pages
```

### Urgency Signals

| Signal | Implementation |
|--------|----------------|
| Availability | "Only X tickets left" |
| Time | Countdown to event |
| Social proof | "X people viewing" |
| Price tiers | Early bird vs. regular pricing |

### Events Checklist

```
[ ] Event pages have structured data (Event schema)
[ ] Performer/artist profiles with discography/history
[ ] Venue pages with amenities, seating charts
[ ] Genre/category pages for discovery
[ ] Past event content for authority building
[ ] Clear urgency signals on ticket pages
[ ] Related events for cross-selling
```

---

## B2B Service Websites

B2B and professional services require extremely high E-A-T signals and structured expertise content.

### Topical Map Configuration

| Component | B2B Specification |
|-----------|------------------|
| Central Entity | The service or expertise area |
| Source Context | Providing professional services |
| CSI Predicates | consult, advise, implement, solve, analyze |
| Core Section | Service pages, case studies, consultations |
| Author Section | Methodology, research, industry insights |

### Expertise Demonstration

| Signal Type | Implementation |
|-------------|----------------|
| Statistics | Original research, data, metrics |
| Research papers | Published studies, white papers |
| Unique definitions | Proprietary frameworks, methodologies |
| Deep expertise | Material science, legal precedents, etc. |

### Content Engineering

| Requirement | Implementation |
|-------------|----------------|
| Scientific style | Objective language, citations |
| Multiple perspectives | User view, expert view, regulatory view |
| Conditional language | "Depends on...", "In cases where..." |
| Expert authors | Named domain experts, credentials shown |

### Contextual Segmentation

Create segments linking related service aspects:

```
Divorce Law Services
|---- Legal Process -> links to -> Psychological Impact
|---- Child Custody -> links to -> Financial Implications
---- Mediation -> links to -> Court Procedures
```

### Trust Signals

| Signal | Implementation |
|--------|----------------|
| Licenses/Certifications | Digitized and displayed |
| Awards | Schema markup + visible display |
| Reviews/Testimonials | Structured data implementation |
| Case studies | Detailed methodology + results |

### B2B Checklist

```
[ ] Expert authors with credentials
[ ] Original research/statistics present
[ ] Multiple perspectives covered
[ ] Methodology documented
[ ] Licenses/awards displayed with schema
[ ] Case studies with metrics
[ ] Service pages link to expertise content
[ ] Semantic HTML for trust elements
```

---

## Lead Generation / Local Websites

Local service businesses focused on generating inquiries, quotes, and appointments.

### Topical Map Configuration

| Component | Lead Gen Specification |
|-----------|----------------------|
| Central Entity | The service category (plumbing, landscaping, etc.) |
| Source Context | Providing local services |
| CSI Predicates | contact, hire, schedule, request, get_quote, book |
| Core Section | Service pages, location pages, pricing guides |
| Author Section | Maintenance tips, seasonal guides, DIY tutorials |

### Location-Based Structure

| Page Type | Purpose |
|-----------|---------|
| Service + Location | "Plumbing Services in Amsterdam" |
| Neighborhood pages | Hyperlocal authority |
| Service area map | Geographic coverage clarity |

### Lead Capture Optimization

| Element | Best Practice |
|---------|--------------|
| Contact forms | Above fold, minimal fields |
| Phone numbers | Click-to-call, tracked |
| Quote requests | Service-specific forms |
| Chat widgets | Immediate response option |

### Local Trust Signals

| Signal | Implementation |
|--------|----------------|
| Google Business Profile | Linked and consistent |
| Local reviews | Google, Yelp displayed |
| Service area | Clear geographic boundaries |
| Response time | "Call back within X hours" |
| Licenses | State/local license numbers |

### Project Galleries

| Content Type | Purpose |
|-------------|---------|
| Before/after | Visual proof of quality |
| Project descriptions | Scope, challenges, solutions |
| Location tags | Geographic relevance |

### Lead Gen Checklist

```
[ ] Service + location pages for all service areas
[ ] Contact forms above fold
[ ] Phone number click-to-call enabled
[ ] Google Business Profile linked
[ ] Local reviews displayed
[ ] License numbers visible
[ ] Project gallery with locations
[ ] Service area clearly defined
[ ] Response time commitment stated
```

---

## Real Estate Websites

Property listing sites for sale or rent with location-based search and lead generation.

### Topical Map Configuration

| Component | Real Estate Specification |
|-----------|--------------------------|
| Central Entity | Property type or neighborhood |
| Source Context | Facilitating property transactions/rentals |
| CSI Predicates | discover, invest, relocate, tour, lease, purchase |
| Core Section | Listings, neighborhood guides, market analysis |
| Author Section | Market trends, investment guides, mortgage tips |

### Property Listing Structure

| Attribute Type | Examples | Priority |
|---------------|----------|----------|
| Core specs | Price, sqft, bedrooms, bathrooms | Highest |
| Location | Address, neighborhood, school district | Highest |
| Features | Amenities, parking, year built | High |
| Financial | HOA fees, taxes, price history | High |
| Lifestyle | Commute times, walkability, nearby | Medium |

### Location Content Strategy

| Content Type | Purpose |
|-------------|---------|
| Neighborhood guides | Local authority, buyer research |
| School district pages | Family buyer segment |
| Market reports | Investment/pricing context |
| Relocation guides | Out-of-area buyer segment |

### Property-to-Location Linking

```
Property Listing
|---- Neighborhood -> links to -> Neighborhood Guide
|---- School district -> links to -> School Info Page
|---- Property type -> links to -> "Buying a Condo" Guide
|---- Price range -> links to -> Market Analysis
```

### Lead Capture for Real Estate

| Action | Implementation |
|--------|----------------|
| Schedule viewing | Calendar integration |
| Request info | Property-specific form |
| Save/favorite | User account feature |
| Price alerts | Notification signup |

### Real Estate Checklist

```
[ ] Property listings have comprehensive specs
[ ] Neighborhood guides for all service areas
[ ] Market analysis/reports published regularly
[ ] School district information included
[ ] Virtual tour/photos prominent
[ ] Price history displayed
[ ] Similar listings shown
[ ] Contact forms on all listings
[ ] Agent/broker profiles with credentials
```

---

## Healthcare Websites

Medical practices with high E-A-T requirements and patient education focus.

### Topical Map Configuration

| Component | Healthcare Specification |
|-----------|------------------------|
| Central Entity | Medical specialty or condition |
| Source Context | Providing medical services |
| CSI Predicates | treat, diagnose, schedule, consult, prevent, learn |
| Core Section | Condition guides, treatments, provider profiles |
| Author Section | Medical research, wellness tips, patient stories |

### YMYL Compliance

Healthcare content requires extra E-A-T signals:

| Requirement | Implementation |
|-------------|----------------|
| Medical review | Content reviewed by licensed MD |
| Author credentials | Board certifications displayed |
| Citations | Link to medical journals, studies |
| Disclaimers | "Consult your doctor" language |
| Last updated | Date of last medical review |

### Condition-Treatment Structure

```
Condition Page
|---- Symptoms -> links to -> Diagnosis Page
|---- Treatments -> links to -> Treatment Option Pages
|---- Providers -> links to -> Specialist Profiles
|---- FAQ -> links to -> Related Conditions
```

### Provider Profiles

| Element | Purpose |
|---------|---------|
| Credentials | Board certifications, education |
| Specialties | Areas of expertise |
| Experience | Years practicing, procedures performed |
| Reviews | Patient testimonials |
| Availability | Booking calendar |

### Patient Education Content

| Content Type | Purpose |
|-------------|---------|
| Condition overviews | Educate before consultation |
| Treatment comparisons | Informed decision-making |
| Post-procedure guides | Recovery support |
| Prevention guides | Wellness/authority building |

### Healthcare Checklist

```
[ ] All content medically reviewed
[ ] Provider credentials prominently displayed
[ ] Citations to medical literature
[ ] Patient testimonials with consent
[ ] Appointment booking integrated
[ ] Insurance information clear
[ ] HIPAA compliance noted
[ ] Condition pages link to treatments
[ ] Last reviewed dates on all medical content
```

---

## Hospitality / Travel Websites

Accommodation and travel sites with real-time availability and booking focus.

### Topical Map Configuration

| Component | Hospitality Specification |
|-----------|-------------------------|
| Central Entity | Property type or destination |
| Source Context | Providing accommodation/travel services |
| CSI Predicates | book, explore, visit, discover, plan, stay |
| Core Section | Property pages, destination guides, booking info |
| Author Section | Travel guides, local tips, seasonal recommendations |

### Property Page Structure

| Attribute Type | Examples | Priority |
|---------------|----------|----------|
| Availability | Real-time calendar, pricing | Highest |
| Accommodations | Room types, capacity, beds | High |
| Amenities | Pool, wifi, breakfast, parking | High |
| Location | Distance to attractions, transport | High |
| Policies | Cancellation, check-in/out | Medium |

### Destination Content Strategy

| Content Type | Purpose |
|-------------|---------|
| Destination guides | Inspire and inform travelers |
| "Things to do" | Activity/attraction content |
| Seasonal guides | When to visit content |
| Local tips | Insider knowledge authority |

### Booking Flow Optimization

| Element | Best Practice |
|---------|--------------|
| Availability calendar | Visual, easy date selection |
| Price transparency | Total cost shown early |
| Urgency signals | "Only X rooms left" |
| Trust signals | Reviews, ratings visible |

### Visual Content Requirements

| Content Type | Standard |
|-------------|----------|
| Property photos | Professional, multiple angles |
| Room photos | Each room type shown |
| Amenity photos | Pool, restaurant, gym |
| Location photos | Nearby attractions |

### Hospitality Checklist

```
[ ] Real-time availability displayed
[ ] Multiple room/property photos
[ ] Amenities clearly listed
[ ] Guest reviews prominent
[ ] Destination guides for all locations
[ ] Clear cancellation policies
[ ] Distance to key attractions shown
[ ] Seasonal pricing/events highlighted
[ ] Mobile booking optimized
```

---

## Blog/Informational Websites

Informational sites must cover entire query networks and prove unique insight beyond summarizing common knowledge.

### Topical Map Configuration

| Component | Blog Specification |
|-----------|-------------------|
| Central Entity | The knowledge domain |
| Source Context | Publishing/informing |
| CSI Predicates | learn, understand, discover, explore |
| Core Section | Main topic clusters |
| Author Section | Related topics, background, tangential |

### Content Justification Rules

| Rule | Implementation |
|------|----------------|
| Query connection required | No pages without query demand |
| Historical data value | AS content must link to CS |
| No dead weight | Unlinked pages dilute authority |

### Template Standards

| Content Type | Template Requirements |
|--------------|----------------------|
| Listicles | Specified predicates (compare, learn, examine) |
| How-to guides | Numbered steps, action verbs |
| Definitions | X is Y format, followed by attributes |
| Comparisons | Table format, consistent criteria |

### Unique Information Gain

You must provide information not found on competitors:

| Strategy | Implementation |
|----------|----------------|
| New entities | Add factors competitors missed |
| New contexts | Different angles on same topic |
| New attributes | Deeper detail than competitors |
| Unique expressions | Distinctive phrases, terminology |

### Bridge Topics

Use bridge topics to connect distant concepts:

| Distant Concepts | Bridge Topic |
|------------------|--------------|
| Swimming styles <-> Pool construction | Pool design considerations |
| Recipe types <-> Kitchen equipment | Equipment needs by cuisine |
| Travel guides <-> Visa requirements | Trip planning overview |

### Blog Checklist

```
[ ] All pages have query demand
[ ] Author Section links to Core Section
[ ] No orphan pages
[ ] Unique information present
[ ] Bridge topics connect clusters
[ ] Consistent templates by content type
[ ] Author vector distinctive
[ ] N-grams unique to site
```

---

## Affiliate / Review Websites

Product reviews and comparisons with commerce-like structure but third-party products.

### Topical Map Configuration

| Component | Affiliate Specification |
|-----------|------------------------|
| Central Entity | Product category |
| Source Context | Reviewing/recommending products |
| CSI Predicates | compare, review, rate, recommend, choose |
| Core Section | Product reviews, comparisons, buying guides |
| Author Section | Industry news, trends, how-to content |

### Review Content Structure

| Section | Purpose |
|---------|---------|
| Verdict summary | Quick answer for scanners |
| Pros/cons | Balanced evaluation |
| Testing methodology | Credibility |
| Alternatives | Comparison context |
| Who it's for | Audience matching |

### Comparison Content

| Format | Use Case |
|--------|----------|
| Tables | Feature-by-feature comparison |
| Prose | Nuanced analysis |
| Rankings | Clear recommendations |
| Use-case segments | "Best for X" sections |

### Trust Requirements

| Signal | Implementation |
|--------|----------------|
| Testing proof | Photos, videos of actual testing |
| Author expertise | Credentials, experience |
| Disclosure | Affiliate relationship stated |
| Update dates | Last tested/updated dates |

### Affiliate Checklist

```
[ ] Clear affiliate disclosure
[ ] Testing methodology explained
[ ] Pros and cons balanced
[ ] Comparison tables present
[ ] Author credentials shown
[ ] Last updated dates visible
[ ] "Best for X" segmentation
[ ] Links to retailer product pages
```

---

## News / Media Websites

Journalism and news with freshness signals and source attribution focus.

### Topical Map Configuration

| Component | News Specification |
|-----------|-------------------|
| Central Entity | News beat or topic area |
| Source Context | Reporting news |
| CSI Predicates | report, investigate, analyze, document, uncover |
| Core Section | Breaking news, investigations, exclusives |
| Author Section | Analysis, opinion, expert interviews |

### Freshness Signals

| Signal | Implementation |
|--------|----------------|
| Publish date | Prominent, ISO format |
| Update log | "Updated X with Y" |
| Breaking badge | For developing stories |
| Archive dating | Clear historical context |

### Source Attribution

| Requirement | Implementation |
|-------------|----------------|
| Named sources | Quote attribution |
| Document links | Primary source linking |
| Source diversity | Multiple perspectives |
| Methodology | How information was obtained |

### Content Tiers

| Tier | Content Type | Freshness |
|------|-------------|-----------|
| Breaking | News as it happens | Hours |
| Daily | Regular coverage | Days |
| Analysis | Deep dives | Weeks |
| Evergreen | Explainers | Months |

### Author Prominence

| Element | Purpose |
|---------|---------|
| Bylines | Every article attributed |
| Author pages | Bio, credentials, archive |
| Beat expertise | Topic specialization |
| Social links | Direct contact/follow |

### News Checklist

```
[ ] Publish dates prominent
[ ] Update logs for developing stories
[ ] Source attribution clear
[ ] Author bylines on all content
[ ] Author pages with credentials
[ ] Breaking news flagged
[ ] Archive properly dated
[ ] Corrections policy linked
```

---

## Education / Course Websites

Online courses and educational content with credential and outcome focus.

### Topical Map Configuration

| Component | Education Specification |
|-----------|------------------------|
| Central Entity | Subject area or skill |
| Source Context | Providing education/training |
| CSI Predicates | learn, enroll, master, upskill, earn, achieve |
| Core Section | Course pages, curriculum, career outcomes |
| Author Section | Industry trends, skill guides, career tips |

### Course Page Structure

| Section | Purpose |
|---------|---------|
| Learning outcomes | What students will achieve |
| Curriculum | Detailed module breakdown |
| Instructor bio | Credibility/expertise |
| Student outcomes | Career results, testimonials |
| Prerequisites | Who this is for |

### Credential Messaging

| Element | Implementation |
|---------|----------------|
| Certification details | What credential is earned |
| Industry recognition | Who accepts this credential |
| Career impact | Salary increase, job placement |
| Credential validity | Expiration, renewal |

### Student Journey Content

| Content Type | Funnel Stage |
|-------------|--------------|
| Topic overviews | Awareness |
| Skill guides | Consideration |
| Course comparisons | Decision |
| Career outcomes | Conversion |
| Alumni success | Retention/referral |

### Learning Path Structure

```
Career Goal
|---- Required skills -> links to -> Course A
|---- Prerequisite knowledge -> links to -> Course B
|---- Certification path -> links to -> Credential Page
```

### Education Checklist

```
[ ] Learning outcomes clearly stated
[ ] Curriculum breakdown detailed
[ ] Instructor credentials displayed
[ ] Student testimonials/outcomes
[ ] Credential value explained
[ ] Career path connections
[ ] Prerequisites stated
[ ] Free preview/trial available
[ ] Completion rates shown
```

---

## Recruitment / Job Websites

Job listings and career resources connecting employers with candidates.

### Topical Map Configuration

| Component | Recruitment Specification |
|-----------|-------------------------|
| Central Entity | Job type or industry |
| Source Context | Connecting employers and candidates |
| CSI Predicates | apply, search, hire, find, advance, grow |
| Core Section | Job listings, company profiles, salary guides |
| Author Section | Career tips, resume guides, interview prep |

### Job Listing Structure

| Attribute | Priority |
|-----------|----------|
| Job title, company | Highest |
| Salary range | Highest |
| Location/remote | High |
| Requirements | High |
| Benefits | Medium |
| Company culture | Medium |

### Two-Sided Content

| Audience | Content Focus |
|----------|--------------|
| Job seekers | Resume tips, interview prep, career paths |
| Employers | Hiring guides, employer branding, recruitment tips |

### Salary Transparency

| Content Type | Purpose |
|-------------|---------|
| Salary ranges | On job listings |
| Salary guides | By role, location, experience |
| Salary calculator | Interactive tool |
| Compensation trends | Industry reports |

### Career Path Content

```
Entry-Level Role
|---- Skills needed -> links to -> Skill Guide
|---- Next role -> links to -> Mid-Level Jobs
|---- Certifications -> links to -> Certification Info
|---- Salary progression -> links to -> Salary Guide
```

### Recruitment Checklist

```
[ ] Salary ranges on listings
[ ] Company profiles complete
[ ] Skill requirements clear
[ ] Remote/location filter
[ ] Career path content
[ ] Resume/interview guides
[ ] Industry salary guides
[ ] Job alert functionality
[ ] Easy apply option
```

---

## Directory / Listing Websites

Aggregated listings and reviews with curation and discovery focus.

### Topical Map Configuration

| Component | Directory Specification |
|-----------|------------------------|
| Central Entity | Entity type (businesses, products, places) |
| Source Context | Curating and organizing information |
| CSI Predicates | discover, compare, find, rank, explore, browse |
| Core Section | Entity pages, category pages, top lists |
| Author Section | Category analysis, methodology, trend reports |

### Listing Page Structure

| Section | Purpose |
|---------|---------|
| Core info | Name, category, location |
| Ratings/reviews | Aggregated feedback |
| Contact details | How to reach |
| Photos | Visual verification |
| Claim/verify | Ownership verification |

### Category Taxonomy

| Level | Example |
|-------|---------|
| Top category | Restaurants |
| Subcategory | Italian Restaurants |
| Location | Italian Restaurants in Amsterdam |
| Attribute | Best Italian Restaurants in Amsterdam |

### Review Aggregation

| Element | Implementation |
|---------|----------------|
| Overall rating | Calculated average |
| Rating breakdown | By criteria |
| Review count | Total reviews shown |
| Recent reviews | Freshness indicator |
| Review sources | If aggregating multiple |

### Top Lists & Rankings

| Content Type | Purpose |
|-------------|---------|
| "Best of" lists | Discovery, high traffic |
| Comparison pages | Decision support |
| Award pages | Authority building |
| Methodology | Ranking credibility |

### Directory Checklist

```
[ ] Consistent listing format
[ ] Clear category taxonomy
[ ] Rating system explained
[ ] Review moderation policy
[ ] Claim/verify process for owners
[ ] "Best of" lists by category
[ ] Methodology page
[ ] Last updated dates
[ ] Photo verification
```

---

## Community / Forum Websites

User discussions and Q&A with community consensus and reputation systems.

### Topical Map Configuration

| Component | Community Specification |
|-----------|------------------------|
| Central Entity | Topic/interest area |
| Source Context | Facilitating community discussion |
| CSI Predicates | ask, answer, discuss, share, help, contribute |
| Core Section | Popular threads, best answers, topic hubs |
| Author Section | Community news, moderator guides, meta discussions |

### Thread/Discussion Structure

| Element | Purpose |
|---------|---------|
| Original question | Clear, searchable |
| Accepted answer | Community-validated solution |
| Related questions | Discovery/context |
| Tags | Categorization |
| Vote count | Quality signal |

### Reputation Systems

| Signal | Implementation |
|--------|----------------|
| User reputation | Points/badges |
| Answer quality | Accept rate, upvotes |
| Expertise areas | Topic-specific reputation |
| Contribution history | Profile visibility |

### Content Quality Signals

| Signal | Implementation |
|--------|----------------|
| Accepted answers | Marked as solution |
| Vote scores | Community validation |
| Expert badges | Verified expertise |
| Moderator highlights | Curated best content |

### Community Guidelines Content

| Content Type | Purpose |
|-------------|---------|
| Rules/guidelines | Behavior expectations |
| FAQ | Common questions answered |
| How to ask | Quality question guidance |
| Moderation policy | Transparency |

### Community Checklist

```
[ ] Clear community guidelines
[ ] Reputation system explained
[ ] Accepted answer feature
[ ] Voting/quality signals
[ ] Topic categorization
[ ] User profiles with history
[ ] Moderator presence visible
[ ] FAQ derived from common questions
[ ] Search functionality
```

---

## Nonprofit / Charity Websites

Mission-driven organizations with impact metrics and transparency focus.

### Topical Map Configuration

| Component | Nonprofit Specification |
|-----------|------------------------|
| Central Entity | The cause or mission |
| Source Context | Advancing a charitable mission |
| CSI Predicates | donate, volunteer, support, help, create_impact |
| Core Section | Mission, programs, impact reports, donation |
| Author Section | Cause updates, beneficiary stories, research |

### Mission Communication

| Element | Purpose |
|---------|---------|
| Mission statement | Clear, compelling why |
| Theory of change | How donations create impact |
| Programs | Specific initiatives |
| Impact metrics | Measurable outcomes |

### Transparency Content

| Content Type | Purpose |
|-------------|---------|
| Financial reports | 990 forms, audits |
| Impact reports | Annual outcome metrics |
| Fund allocation | Where money goes |
| Board information | Governance transparency |

### Donation Experience

| Element | Best Practice |
|---------|--------------|
| Donation amounts | Suggested with impact explanation |
| Recurring option | Monthly giving promoted |
| Impact calculator | "Your $X provides Y" |
| Tax information | Deductibility clear |

### Beneficiary Content

| Content Type | Purpose |
|-------------|---------|
| Impact stories | Emotional connection |
| Before/after | Visible change |
| Beneficiary voice | First-person accounts |
| Program updates | Ongoing progress |

### Volunteer Engagement

| Content Type | Purpose |
|-------------|---------|
| Volunteer opportunities | Available roles |
| Volunteer stories | Social proof |
| Skills-based options | Professional engagement |
| Corporate programs | Business partnerships |

### Nonprofit Checklist

```
[ ] Mission clearly stated
[ ] Impact metrics prominent
[ ] Financial transparency (990, audits)
[ ] Donation process simple
[ ] Impact per dollar explained
[ ] Beneficiary stories shared
[ ] Volunteer opportunities listed
[ ] Board/leadership visible
[ ] Contact for questions available
[ ] Charity ratings linked (GuideStar, Charity Navigator)
```

---

## Comparison Matrix

### Attribute Priority by Type

| Attribute | E-comm | SaaS | B2B | Blog | Lead Gen | Real Estate | Healthcare |
|-----------|--------|------|-----|------|----------|-------------|------------|
| Price | Highest | High | Medium | Low | High | Highest | Medium |
| Location | Low | Low | Medium | Low | Highest | Highest | High |
| Reviews | Highest | High | High | Low | Highest | High | Highest |
| Expertise | Low | Medium | Highest | High | Medium | Low | Highest |
| Availability | High | Medium | Low | Low | High | High | High |
| Credentials | Low | Medium | Highest | Medium | High | Medium | Highest |

### CSI Predicates by Type

| Type | Primary Predicates |
|------|-------------------|
| E-commerce | buy, compare, choose, order |
| SaaS | generate, automate, manage, integrate |
| Marketplace | buy, sell, list, bid, browse |
| Events | attend, book, experience, discover |
| B2B Services | consult, advise, implement, solve |
| Lead Gen | contact, hire, schedule, request |
| Real Estate | discover, invest, tour, lease |
| Healthcare | treat, diagnose, schedule, prevent |
| Hospitality | book, explore, visit, stay |
| Blog | learn, understand, discover, explore |
| Affiliate | compare, review, rate, recommend |
| News | report, investigate, analyze, document |
| Education | learn, enroll, master, upskill |
| Recruitment | apply, search, hire, advance |
| Directory | discover, compare, find, rank |
| Community | ask, answer, discuss, share |
| Nonprofit | donate, volunteer, support, help |

### Trust Signal Priority by Type

| Signal | E-comm | Lead Gen | Healthcare | Nonprofit |
|--------|--------|----------|------------|-----------|
| Reviews | Critical | Critical | Critical | Important |
| Credentials | Optional | Important | Critical | Important |
| Transparency | Optional | Optional | Important | Critical |
| Case studies | Optional | Important | Important | Critical |
| Statistics | Optional | Optional | Important | Critical |

### Content Format by Type

| Format | When to Use |
|--------|-------------|
| Tables | Specs, comparisons, pricing |
| Lists | Features, steps, requirements |
| Prose | Explanations, methodology, stories |
| Calendars | Events, availability, booking |
| Maps | Location-based content |
| Calculators | Pricing, ROI, impact |
