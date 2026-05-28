# Streamer-Bait Game Design

## Patterns


---
  #### **Id**
proximity-voice-chat-design
  #### **Name**
Proximity Voice Chat Design
  #### **Description**
The killer feature of 2020s streamer games
  #### **When To Use**
Any co-op game intended for streaming
  #### **Structure**
    1. Voice volume tied to player distance
    2. Sounds only audible when nearby
    3. Alternative communication tools (walkie-talkies, radios)
    4. Battery/resource limits on long-range comms
    5. In-game voice for atmosphere, Discord for "cheating"
    
  #### **Code Example**
    // Unity/Dissonance proximity voice setup
    public class ProximityVoice : MonoBehaviour {
      public float maxDistance = 15f;
      public float minDistance = 2f;
      public AnimationCurve falloffCurve;
    
      void UpdateVoiceVolume(VoicePlayer player) {
        float distance = Vector3.Distance(
          transform.position,
          player.transform.position
        );
    
        // Linear falloff with curve adjustment
        float normalizedDist = Mathf.InverseLerp(
          minDistance, maxDistance, distance
        );
        float volume = 1f - falloffCurve.Evaluate(normalizedDist);
    
        player.SetVolume(volume);
      }
    }
    
  #### **Benefits**
    - Natural tension from separation
    - Forces strategic grouping decisions
    - Creates "last words" dramatic moments
    - Enables information asymmetry
  #### **Pitfalls**
    - Players will use Discord anyway - design for it
    - Need fallback for solo players

---
  #### **Id**
asymmetric-information-design
  #### **Name**
Asymmetric Information Design
  #### **Description**
Viewers know things players don't - maximum engagement
  #### **When To Use**
Horror games, deduction games, suspense mechanics
  #### **Structure**
    1. Camera shows dangers player can't see
    2. UI elements only visible to audience (health bars, timers)
    3. Jump scare setup visible in background
    4. Traitor identity revealed to viewers early
    5. Chat integration for hints (optional)
    
  #### **Code Example**
    // Viewer-only information system
    class StreamerOverlay {
      constructor(isStreaming) {
        this.isStreaming = isStreaming;
      }
    
      showViewerHint(message, duration = 5000) {
        if (!this.isStreaming) return;
    
        // Shows on stream capture but not player screen
        // Requires OBS scene with viewer-only elements
        streamOverlay.displayText(message, duration);
      }
    
      revealTraitor(playerName) {
        // Viewers see "IMPOSTOR: PlayerName" early
        this.showViewerHint(`The traitor is: ${playerName}`);
      }
    }
    
  #### **Benefits**
    - Creates dramatic irony (audience knows, player doesn't)
    - Builds anticipation for jump scares
    - Enables chat reactions before streamer reacts
  #### **Pitfalls**
    - Stream snipers can cheat
    - Requires careful balance of reveal timing

---
  #### **Id**
content-moment-engineering
  #### **Name**
Content Moment Engineering
  #### **Description**
Design specific moments intended to become clips
  #### **When To Use**
Any game targeting content creators
  #### **Structure**
    1. Design "peak" moments with clear visual/audio punch
    2. Quick recovery to reset for next moment
    3. Unpredictable timing (tension before payoff)
    4. Reaction-worthy reveals
    5. Shareable outcomes (screenshot-worthy)
    
  #### **Code Example**
    // Content moment trigger system
    class ContentMomentManager {
      triggerJumpScare(player, monster) {
        // 1. Build tension (quieter audio, slower gameplay)
        this.buildTension(3000);
    
        // 2. Trigger with visual/audio punch
        this.flashScreen();
        this.playLoudStinger();
        monster.lungeAt(player);
    
        // 3. Immediate consequence
        player.takeDamage(30);
        player.dropItem();
    
        // 4. Quick reset for next moment
        setTimeout(() => this.resetTension(), 1000);
    
        // 5. Log for highlight reel
        this.logClipMoment('jumpscare', player.name);
      }
    
      logClipMoment(type, context) {
        // Integration with clip systems
        // Could integrate with Crowd Control, Medal, etc.
        this.clipLog.push({
          timestamp: Date.now(),
          type,
          context
        });
      }
    }
    
  #### **Benefits**
    - Designed virality, not accidental
    - Streamers know your game "delivers"
    - Creates highlight reel material
  #### **Pitfalls**
    - Over-engineering kills organic moments
    - Balance spectacle with gameplay depth

---
  #### **Id**
social-deduction-mechanics
  #### **Name**
Social Deduction Mechanics
  #### **Description**
Betrayal and hidden roles for maximum drama
  #### **When To Use**
Multiplayer games seeking social viral spread
  #### **Structure**
    1. Hidden roles (at least one traitor)
    2. Teams with conflicting goals
    3. Simple, clear victory conditions
    4. Voting/accusation mechanics
    5. Visible tells vs hidden information
    
  #### **Code Example**
    // Basic social deduction setup
    const SocialDeductionGame = {
      setupRoles(players) {
        const roles = {
          traitors: Math.floor(players.length / 4) || 1,
          innocents: players.length - this.traitors
        };
    
        // Shuffle and assign
        const shuffled = this.shuffle([...players]);
        shuffled.forEach((player, i) => {
          player.role = i < roles.traitors ? 'traitor' : 'innocent';
          player.role_reveal = player.role === 'traitor'
            ? { allies: shuffled.slice(0, roles.traitors) }
            : { allies: [] };
        });
      },
    
      callVote(accuser, accused) {
        // Open voting phase
        this.votingPhase = true;
        this.accused = accused;
        this.votes = {};
    
        // Timer for vote
        setTimeout(() => this.tallyVotes(), 30000);
      },
    
      tallyVotes() {
        const guilty = Object.values(this.votes)
          .filter(v => v === 'guilty').length;
        const innocent = Object.values(this.votes)
          .filter(v => v === 'innocent').length;
    
        if (guilty > innocent) {
          this.eliminate(this.accused);
        }
        this.votingPhase = false;
      }
    };
    
  #### **Benefits**
    - Every round is unique emergent narrative
    - Players create the content naturally
    - Encourages group play (audience multiplication)
  #### **Pitfalls**
    - Betrayal causes real friction - design forgiveness
    - Need enough players for tension

---
  #### **Id**
comedic-failure-design
  #### **Name**
Comedic Failure State Design
  #### **Description**
Make losing entertaining for viewer and player
  #### **When To Use**
Any game where players will fail publicly
  #### **Structure**
    1. Failure must feel fair (player knew the risk)
    2. Visual/audio feedback that's amusing not frustrating
    3. Quick restart to try again
    4. Shareable failure (screenshot/clip worthy)
    5. Progression despite failure (learn something)
    
  #### **Code Example**
    // Comedic death system
    class ComedyDeathHandler {
      onPlayerDeath(player, cause) {
        // 1. Ragdoll with exaggerated physics
        player.enableRagdoll({
          forceMultiplier: 3.0,  // Dramatic launch
          rotationRandomness: 360
        });
    
        // 2. Comedic sound effect
        const deathSounds = [
          'wilhelm_scream.wav',
          'slide_whistle.wav',
          'cartoon_bonk.wav'
        ];
        this.playSound(this.randomChoice(deathSounds));
    
        // 3. Death message with humor
        const messages = [
          `${player.name} speedran to the death screen`,
          `${player.name} discovered a new way to die`,
          `${player.name} is no longer with us`
        ];
        this.displayDeathMessage(this.randomChoice(messages));
    
        // 4. Quick restart option
        this.showRespawnButton(3000);  // 3 second wait
    
        // 5. Track for "best deaths" highlight
        this.logClip('death', cause, player.position);
      }
    }
    
  #### **Benefits**
    - Three losers per round still having fun
    - Clip-worthy failures, not rage quits
    - Encourages risk-taking for content
  #### **Pitfalls**
    - Don't mock player skill
    - Maintain stakes despite humor

---
  #### **Id**
streamer-mode-implementation
  #### **Name**
Streamer Mode Implementation
  #### **Description**
Technical features for content creator compatibility
  #### **When To Use**
Any game targeting streaming audience
  #### **Structure**
    1. DMCA-safe audio toggle
    2. Delay-compatible lobbies (stream sniping protection)
    3. UI readability at compression (large fonts, high contrast)
    4. Audio ducking support for commentary
    5. Integration hooks (Crowd Control, etc.)
    
  #### **Code Example**
    // Streamer mode configuration
    const StreamerModeConfig = {
      audio: {
        dmcaSafeMusic: true,         // Replace licensed tracks
        voiceChatDucking: true,      // Lower game audio during speech
        noLicensedMusic: true        // Completely disable risky audio
      },
    
      antiSnipe: {
        delayedLobbyDisplay: true,   // Don't show lobby code until start
        anonymizeNames: true,        // Replace player names with generic
        hideLobbyCode: true          // Never show join code on stream
      },
    
      ui: {
        highContrastMode: true,      // Readable at 720p streaming
        largerFonts: true,           // 26px minimum
        streamSafeOverlays: true     // Avoid OBS capture issues
      },
    
      integration: {
        crowdControl: true,
        twitchExtensions: true,
        clipMarkers: true            // Auto-mark highlight moments
      }
    };
    
  #### **Benefits**
    - Streamers choose your game over competitors
    - Avoids DMCA takedowns that hurt visibility
    - Reduces stream sniping complaints
  #### **Pitfalls**
    - Streamer mode shouldn't be "worse" experience
    - Test with actual streamers before launch

---
  #### **Id**
price-point-strategy
  #### **Name**
Streamer-Friendly Pricing
  #### **Description**
Price for group purchases and impulsive buys
  #### **When To Use**
Setting launch price for streamer-targeted game
  #### **Structure**
    1. Sweet spot: $10-15 USD
    2. Reduces friction for 4-player group buys ($40-60 total)
    3. Impulse purchase after watching stream
    4. Launch discount optional but effective
    5. Bundles for friend groups
    
  #### **Examples**
    
---
      ###### **Lethal Company**
$10
    
---
      ###### **Stardew Valley**
$15
    
---
      ###### **Among Us**
Free + cosmetics
    
---
      ###### **Phasmophobia**
$14
  #### **Benefits**
    - Viewers buy immediately after watching
    - Groups coordinate purchases easily
    - Lower risk = more purchases
  #### **Pitfalls**
    - Too cheap signals low quality
    - Need volume to compensate for margin

## Anti-Patterns


---
  #### **Id**
youtube-bait-only
  #### **Name**
YouTube Bait Without Depth
  #### **Description**
Games that are only entertaining to watch, not play
  #### **Why Bad**
    Goat Simulator dropped from 10k to 2k players in one year. Games relying solely on bugs/chaos have no staying power. Players feel cheated after initial novelty wears off.
    
  #### **Signs**
    - Humor relies entirely on bugs
    - No progression or skill development
    - Players finish in one session
    - Reviews mention "watch, don't buy"
  #### **Better Approach**
    Octodad model - "charming, fun, and well put together." Entertainment comes from good design, not just broken physics.
    

---
  #### **Id**
over-engineering-content-moments
  #### **Name**
Over-Engineering Content Moments
  #### **Description**
Designing so hard for clips that organic fun disappears
  #### **Why Bad**
    Players sense when they're being "directed" too heavily. Best streams come from genuine reactions, not scripted beats. Reduces replayability when all moments are predictable.
    
  #### **Signs**
    - Every encounter feels identical
    - 'Randomness' is actually scripted sequences
    - Streamers complain it's repetitive
  #### **Better Approach**
    Design systems, not moments. Let emergence create clips. Provide the ingredients, not the recipe.
    

---
  #### **Id**
ignoring-non-streamers
  #### **Name**
Ignoring Non-Streaming Players
  #### **Description**
Only designing for content creators, forgetting regular players
  #### **Why Bad**
    Content creators are 1% of playerbase but drive discovery. If game isn't fun to play, word of mouth dies after initial spike. Reviews from regular players tank Steam score.
    
  #### **Signs**
    - Solo play is boring/broken
    - Game requires external audience to be fun
    - 'This is only fun to watch' reviews
  #### **Better Approach**
    Core loop fun for everyone. Streaming features are additions, not replacements for good game design.
    

---
  #### **Id**
no-copyright-safe-audio
  #### **Name**
No Copyright-Safe Audio Option
  #### **Description**
Shipping with only DMCA-risky music
  #### **Why Bad**
    Streamers get VODs muted or deleted. Repeated strikes = banned accounts. Streamers avoid your game entirely.
    
  #### **Consequences**
    - Muted VODs lose discoverability
    - Streamers won't risk playing
    - YouTube videos get demonetized
  #### **Better Approach**
    Ship with streamer mode. DMCA-safe alternative soundtrack. CD Projekt RED made Cyberpunk 2077 completely DMCA-safe.
    

---
  #### **Id**
session-too-long
  #### **Name**
Sessions Too Long for Streaming
  #### **Description**
Matches/runs that don't fit stream format
  #### **Why Bad**
    Streamers prefer 15-30 minute sessions for variety. 2-hour sessions = one game per stream = less exposure. Viewers drop off during long sessions.
    
  #### **Signs**
    - Average session > 45 minutes
    - No natural break points
    - Streamers cut mid-run frequently
  #### **Better Approach**
    Design 15-20 minute runs with satisfying conclusions. Multiple runs per stream = more content, more clips.
    