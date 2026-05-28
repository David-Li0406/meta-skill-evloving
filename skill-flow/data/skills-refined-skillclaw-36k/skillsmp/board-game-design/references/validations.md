# Board Game Design - Validations

## Ambiguous Modal Verbs in Rules

### **Id**
bgd-ambiguous-may-vs-must
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(can|could|might|should)\b(?!.*\b(must|cannot|may not)\b)
### **Message**
Ambiguous modal verb detected. 'Can' implies ability, 'may' implies permission, 'must' implies requirement. Be explicit.
### **Fix Action**
Replace 'can' with 'may' for permission or 'must' for requirements. Avoid 'should' - rules are not suggestions.
### **Applies To**
  - *.md
  - *.txt
  - *rulebook*
  - *rules*

## Passive Voice in Critical Rules

### **Id**
bgd-passive-voice-rules
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(is|are|was|were|been|being)\s+(moved|placed|taken|drawn|discarded|removed|added|gained|lost)\b
### **Message**
Passive voice makes rules ambiguous. Who performs the action?
### **Fix Action**
Use active voice: 'The active player draws' not 'Cards are drawn'
### **Applies To**
  - *.md
  - *.txt
  - *rulebook*
  - *rules*

## Undefined Game Term Reference

### **Id**
bgd-undefined-game-term
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(the\s+(?:token|marker|tile|card|die|dice|meeple|resource))\b(?!.*(?:glossary|definition|see))
### **Message**
Generic component term without definition. Which specific token/marker/card?
### **Fix Action**
Use specific named terms defined in component list (e.g., 'Victory Point token', 'Action card')
### **Applies To**
  - *rulebook*
  - *rules*

## Missing Exception or Edge Case Handling

### **Id**
bgd-missing-exception-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(always|never|every|all)\s+(?:player|card|token|action)
### **Message**
Absolute terms often have exceptions. What happens in edge cases?
### **Fix Action**
Add explicit exception handling: 'All players EXCEPT the active player...' or 'Every action UNLESS...'
### **Applies To**
  - *rulebook*
  - *rules*

## Circular Rule Reference

### **Id**
bgd-circular-reference
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \(see\s+(?:section|rule|page)\s+\d+\).*\(see\s+(?:section|rule|page)\s+\d+\)
### **Message**
Multiple cross-references may create circular navigation. Player should not need to flip constantly.
### **Fix Action**
Inline simple rules. Use appendix for complex interactions. Minimize cross-references.
### **Applies To**
  - *rulebook*
  - *rules*

## Inconsistent Terminology Usage

### **Id**
bgd-inconsistent-terminology
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(victory\s*point|VP|point|score)\b.*\b(victory\s*point|VP|point|score)\b
### **Message**
Multiple terms for same concept detected. Use consistent terminology throughout.
### **Fix Action**
Choose one term (e.g., 'Victory Points' or 'VP') and use it exclusively. Define on first use.
### **Applies To**
  - *rulebook*
  - *rules*

## Missing Turn Structure Section

### **Id**
bgd-missing-turn-structure
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:turn|round|phase|action)\s+(?:structure|sequence|order|overview))
### **Message**
No clear turn structure section found. Players need explicit turn sequence.
### **Fix Action**
Add 'Turn Structure' or 'Round Sequence' section early in rulebook with numbered steps.
### **Applies To**
  - *rulebook*
  - *rules*

## Missing Player Count Specification

### **Id**
bgd-missing-player-count
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:player|players)\s*(?:count|number)?:?\s*\d)
### **Message**
Player count not specified. Every design document needs explicit player count range.
### **Fix Action**
Add player count specification: 'Players: 2-4' or 'Player Count: 3-5 (best at 4)'
### **Applies To**
  - *design*
  - *gdd*
  - *concept*

## Missing Play Time Estimate

### **Id**
bgd-missing-play-time
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:play\s*time|duration|length|minutes))
### **Message**
Play time not specified. Include estimated duration.
### **Fix Action**
Add play time estimate: 'Play Time: 60-90 minutes' or 'Duration: 30 min/player'
### **Applies To**
  - *design*
  - *gdd*
  - *concept*

## Missing Core Loop Description

### **Id**
bgd-missing-core-loop
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:core\s*loop|main\s*mechanic|primary\s*mechanic|central\s*mechanic))
### **Message**
No core loop described. What do players DO on each turn?
### **Fix Action**
Add 'Core Loop' section: 'On your turn: 1. Draw cards 2. Play actions 3. Score points'
### **Applies To**
  - *design*
  - *gdd*
  - *concept*

## Missing Victory Condition

### **Id**
bgd-missing-victory-condition
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*(?:win|victory|winning|end\s*game|game\s*end|score|scoring))
### **Message**
No victory condition described. How does the game end? How is the winner determined?
### **Fix Action**
Add clear victory condition: 'The game ends when X. The player with most points wins.'
### **Applies To**
  - *design*
  - *gdd*
  - *concept*

## Component Without Cost Estimate

### **Id**
bgd-uncosted-component
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(miniature|custom\s*dice|custom\s*meeple|insert|metal\s*coin)\b(?!.*\$)
### **Message**
Custom component mentioned without cost consideration. These are expensive!
### **Fix Action**
Add cost estimate or alternative: 'Custom meeples (~$0.30/ea) or standard cubes ($0.03/ea)'
### **Applies To**
  - *design*
  - *gdd*
  - *component*

## Balance Claim Without Testing Evidence

### **Id**
bgd-untested-claim
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(balanced|fair|equal|even)\b(?!.*(?:playtest|tested|test\s*result|game\s*\d+))
### **Message**
Balance claim without testing evidence. How do you know it's balanced?
### **Fix Action**
Add testing data: 'Balanced across 20 playtests - win rate: Player 1 (48%), Player 2 (52%)'
### **Applies To**
  - *design*
  - *balance*
  - *notes*

## Missing Playtest Tracking

### **Id**
bgd-missing-playtest-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \bplaytest\b(?!.*(?:date|player|count|version|result|note))
### **Message**
Playtest mentioned without structured tracking. Document systematically.
### **Fix Action**
Use playtest log: Date, Version, Players, Count, Duration, Issues Found, Changes Made
### **Applies To**
  - *playtest*
  - *notes*
  - *log*

## Asymmetric Elements Without Balance Testing

### **Id**
bgd-asymmetric-untested
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(faction|asymmetric|unique\s*power|variable\s*power)\b(?!.*(?:win\s*rate|balance|tested|playtest\s*\d+))
### **Message**
Asymmetric element without documented balance testing. Each faction needs win rate data.
### **Fix Action**
Track win rates per faction: 'Faction A: 47% (23 games), Faction B: 51% (23 games)...'
### **Applies To**
  - *design*
  - *balance*
  - *faction*

## Component Missing Dimensions

### **Id**
bgd-component-missing-dimensions
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(board|card|token|tile|box)\b(?!.*(?:mm|cm|inch|"|x\s*\d))
### **Message**
Component mentioned without dimensions. Manufacturers need exact sizes.
### **Fix Action**
Add dimensions: 'Cards: 63mm x 88mm (poker size)' or 'Board: 18" x 18" (folded 9x18)'
### **Applies To**
  - *component*
  - *spec*
  - *manufacturing*

## Component Missing Quantity

### **Id**
bgd-component-missing-quantity
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(card|token|die|dice|meeple|tile|cube|disc)\b(?!.*(?:\d+\s*(?:x|each|per|total)|quantity))
### **Message**
Component type without quantity. How many of each?
### **Fix Action**
Specify quantities: 'Resource cubes: 50 (10 each in 5 colors)'
### **Applies To**
  - *component*
  - *spec*
  - *manufacturing*

## Component Missing Material Specification

### **Id**
bgd-component-missing-material
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(token|meeple|cube|disc|marker)\b(?!.*(?:wood|plastic|cardboard|metal|acrylic))
### **Message**
Component without material specification. Wood? Plastic? Cardboard?
### **Fix Action**
Specify material: 'Worker meeples: wood, natural finish, 16mm'
### **Applies To**
  - *component*
  - *spec*
  - *manufacturing*

## Kickstarter Missing Risks Section

### **Id**
bgd-kickstarter-missing-risks
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(kickstarter|crowdfunding|campaign)\b(?!.*(?:risk|challenge|delay|contingency))
### **Message**
Crowdfunding content without risks acknowledgment. Backers expect transparency.
### **Fix Action**
Add risks section: manufacturing delays, shipping challenges, currency fluctuation, etc.
### **Applies To**
  - *kickstarter*
  - *campaign*

## Stretch Goal Without Cost Analysis

### **Id**
bgd-stretch-goal-uncasted
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(stretch\s*goal|unlock)\b(?!.*\$)
### **Message**
Stretch goal without cost analysis. Each unlock increases production cost.
### **Fix Action**
Add cost impact: 'Metal coins ($2.50/unit increase, unlocks at $X when margin covers)'
### **Applies To**
  - *kickstarter*
  - *campaign*
  - *stretch*

## Potentially Unrealistic Timeline

### **Id**
bgd-timeline-unrealistic
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - deliver.*(?:2|3)\s*months?(?:\s*after|from)
### **Message**
Timeline appears aggressive. Manufacturing + shipping typically takes 4-6 months minimum.
### **Fix Action**
Verify timeline: Manufacturing (90-120 days) + Shipping (45-90 days) + Fulfillment (2-4 weeks)
### **Applies To**
  - *kickstarter*
  - *campaign*
  - *timeline*

## Color-Only Component Differentiation

### **Id**
bgd-color-only-differentiation
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(red|blue|green|yellow|purple|orange)\s+(player|token|cube|meeple|piece)\b(?!.*(?:symbol|shape|pattern|icon))
### **Message**
Components differentiated only by color. Colorblind players cannot distinguish.
### **Fix Action**
Add shape/symbol/pattern differentiation. Use colorblind-friendly palette testing.
### **Applies To**
  - *component*
  - *design*
  - *rulebook*

## Small Text Size Warning

### **Id**
bgd-small-text-warning
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(8\s*pt|9\s*pt|7\s*pt|6\s*pt)\b
### **Message**
Text size below 10pt is difficult to read for many players.
### **Fix Action**
Use minimum 10pt font on cards, 9pt for minor flavor text only
### **Applies To**
  - *component*
  - *spec*
  - *layout*

## Assumed Fine Motor Dexterity

### **Id**
bgd-dexterity-assumption
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \b(stack|flick|balance|precision|careful)\b(?!.*(?:optional|alternative))
### **Message**
Mechanic may require fine motor skills. Consider accessibility alternatives.
### **Fix Action**
Provide alternatives for dexterity elements or note in player guidance
### **Applies To**
  - *design*
  - *rulebook*