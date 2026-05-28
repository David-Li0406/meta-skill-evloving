# Play Store Release Tracks

## Overview

Google Play offers multiple release tracks for different stages of your app's release process. Each track serves a specific purpose and audience.

## Track Types

### 1. Internal Testing Track

**Purpose:** Rapid testing with your team

**Characteristics:**
- **Audience:** Up to 100 internal testers
- **Review time:** None (instant availability)
- **Rollout:** Immediate (100% to all testers)
- **Visibility:** Only invited testers can see and install
- **Version requirements:** Can have lower version code than production

**Best for:**
- Daily/continuous deployment from CI/CD
- QA team testing
- Dogfooding (internal employee usage)
- Quick iteration and bug fixes

**Setup:**
1. Play Console → Release → Testing → Internal testing
2. Create email list of testers
3. Share opt-in URL with team
4. Testers opt-in and can immediately download

**Limitations:**
- Maximum 100 testers
- Updates are immediate (can't schedule)
- No staged rollout option

---

### 2. Closed Testing (Alpha/Beta Tracks)

**Purpose:** Private testing with selected external testers

**Characteristics:**
- **Audience:** Unlimited testers via email lists or Google Groups
- **Review time:** Minimal (typically < 24 hours)
- **Rollout:** Immediate to all testers or staged
- **Visibility:** Only invited testers
- **Version requirements:** Can have lower version code than production

**Best for:**
- Beta tester program
- Customer advisory board testing
- Partner/client testing
- Pre-release validation with real users

**Setup:**
1. Play Console → Release → Testing → Closed testing
2. Create track (e.g., "alpha" or "beta")
3. Add testers:
   - Email list (manual CSV upload)
   - Google Group (automatic membership sync)
4. Share opt-in URL with testers

**Multiple closed tracks:**
You can create multiple closed tracks for different purposes:
- alpha: Early unstable builds
- beta: Stable pre-release builds
- partners: Partner testing
- qa-external: External QA testing

---

### 3. Open Testing (Public Beta)

**Purpose:** Public beta program

**Characteristics:**
- **Audience:** Anyone with the opt-in link
- **Review time:** Standard review (1-7 days typically)
- **Rollout:** Configurable (staged or full)
- **Visibility:** Discoverable in Play Store (with limitations)
- **Version requirements:** Must be higher than production

**Best for:**
- Public beta program
- Early adopter community
- Gathering feedback before production
- Testing at scale

**Setup:**
1. Play Console → Release → Testing → Open testing
2. Configure:
   - Countries (where beta is available)
   - Maximum testers (optional limit)
   - Feedback settings
3. Publish opt-in URL or Play Store listing link

**Considerations:**
- Wider audience = more diverse feedback
- Can impact app ratings if buggy
- Higher review scrutiny than closed testing
- Beta users see "Early Access" badge

---

### 4. Production Track

**Purpose:** Public release to all users

**Characteristics:**
- **Audience:** All users in selected countries
- **Review time:** Standard review (1-7 days, can be longer)
- **Rollout:** Configurable (staged rollout recommended)
- **Visibility:** Fully visible in Play Store
- **Version requirements:** Must be higher than previous production

**Best for:**
- Official public releases
- App updates for all users
- Final release after testing phases

**Staged Rollout Options:**
- **5% → 10% → 20% → 50% → 100%** (recommended)
- Pause at any stage if issues detected
- Gradually increase to monitor stability
- Full rollback available if needed

**Review factors:**
- App content and policies
- Metadata and store listing
- Previous policy violations (if any)
- Random extended reviews sometimes occur

---

## Release Workflow

### Recommended Flow

```
Development
    ↓
Internal Testing (continuous, every commit)
    ↓
Closed Testing / Alpha (weekly releases)
    ↓
Open Testing / Beta (bi-weekly releases)
    ↓
Production (monthly major releases)
```

### Alternative Flow (Simpler)

```
Development
    ↓
Internal Testing (daily/continuous)
    ↓
Production with Staged Rollout (weekly/bi-weekly)
```

### Hotfix Flow

```
Critical Bug Detected
    ↓
Fix in Development
    ↓
Internal Testing (verify fix)
    ↓
Production with Fast Rollout (20% → 50% → 100%)
```

---

## Track Promotion

### Promoting Between Tracks

You can promote a release from one track to another without rebuilding:

**In Play Console:**
1. Navigate to: Release → [Source Track] → Releases
2. Find the release to promote
3. Click "Promote release"
4. Select target track
5. Update release notes if needed
6. Click "Review release"
7. Submit

**Benefits:**
- Same exact APK/AAB (no rebuild needed)
- Saves time and ensures consistency
- Keeps version code sequential

**Promotion Paths:**
- Internal → Alpha → Beta → Production
- Internal → Production (skip beta)
- Alpha → Production (skip beta)

**Restrictions:**
- Cannot promote to track with higher version code already
- Cannot promote from production to testing tracks

---

## Version Code Strategy

### Option 1: Continuous Versioning (Recommended)

All tracks use sequential version codes:

```
1 → Internal
2 → Internal
3 → Alpha
4 → Internal
5 → Alpha
6 → Beta
7 → Production
8 → Internal
...
```

**Pros:**
- Simple and clear
- Easy to track
- No mental overhead

**Cons:**
- Version numbers increase quickly
- Can't easily tell track from version code

### Option 2: Track-Based Versioning

Different ranges for different tracks:

```
Internal:  1000-1999 (e.g., 1001, 1002, 1003)
Alpha:     2000-2999 (e.g., 2001, 2002)
Beta:      3000-3999 (e.g., 3001, 3002)
Production: 1-999    (e.g., 1, 2, 3)
```

**Pros:**
- Can tell track from version code
- Organized by track

**Cons:**
- More complex to manage
- Promotion requires version code bump
- Can run out of range

### Option 3: Semantic Versioning Encoded

Encode semantic version in version code:

```
Version 1.2.3 = 10203 (Major.Minor.Patch)
Version 2.0.0 = 20000
Version 2.1.5 = 20105
```

**Pros:**
- Version code matches version name
- Clear relationship

**Cons:**
- Limited to 2.1.4.7 (max version code is 2100000000)
- Must update both version code and name together

---

## Release Notes Per Track

Different tracks can have different release notes:

**Internal Testing:**
```
- Fixed crash in user profile
- Updated API endpoints
- Added logging for debugging
```
(Can be technical for internal team)

**Production:**
```
- Improved app stability
- Enhanced user profile experience
- Performance optimizations
```
(User-friendly language)

---

## Best Practices

### 1. Use Internal Testing for CI/CD
- Deploy every commit or daily
- Catch issues early
- Team always has latest version

### 2. Beta Test Before Production
- Minimum 1 week in beta
- Monitor crash rates and reviews
- Fix issues before production

### 3. Use Staged Rollout for Production
- Start with 5-10%
- Monitor for 24-48 hours
- Increase gradually
- Pause if issues detected

### 4. Keep Testers Engaged
- Thank beta testers publicly
- Respond to feedback
- Share roadmap updates
- Offer early access to features

### 5. Monitor Metrics
- Crash-free rate per track
- ANR (App Not Responding) rate
- User feedback and ratings
- Install/uninstall rates

---

## Track Comparison Table

| Feature | Internal | Closed | Open | Production |
|---------|----------|--------|------|------------|
| Max Testers | 100 | Unlimited | Unlimited | Unlimited |
| Review Time | None | < 1 day | 1-7 days | 1-7 days |
| Staged Rollout | No | Optional | Yes | Yes |
| Public Visibility | No | No | Limited | Yes |
| Feedback Channel | Email | In-app | In-app + Reviews | Reviews |
| Minimum Updates | Immediate | Hours | Days | Days |

---

## Troubleshooting

**"Cannot create closed track"**
- Ensure app has been published once
- Check permissions (need release manager role)

**"Testers not receiving updates"**
- Verify testers opted in via link
- Check email list is correct
- Internal track: max 100 testers

**"Version code error on promotion"**
- Target track already has higher version code
- Increment version code before promotion

**"Review taking too long"**
- Standard: 1-7 days
- Contact Play Console support after 7 days
- Check for policy violations in email

---

## References

- [Release Tracks Overview](https://support.google.com/googleplay/android-developer/answer/9845334)
- [Testing with Internal Tracks](https://support.google.com/googleplay/android-developer/answer/9303479)
- [Staged Rollouts](https://support.google.com/googleplay/android-developer/answer/6346149)
- [App Review Process](https://support.google.com/googleplay/android-developer/answer/9859455)
