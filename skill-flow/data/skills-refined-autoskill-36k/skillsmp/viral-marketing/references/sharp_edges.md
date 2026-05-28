# Viral Marketing - Sharp Edges

## Spam Guilt Association

### **Id**
spam-guilt-association
### **Summary**
Making users unknowingly spam their contacts
### **Severity**
critical
### **Situation**
  Auto-posting to social without clear consent. "Invite all" that blasts everyone.
  Users don't realize what they've done until friends complain.
  
### **Why**
  Users feel betrayed when they realize what happened. They never trust you again.
  They tell others not to trust you. Your brand becomes associated with spam.
  LinkedIn's early growth tactics still haunt them.
  
### **Solution**
  - Make every share action explicit and opt-in
  - Show users exactly what will be sent before sending
  - Never auto-select contacts
  - Let users customize messages
  - Treat their relationships with more respect than they might themselves
  
### **Symptoms**
  - User complaints about spam
  - "I didn't mean to send that" messages
  - Trust damage
  - Brand association with spam
### **Detection Pattern**


## Reward Mismatch

### **Id**
reward-mismatch
### **Summary**
Offering rewards that attract wrong users
### **Severity**
critical
### **Situation**
  "$20 for every friend who signs up" attracts reward hunters, not real users.
  Incentivizing signups without engagement.
  
### **Why**
  You pay to acquire users who never engage. Unit economics collapse.
  Real customers outnumbered by fraudsters. CAC skyrockets while LTV stays flat.
  
### **Solution**
  - Reward activation, not signup
  - Gate rewards behind real usage
  - Cap rewards per referrer
  - Use two-sided incentives (referrer + referee both benefit)
  - Monitor for fraud patterns aggressively
  
### **Symptoms**
  - High signup, low activation
  - Referral fraud patterns
  - Terrible unit economics
  - Users disappear after reward
### **Detection Pattern**


## False Viral Metrics

### **Id**
false-viral-metrics
### **Summary**
Celebrating K-factor calculated wrong
### **Severity**
high
### **Situation**
  Counting invites sent, not invites that converted. Ignoring cycle time.
  Thinking you're growing virally when you're not.
  
### **Why**
  You make strategic decisions based on false growth.
  Eventually reality catches up—no hockey stick, just expensive acquisition.
  
### **Solution**
  - Calculate K-factor correctly: (invites per user) × (conversion rate)
  - Include cycle time—K=0.8 with 1-day cycle beats K=1.1 with 30-day cycle
  - Distinguish true viral growth from referral attribution
  - Track cohorts over time, not just snapshots
  
### **Symptoms**
  - K-factor looks good, growth doesn't follow
  - Confusion about viral vs paid growth
  - Optimizing wrong metrics
  - Hockey stick never materializes
### **Detection Pattern**


## Incentivizing Non Sharers

### **Id**
incentivizing-non-sharers
### **Summary**
Building referral programs for products people don't naturally talk about
### **Severity**
high
### **Situation**
  Trying to make toilet paper viral. Building referral programs for products
  no one discusses. If people don't already share, incentives won't help.
  
### **Why**
  Nobody shares, no matter the incentive. You waste budget on a program
  that generates nothing. Virality amplifies existing sharing—it can't create it.
  
### **Solution**
  Before building referral mechanics, ask:
  "Do people already talk about this product?"
  If no, fix the product first.
  
  # Products that naturally spread:
  - Remarkable experiences
  - Social identity signals
  - Collaborative tools (network effects)
  - Shareable content
  
  # Products that don't:
  - Commodities
  - Embarrassing products
  - Low-engagement utilities
  
### **Symptoms**
  - Referral program unused
  - Low share rates despite incentives
  - No organic word-of-mouth
  - Incentives don't move the needle
### **Detection Pattern**


## Single Channel Dependency

### **Id**
single-channel-dependency
### **Summary**
Building viral strategy around one platform that can change
### **Severity**
high
### **Situation**
  Entire viral strategy built on Facebook shares or WhatsApp forwards.
  Platform changes algorithm—growth dies overnight.
  
### **Why**
  Platform changes algorithm—growth dies overnight.
  Platform blocks your share mechanism—you're done.
  You've built on rented land.
  
### **Solution**
  - Diversify share channels from the start
  - Build owned channels (email, SMS, direct links) alongside platform-dependent ones
  - Design sharing to work even if specific platforms disappear
  - Don't over-optimize for one platform's mechanics
  
### **Symptoms**
  - 90%+ referrals from one platform
  - Growth swings with algorithm changes
  - No owned channels
  - Platform dependency risk
### **Detection Pattern**


## Friction Overcorrection

### **Id**
friction-overcorrection
### **Summary**
Making sharing so easy people do it accidentally
### **Severity**
medium
### **Situation**
  One-click shares that people don't remember making.
  No confirmation, no preview. Volume over quality.
  
### **Why**
  Accidental shares embarrass users. They feel tricked.
  Low-intent shares don't convert anyway.
  You get volume without quality—and damage trust.
  
### **Solution**
  - Confirm before sending
  - Show preview of what will be shared
  - Let users personalize
  - A moment of friction that creates intent produces higher-quality shares
  
  # The right friction:
  Zero friction → Accidental, low quality
  Tiny friction (preview + confirm) → Intentional, high quality
  
### **Symptoms**
  - Shares that don't convert
  - Users surprised by their shares
  - I didn't mean to share that
  - High volume, low quality
### **Detection Pattern**


## Referrer Reward Only

### **Id**
referrer-reward-only
### **Summary**
Only incentivizing the referrer, not the referee
### **Severity**
high
### **Situation**
  "You get $10 when your friend signs up."
  The friend has no reason to use your referral link vs signing up directly.
  
### **Why**
  The referee has no reason to use your link vs. signing up directly.
  They might resent that their friend is getting paid off them.
  Conversion tanks.
  
### **Solution**
  Always use two-sided incentives.
  The referee should get something—preferably something better than referrer.
  
  # Better framing:
  "Your friend gets $20, and you get $10 when they join."
  The referee is the priority.
  
  # Two-sided examples:
  - Friend gets 50% off, you get free month
  - Friend gets extended trial, you get credits
  - Both get bonuses
  
### **Symptoms**
  - Low referral link usage
  - Direct signups instead of referrals
  - Referee resentment
  - Poor conversion on referred users
### **Detection Pattern**


## Timing Ignorance

### **Id**
timing-ignorance
### **Summary**
Asking for referrals at the wrong moment
### **Severity**
high
### **Situation**
  Hitting new users with "Invite friends!" before they've experienced value.
  Maximum exposure to referral prompts, minimum results.
  
### **Why**
  Users don't know if your product is good yet. They're not going to recommend
  something they haven't validated. You train them to ignore referral prompts.
  
### **Solution**
  Ask for referrals after moment of delight:
  - After successful transaction
  - After achieving a goal
  - After positive experience
  - When they're feeling good about you
  
  # Best timing:
  "Congrats on [achievement]! Know anyone else who'd benefit?"
  
  # Worst timing:
  "Welcome! Invite 5 friends to continue"
  
### **Symptoms**
  - Low share rates on prompts
  - Users ignore referral requests
  - Prompts feel pushy
  - No correlation between satisfaction and sharing
### **Detection Pattern**


## Vanity Sharing

### **Id**
vanity-sharing
### **Summary**
Adding share buttons for content nobody would share
### **Severity**
medium
### **Situation**
  "Share this terms of service update!"
  Share buttons on every page regardless of share-worthiness.
  (0 shares displayed)
  
### **Why**
  Unused share buttons look pathetic. Clutter the interface.
  Train users that your share prompts are irrelevant.
  When you have something actually share-worthy, they ignore it.
  
### **Solution**
  Only add share mechanics to genuinely share-worthy content.
  Ask: "Would I share this?" If no, don't add the button.
  Make sharing rare and valuable, not ubiquitous and ignored.
  
  # Share-worthy content:
  - Useful resources
  - Interesting findings
  - Entertainment value
  - Social identity signal
  
  # Not share-worthy:
  - Terms of service
  - Basic product pages
  - Boring updates
  
### **Symptoms**
  - 0 shares displayed on buttons
  - Share buttons everywhere, used nowhere
  - Interface clutter
  - Users tune out share prompts
### **Detection Pattern**


## Forced Virality

### **Id**
forced-virality
### **Summary**
Making the product unusable without inviting others
### **Severity**
critical
### **Situation**
  Forcing shares to unlock features. Gating core functionality behind referrals.
  "Invite 5 friends to continue using the app."
  
### **Why**
  Users resent being forced. They spam their contacts with angry apologies.
  They churn immediately. The shares are hostile, not enthusiastic.
  You might get K>1 but terrible retention.
  
### **Solution**
  Sharing should be natural and valuable, never forced.
  The product should work alone; sharing should make it better.
  Users share because they want to, not because they have to.
  
  # Natural virality:
  - Collaborative features (need others to use)
  - Shared outputs (content worth sharing)
  - Social identity (proud to be associated)
  
  # Forced virality (never works):
  - Gate features behind invites
  - Require shares to proceed
  - Punishment for not sharing
  
### **Symptoms**
  - Hostile referrals
  - High churn after forced shares
  - Negative brand sentiment
  - Fake/throwaway invites
### **Detection Pattern**


## Referral Fraud Blindness

### **Id**
referral-fraud-blindness
### **Summary**
Not building fraud detection into referral programs
### **Severity**
critical
### **Situation**
  No fraud detection. Getting exploited by fake accounts, self-referrals,
  and organized fraud rings within days of launch.
  
### **Why**
  Fraudsters find your program within days. They extract thousands in rewards.
  Your economics collapse. By the time you notice, you've paid a fortune for nothing.
  
### **Solution**
  Build fraud detection from day one:
  - Flag same-device referrals
  - Flag same-IP signups
  - Flag rapid referral patterns
  - Delay reward payouts
  - Set per-user caps
  - Monitor for anomalies
  
  Better to miss some legit referrals than to hemorrhage money.
  
### **Symptoms**
  - Suspicious referral patterns
  - Same people referring each other
  - Burst activity from single sources
  - Economics don't make sense
### **Detection Pattern**


## Message Control Overreach

### **Id**
message-control-overreach
### **Summary**
Not letting users customize share messages
### **Severity**
medium
### **Situation**
  Forcing users to use your exact pre-written copy.
  Pre-filled messages that sound corporate and fake.
  
### **Why**
  Pre-written messages are obviously pre-written. They don't sound like the person.
  Recipients ignore or distrust them. The share loses authenticity.
  Personal messages convert 10x better than templated ones.
  
### **Solution**
  - Provide default copy but make it editable
  - Let users write in their own voice
  - Guide, don't control
  - Personal messages convert 10x better than templated
  
  # Good default:
  "[Pre-filled but editable message]"
  User can customize or use as-is
  
  # Bad control:
  "[Fixed message that can't be changed]"
  Feels fake, gets ignored
  
### **Symptoms**
  - Obvious templated shares
  - Low engagement on shared content
  - "Clearly an ad" perception
  - Users avoiding share because of forced copy
### **Detection Pattern**
