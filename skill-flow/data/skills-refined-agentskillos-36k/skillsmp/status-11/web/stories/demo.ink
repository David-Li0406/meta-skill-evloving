// Stable demo story for GEngine
// Expanded branching sample with varied narrative contexts for AI branch testing.
// Includes: exploration, dialogue, tension, discovery scenes.
// Alternate runs rotate paths for validator (minimum two-choice branch).

VAR campfire_log = false
VAR pocket_compass = true
VAR courage = 0
VAR caution = 0
VAR met_stranger = false
VAR found_artifact = false
VAR wolves_spotted = false

-> start

=== start ===
Hello, wanderer. Welcome back to the ridge.
#smoke
The embers breathe a thin ribbon of smoke into the evening air.
Your companion nods at you, waiting for a decision.
+ [Head toward the pines]
    ~ courage += 1
    -> pines
+ [Stay by the fire]
    ~ caution += 1
    -> campfire
+ [Check the compass]
    ~ pocket_compass = false
    The needle jitters, then settles north. The path is set.
    -> pines
+ [Mark the campsite]
    You arrange stones in a ring, marking where you started.
    -> campfire

=== pines ===
The pines hush the wind. Mist gathers between the trunks.
The smoke tag still clings to your clothes, a reminder of camp.
+ [Follow the faint trail]
    -> trail
+ [Cut through the underbrush]
    ~ courage += 1
    -> underbrush
+ [Investigate the distant light]
    -> watchtower

=== trail ===
Footsteps echo in front of you. A lantern swings.
A stranger whispers, "Looking for the signal?"
+ [Answer honestly]
    "Yes. I need the flare to guide my friends."
    The stranger smiles and hands you a flint and dried moss.
    ~ campfire_log = true
    ~ met_stranger = true
    -> stranger_dialogue
+ [Pretend you're lost]
    "Just wandering." The stranger shrugs and leaves.
    The trail fades into darkness.
    -> lost_end

=== stranger_dialogue ===
// DIALOGUE SCENE: Conversation with the stranger
The stranger lingers, lantern casting long shadows across the path.
"You're not the first to come through here tonight," they say. "There's trouble brewing."
+ [Ask about the trouble]
    "What kind of trouble?"
    The stranger glances over their shoulder. "Wolves. A pack moved down from the high ridge. They're hungry."
    ~ wolves_spotted = true
    -> wolves_warning
+ [Thank them and move on]
    "I appreciate the supplies. I should get back."
    The stranger nods. "Safe travels. Keep that fire burning."
    -> return_with_supplies
+ [Ask about the signal]
    "Who else uses the signal?"
    "Rangers, mostly. And travelers like yourself. It's an old system—smoke by day, fire by night."
    The stranger pauses. "There's an old watchtower east of here. Abandoned, but the beacon still works."
    -> watchtower_hint

=== wolves_warning ===
// TENSION SCENE: Urgency and stakes
Your pulse quickens. Wolves in the forest changes everything.
"How close?" you ask.
"Close enough. I heard them an hour ago, down by the creek."
The stranger hands you a burning branch from their lantern. "Take this. Fire keeps them wary."
+ [Rush back to camp]
    ~ caution += 1
    You thank the stranger and hurry back toward the ridge.
    The forest feels different now—every snapped twig a potential threat.
    -> tense_return
+ [Ask to travel together]
    "Safety in numbers. Will you come with me?"
    The stranger hesitates, then nods. "To the ridge. No further."
    ~ courage += 1
    -> escorted_return
+ [Head for the watchtower instead]
    "The watchtower—is it defensible?"
    "Stone walls, iron door. If you can reach it."
    ~ courage += 1
    -> watchtower

=== watchtower_hint ===
The stranger points east, where the trees thin against the night sky.
"You might see it from the clearing. A dark shape against the stars."
+ [Thank them and head east]
    -> watchtower
+ [Return to camp first]
    "I'll check on my companion first."
    -> return_with_supplies

=== watchtower ===
// DISCOVERY/MYSTERY SCENE: Finding something unexpected
You push through the undergrowth until the trees give way to a rocky clearing.
The watchtower rises before you—older than you expected, its stones weathered by centuries.
The door hangs open, creaking in the wind.
+ [Enter the tower]
    ~ courage += 1
    -> tower_interior
+ [Circle around first]
    ~ caution += 1
    You walk the perimeter, checking for signs of recent activity.
    Boot prints in the mud. Someone was here recently.
    -> tower_exterior
+ [Call out]
    "Hello? Anyone there?"
    Silence. Then, from somewhere above, the flutter of wings. Just birds.
    -> tower_interior

=== tower_interior ===
Inside, dust motes drift in the moonlight filtering through arrow slits.
A spiral staircase winds upward. At its base, you notice something glinting beneath debris.
+ [Investigate the glinting object]
    You brush away leaves and dirt to reveal an old brass compass—far older than yours.
    ~ found_artifact = true
    The needle spins wildly, then settles pointing... down?
    -> artifact_mystery
+ [Climb the stairs]
    The steps groan but hold. At the top, the beacon platform opens to the sky.
    The view is breathtaking—you can see the ridge, the forest, the distant gleam of water.
    -> beacon_platform
+ [Search for supplies]
    You find a dusty pack in the corner: rope, a tinderbox, dried meat wrapped in cloth.
    ~ campfire_log = true
    -> return_with_supplies

=== tower_exterior ===
Following the boot prints, you find a cache hidden beneath a loose stone.
Inside: a leather journal and a small knife.
+ [Take the journal]
    ~ found_artifact = true
    The pages are filled with sketches of the forest and notes about "the old paths."
    -> artifact_mystery
+ [Leave it undisturbed]
    You replace the stone. Whatever this is, it's not yours.
    -> tower_interior

=== artifact_mystery ===
// DISCOVERY SCENE: Deepening the mystery
{found_artifact:
    The artifact feels significant—a piece of a larger puzzle you don't yet understand.
}
A sense of unease settles over you. This place holds secrets.
+ [Take the artifact back to camp]
    Whatever this means, your companion should see it.
    -> return_with_supplies
+ [Investigate further]
    ~ courage += 1
    You need to know more before you leave.
    -> beacon_platform
+ [Leave everything and go]
    ~ caution += 1
    Some mysteries are better left alone.
    -> tense_return

=== beacon_platform ===
The platform is intact, the old beacon mechanism still functional.
From here, you could signal for miles.
{wolves_spotted:
    In the distance, you hear howling. The pack is on the move.
}
+ [Light the beacon]
    ~ courage += 1
    You work the mechanism until sparks catch. The beacon flares to life.
    A column of fire rises into the night.
    -> beacon_lit
+ [Use it as a vantage point]
    ~ caution += 1
    You scan the forest below. There—movement near the creek. 
    {wolves_spotted: The wolves.}
    {not wolves_spotted: Deer, perhaps. Or something else.}
    -> descent_choice
+ [Head back down]
    -> return_with_supplies

=== beacon_lit ===
The beacon burns bright. If anyone is out there, they'll see it now.
You wait, watching the forest below.
After what feels like hours, an answering light flickers from the ridge—your companion's fire, burning strong.
+ [Descend and return to camp]
    -> rescue_end
+ [Wait for others to respond]
    More lights appear—distant camps, rangers, travelers drawn by your signal.
    By dawn, a small group has gathered at the tower. You're no longer alone.
    -> tower_gathering_end

=== descent_choice ===
The stairs feel longer going down. Shadows pool in the corners.
+ [Exit through the main door]
    -> tense_return
+ [Look for another way out]
    ~ courage += 1
    You find a narrow passage leading to a root cellar—and from there, a hidden path into the forest.
    -> hidden_path

=== hidden_path ===
The path is old, overgrown but still passable.
It winds through the trees, eventually emerging near the campfire.
Your companion looks up, startled. "Where did you come from?"
+ [Explain everything]
    You tell them about the tower, the artifact, the hidden paths.
    {found_artifact: You show them what you found.}
    -> revelation_end
+ [Keep some secrets]
    "Just exploring. Found a shortcut."
    -> quiet_end

=== tense_return ===
// TENSION SCENE: Returning under pressure
You move quickly through the forest, senses heightened.
{wolves_spotted:
    Every sound could be the pack. You keep the torch high.
}
The ridge appears through the trees. Almost there.
+ [Run for it]
    ~ courage += 1
    You sprint the last hundred yards, bursting into the clearing.
    Your companion jumps up, alarmed. "What happened?"
    -> urgent_return_end
+ [Move carefully]
    ~ caution += 1
    You approach slowly, watching every shadow.
    The campfire glows ahead. Your companion waves.
    -> quiet_end

=== escorted_return ===
// DIALOGUE SCENE: Traveling with the stranger
You walk together in silence at first. Then the stranger speaks.
"I've walked these woods for twenty years. Never seen anything like this season."
+ [Ask what's different]
    "The animals are restless. Moving in patterns I don't recognize. Something's changed."
    -> philosophical_moment
+ [Share your own observations]
    You mention the compass needle, the strange artifacts.
    The stranger stops walking. "You've seen them too."
    -> shared_mystery
+ [Just listen]
    You let them talk. Sometimes people just need to be heard.
    The stranger shares stories of the forest—its history, its secrets.
    -> return_with_supplies

=== philosophical_moment ===
The stranger looks up at the stars. "Maybe the world is shifting. Or maybe we're just paying attention for once."
You walk on in thoughtful silence.
-> return_with_supplies

=== shared_mystery ===
"There are others who know," the stranger says. "Meet me at the watchtower, three days hence."
They press something into your hand—a small token, carved wood.
~ found_artifact = true
-> return_with_supplies

=== underbrush ===
Branches claw at your sleeves. You push through until you find a clearing.
A hollow tree smolders here, smoke curling upward.
+ [Tend the ember]
    You coax the ember into a steady glow.
    ~ campfire_log = true
    -> return_with_supplies
+ [Snuff it out]
    You stamp the ember flat. The clearing falls silent.
    ~ caution += 1
    -> return_empty
+ [Follow the smoke upward]
    Looking up, you notice the smoke forms an unusual pattern against the sky.
    -> smoke_pattern

=== smoke_pattern ===
// DISCOVERY SCENE: Environmental mystery
The smoke curls in spirals that seem almost intentional—like signals, or writing.
+ [Try to read the pattern]
    ~ courage += 1
    You watch carefully. Is that... a direction? An arrow pointing north?
    -> watchtower
+ [Dismiss it as coincidence]
    ~ caution += 1
    Smoke is just smoke. You turn back toward camp.
    -> return_empty
+ [Tend the ember to see more]
    ~ campfire_log = true
    You feed the ember. The smoke thickens, the patterns become clearer.
    But then the wood gives out. The message, if there was one, fades.
    -> return_with_supplies

=== campfire ===
You stay by the fire. Sparks drift like fireflies.
+ [Add another log]
    If only you had one. Perhaps the forest holds more.
    -> pines
+ [Wait and watch]
    The smoke rises in a slow spiral. Somewhere, an answer will arrive.
    -> waiting_end
+ [Study the flames]
    You watch the fire dance, losing yourself in thought.
    -> meditation_moment

=== meditation_moment ===
// INTROSPECTIVE SCENE: Character development
The flames flicker and pop. In their movement, you see glimpses of memory.
+ [Think about the journey ahead]
    Tomorrow you'll push further. But for now, this moment of peace is enough.
    -> waiting_end
+ [Think about home]
    Somewhere beyond these hills, people are waiting. You'll return to them.
    ~ caution += 1
    -> quiet_end
+ [Snap out of it]
    ~ courage += 1
    No time for daydreaming. There's work to do.
    -> pines

=== return_with_supplies ===
You hurry back with ember and tinder.
Your companion grins. "Perfect timing."
+ [Light a signal]
    You build a small pile of branches.
    {campfire_log:
      The ember takes; smoke blooms bright and steady.
    - else:
      It takes effort, but the tinder finally catches.
    }
    A column of smoke marks your position.
    -> rescue_end
+ [Keep the supplies for later]
    You pocket the flint. The night deepens.
    -> quiet_end
+ [Share what you learned]
    {met_stranger or found_artifact:
        You tell your companion about your discoveries.
        {found_artifact: You show them the artifact.}
        {met_stranger: You describe the stranger's warning.}
        -> revelation_end
    - else:
        "Not much to tell. Just a quiet walk."
        -> quiet_end
    }

=== return_empty ===
You return with empty hands. The campfire is low.
Your companion raises an eyebrow.
+ [Admit you panicked]
    ~ caution += 1
    They nod. "At least we're safe."
    -> quiet_end
+ [Pretend you found nothing]
    "The woods were silent," you say. The smoke thins.
    -> waiting_end
+ [Suggest trying again at dawn]
    "I'll go back when there's light. The forest is... strange tonight."
    -> waiting_end

// === ENDINGS ===

=== rescue_end ===
A horn echoes in the distance. Lanterns appear through the mist.
Your signal worked; friends converge on the camp.
The night ends with relieved laughter.
-> END

=== waiting_end ===
You wait until dawn. No one comes, but the sunrise is kind.
The journey will continue another day.
-> END

=== quiet_end ===
Without a signal, the ridge stays quiet.
You and your companion share the last of the rations and plan anew.
-> END

=== lost_end ===
The trail dissolves into fog. Without the smoke to guide you, you wander until the stars fade.
-> END

=== tower_gathering_end ===
By the time the sun rises, the watchtower has become a meeting point.
Rangers, travelers, seekers of old paths—all drawn by the beacon.
Whatever happens next, you won't face it alone.
-> END

=== urgent_return_end ===
{wolves_spotted:
    You tell your companion about the wolves. Together, you build up the fire.
    The pack circles once, twice, then moves on. Fire keeps them wary.
}
{not wolves_spotted:
    Your companion calms you down. "Whatever it was, you're safe now."
}
The night passes in watchful silence. Dawn brings relief.
-> END

=== revelation_end ===
Your companion listens carefully to everything you share.
{found_artifact:
    They turn the artifact over in their hands. "This changes things."
}
"We should investigate further," they say. "But not tonight."
You both settle in, minds full of questions, ready for what tomorrow brings.
-> END
