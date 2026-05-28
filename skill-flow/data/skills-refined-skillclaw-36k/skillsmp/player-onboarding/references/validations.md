# Player Onboarding - Validations

## Unskippable Tutorial Content

### **Id**
unskippable-tutorial
### **Severity**
error
### **Type**
regex
### **Pattern**
  - skipEnabled.*false|canSkip.*false|allowSkip.*false
  - forceWatch.*true|mandatory.*true|required.*true.*tutorial
### **Message**
Unskippable tutorial detected. Players MUST be able to skip. 30-50% of players will want to skip - if they can't, they quit instead.
### **Fix Action**
Add skipEnabled: true or implement skip button. Remember to grant all rewards/unlocks when skipped.
### **Applies To**
  - *.js
  - *.ts
  - *.yaml
  - *.json

## Tutorial Blocking Core Gameplay

### **Id**
tutorial-before-gameplay
### **Severity**
error
### **Type**
regex
### **Pattern**
  - await.*tutorial.*start.*Game|tutorial\.complete.*then.*startGame
  - if.*!tutorialComplete.*return|!finishedTutorial.*&&.*block
### **Message**
Tutorial blocking gameplay start. Players should be playing within 30 seconds. Integrate teaching INTO gameplay, don't gate on completion.
### **Fix Action**
Move tutorial teaching into first level. Start gameplay immediately, teach during play.
### **Applies To**
  - *.js
  - *.ts

## Too Many Tutorial Steps

### **Id**
excessive-tutorial-steps
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - tutorialStep.*[6-9]|step\s*[>=]\s*[6-9]
  - tutorial\.steps\.length.*>.*5|steps\.push.*steps\.push.*steps\.push.*steps\.push.*steps\.push
### **Message**
6+ tutorial steps detected. Players forget early lessons by step 6. Limit to 4-5 discrete teaching moments in first session, spread more across gameplay.
### **Fix Action**
Reduce to 4-5 core steps. Defer advanced mechanics to later in gameplay.
### **Applies To**
  - *.js
  - *.ts

## Information Overload Popup

### **Id**
info-dump-popup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - showMessage.*\.length.*>.*100|displayText.*length.*>.*80
  - controls:\s*\{[^}]{400,}\}
### **Message**
Long text in tutorial detected. Players don't read. Keep prompts under 10 words. Show, don't tell.
### **Fix Action**
Replace text with visual demonstration. If text necessary, limit to 5-10 words max.
### **Applies To**
  - *.js
  - *.ts
  - *.json

## Skip Without Granting Rewards

### **Id**
no-skip-grant
### **Severity**
error
### **Type**
regex
### **Pattern**
  - skipTutorial(?![\s\S]{0,200}(grant|unlock|give|add))
  - onSkip(?![\s\S]{0,200}(reward|item|ability|unlock))
### **Message**
Skip implemented but may not grant rewards. Players who skip must receive all items/unlocks/abilities they would have gotten.
### **Fix Action**
Add grantSkipRewards() or equivalent after skip. Include items, abilities, flags, and state.
### **Applies To**
  - *.js
  - *.ts

## Unskippable Cutscene at Start

### **Id**
forced-cutscene
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - playCutscene.*await|playVideo.*await|playIntro.*await
  - introSequence(?!.*skipOnInput|.*skipEnabled)
### **Message**
Potential unskippable cutscene at game start. Every second before first input costs players. Make interruptible or skippable.
### **Fix Action**
Add skipOnInput option or skip button. Consider starting gameplay during cutscene (audio over gameplay).
### **Applies To**
  - *.js
  - *.ts

## Hint System Without Cooldown

### **Id**
hint-without-cooldown
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - showHint(?![\s\S]{0,100}(cooldown|delay|timeout|lastHint))
  - displayTip(?![\s\S]{0,100}(interval|throttle|maxShow))
### **Message**
Hint system may spam players. Hints need cooldowns to avoid annoyance. Players need time to try on their own.
### **Fix Action**
Add cooldown (30s minimum), max show count, and detection for 'player exploring vs stuck'.
### **Applies To**
  - *.js
  - *.ts

## Tutorial Without Analytics

### **Id**
no-tutorial-analytics
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*Tutorial(?![\s\S]{0,500}(track|analytics|metrics))
  - tutorial(?![\s\S]{0,300}(funnel|conversion|dropoff))
### **Message**
Tutorial system without visible analytics. You can't improve what you don't measure. Track completion, drop-off points, time per step.
### **Fix Action**
Add analytics tracking for each step: analytics.track('tutorial_step', {step, time, completed})
### **Applies To**
  - *.js
  - *.ts

## Game Over During Tutorial

### **Id**
game-over-in-tutorial
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - gameOver.*tutorial|death.*tutorial.*gameOver
  - tutorial.*onDeath.*gameOverScreen
### **Message**
Game over screen during tutorial. New players shouldn't see game over. Respawn immediately without loading screen.
### **Fix Action**
Replace game over with instant respawn. Hide death count. Make tutorial phase very forgiving.
### **Applies To**
  - *.js
  - *.ts

## Teaching Standard Controls

### **Id**
teaching-obvious-controls
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - tutorial.*wasd|teach.*move.*arrow|hint.*space.*jump
  - showMessage.*"press.*to.*move"|prompt.*"click.*to.*select"
### **Message**
Teaching standard controls (WASD, click, space). Gamers know these. Only teach game-specific mechanics.
### **Fix Action**
Remove prompts for standard controls. Trust players to know genre conventions.
### **Applies To**
  - *.js
  - *.ts

## No Safe Failure During Learning

### **Id**
no-safe-fail-zone
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - tutorialEnemy.*damage.*=.*(?:[2-9]|[1-9][0-9])|enemy.*damage.*tutorial.*(?:[2-9]|[1-9][0-9])
  - tutorial(?![\s\S]{0,200}(forgiving|reduced.*damage|safe))
### **Message**
Tutorial may not have safe failure. New players need forgiving environment to experiment. Reduce enemy damage, remove death penalty.
### **Fix Action**
During tutorial: reduce enemy damage to 25%, give abundant health pickups, instant respawn.
### **Applies To**
  - *.js
  - *.ts

## Single-Path Tutorial Design

### **Id**
linear-only-tutorial
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - if.*solution.*===.*expected|correctAnswer.*===|onlyWay.*true
  - mustUse.*mechanic|requiredAction.*===.*specific
### **Message**
Tutorial may assume single solution. Creative players will find alternatives. Accept any valid solution to objectives.
### **Fix Action**
Define goal, not path. Check for objective completion regardless of method used.
### **Applies To**
  - *.js
  - *.ts

## No Veteran Player Detection

### **Id**
no-veteran-detection
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - tutorial(?![\s\S]{0,400}(veteran|experience|skilled|advanced))
  - onboarding(?![\s\S]{0,400}(detectSkill|playerLevel|adapt))
### **Message**
No veteran detection in onboarding. Veterans get frustrated with basic tutorials. Detect skill and adapt teaching.
### **Fix Action**
Track player actions. If using advanced techniques, reduce tutorial. Offer 'I know this' option.
### **Applies To**
  - *.js
  - *.ts

## Hints Not Contextual

### **Id**
no-context-hints
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - showAllHints|displayControlList|showControls\(\)|listBindings
### **Message**
Hints shown without context. Teach mechanics when needed, not upfront. Players forget what they don't immediately use.
### **Fix Action**
Trigger hints based on player situation: near gap = jump hint, near enemy = attack hint.
### **Applies To**
  - *.js
  - *.ts

## No Mechanic Reinforcement

### **Id**
no-reinforcement-schedule
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - teachMechanic(?![\s\S]{0,300}(reinforce|practice|uses|repeat))
  - tutorial\.complete(?![\s\S]{0,200}schedule.*practice)
### **Message**
Teaching without reinforcement schedule. Players forget unused mechanics. Plan 3-5 uses of each mechanic in next 10 minutes.
### **Fix Action**
After teaching: schedule 3 easy uses, 2 moderate uses, then combine with other mechanics.
### **Applies To**
  - *.js
  - *.ts

## Onboarding Completeness Check

### **Id**
onboarding-checklist
### **Severity**
info
### **Type**
file
### **Pattern**
onboarding-checklist.md
### **Message**
  Consider creating onboarding-checklist.md to track:
  [ ] Skip option visible at all times
  [ ] Time to first input < 10 seconds
  [ ] Core loop reached < 60 seconds
  [ ] Max 4 teaching moments in first 5 minutes
  [ ] Safe failure (no game over in tutorial)
  [ ] Hints have cooldown and max shows
  [ ] Analytics for each onboarding step
  [ ] Veteran detection/skip option
  [ ] Mobile: 3-minute hook complete
  [ ] Reinforcement scheduled for taught mechanics
  
### **Fix Action**
Create checklist file to ensure comprehensive onboarding design
### **Applies To**
  - **/tutorial/**
  - **/onboarding/**

## Mobile Game Slow Start

### **Id**
mobile-slow-start
### **Severity**
error
### **Type**
regex
### **Pattern**
  - mobile.*tutorial.*duration.*>.*120|mobileOnboarding.*time.*>.*180
  - platform.*mobile.*tutorialSteps.*>.*3
### **Message**
Mobile tutorial exceeds 2-3 minutes. Mobile players decide in 3 minutes. Compress onboarding dramatically.
### **Fix Action**
Mobile FTUE: first input < 5s, core loop < 60s, return hook < 180s.
### **Applies To**
  - *.js
  - *.ts
  - *.json

## Mobile Without Auto-Save

### **Id**
mobile-no-save
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - mobile(?![\s\S]{0,300}(autoSave|saveState|persist))
  - platform.*mobile(?![\s\S]{0,200}backgroundSave)
### **Message**
Mobile game may not auto-save frequently. Mobile players get interrupted constantly. Save every 10 seconds.
### **Fix Action**
Implement aggressive auto-save. Save on any significant action. Save on app background.
### **Applies To**
  - *.js
  - *.ts

## Mobile Without Return Hook

### **Id**
mobile-no-return-hook
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - mobileOnboarding(?![\s\S]{0,400}(dailyReward|energy|notification|returnHook))
  - mobile.*ftue(?![\s\S]{0,300}(anticipation|tomorrow|comeback))
### **Message**
Mobile FTUE may lack return hook. The 3-minute session must create anticipation for return. Show what they CAN'T have yet.
### **Fix Action**
Before first session end: show locked content, set up daily reward, create anticipation.
### **Applies To**
  - *.js
  - *.ts