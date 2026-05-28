---
name: Affiliate Link Finder
description: Automatically searches for the highest-rated supplement products on Amazon/iHerb and generates affiliate link suggestions whenever a new supplement is added to the database.
---

# Affiliate Link Finder Skill

## Purpose
This skill automates the process of finding optimal product listings and generating affiliate links when supplements are added to the app database.

## Trigger
This skill should be activated whenever:
- A new supplement is being added to `MockSupplementRepository`
- The user requests an affiliate link update for an existing supplement
- Bulk supplement data is being imported

## Workflow

### Step 1: Extract Supplement Information
From the supplement being added, identify:
- **Primary name** (e.g., "Omega-3", "Magnesium Glycinate")
- **Specific form/type** (e.g., "EPA/DHA", "Glycinate", "Citrate")
- **Target dosage range** (if relevant for search)

### Step 2: Web Search Strategy
Perform targeted searches using the `search_web` tool:

#### Amazon Search
```
Query: "{supplement_name} {form} supplement ADHD {dosage}"
Example: "Omega-3 EPA DHA supplement ADHD 1000mg"
```

**Look for:**
- Products with 4+ star ratings
- High review counts (500+)
- "Amazon's Choice" or "Best Seller" badges
- Third-party tested/certified products
- Brands mentioned in search results (Nordic Naturals, NOW Foods, Thorne, etc.)

#### iHerb Search (Alternative/Backup)
```
Query: "{supplement_name} {form} highest rated iHerb"
```

**Look for:**
- iHerb verified reviews
- Products with detailed supplement facts
- Brand reputation indicators

### Step 3: Extract Product Identifiers

#### For Amazon:
- Extract **ASIN** (Amazon Standard Identification Number)
  - Found in URL: `amazon.com/dp/{ASIN}`
  - Example: `B001U4OYGY`
- Extract product title for verification

#### For iHerb:
- Extract **Product ID**
  - Found in URL: `iherb.com/{product-id}`
  - Example: `81332`

### Step 4: Generate Affiliate Links

Use the `AffiliateService` class to generate tagged links:

```dart
// For Amazon
final affiliateService = AffiliateService();

// Single region
final usLink = affiliateService.getTaggedAffiliateLink(
  supplementId: 'B001U4OYGY',  // ASIN from Step 3
  region: UserRegion.us,
);

// All regions
final allLinks = affiliateService.getAllRegionLinks('B001U4OYGY');
```

**Result format:**
```
US:  https://www.amazon.com/dp/B001U4OYGY?tag=adhdsupplements-20
UK:  https://www.amazon.co.uk/dp/B001U4OYGY?tag=adhdsupplements-21
EU:  https://www.amazon.de/dp/B001U4OYGY?tag=adhdsupplements-22
```

#### For iHerb:
```
https://www.iherb.com/{product-id}?rcode=ADHDSUPP
Example: https://www.iherb.com/81332?rcode=ADHDSUPP
```

### Step 5: Present Recommendation

Provide output in this format:

```markdown
## Affiliate Link Suggestion: {Supplement Name}

### Recommended Product
**Title:** {Product Title from Amazon/iHerb}
**Rating:** {Star Rating} ({Review Count} reviews)
**ASIN/ID:** {Identifier}
**Price:** ${Price} (if available)

### Generated Affiliate Links
- **US Amazon:** {US Link}
- **UK Amazon:** {UK Link}
- **EU Amazon:** {EU Link}
- **iHerb:** {iHerb Link} (if applicable)

### Add to Mock Repository
```dart
Supplement(
  id: '{generate-uuid}',
  name: '{Supplement Name}',
  description: '{Brief description}',
  referralUrl: '{US Link}',  // Default to US
  benefits: [...],
  dosageInstruction: '{Dosage}',
  sideEffects: [...],
  focusLevel: {1-5},
)
```

### Notes
- {Any special considerations}
- {Alternative products if primary is unavailable}
```

## Example Execution

**User Input:**
"Add L-Tyrosine supplement to the database"

**Agent Actions:**
1. Search: "L-Tyrosine supplement ADHD 500mg amazon"
2. Identify top product: "NOW Foods L-Tyrosine 500mg"
3. Extract ASIN: `B0013OQGO6`
4. Generate links using `AffiliateService`
5. Present recommendation (see format above)

## Edge Cases

### No Amazon Listing Found
- Fall back to iHerb search
- Search for general category: "{supplement_name} best brand reddit"
- Suggest manual research with specific brand recommendations

### Multiple Strong Candidates
- Present top 3 options ranked by:
  1. Rating × Review Count score
  2. Price per serving
  3. Third-party certification (USP, NSF, ConsumerLab)

### International Availability Issues
- Note if product unavailable in UK/EU
- Suggest region-specific alternatives
- Update affiliate link map accordingly

## Quality Checks

Before finalizing recommendation:
- [ ] ASIN/Product ID is valid
- [ ] Product matches supplement specification (name, form, dosage)
- [ ] Rating ≥ 4.0 stars
- [ ] Review count ≥ 100 (or note if lower)
- [ ] Affiliate tag is correctly formatted
- [ ] Link opens to correct product page

## Maintenance

This skill should be reviewed quarterly to:
- Update affiliate tag IDs if changed
- Verify top-rated products are still available
- Add new platforms (e.g., Fullscript, Wellevate)
- Refine search queries based on accuracy
