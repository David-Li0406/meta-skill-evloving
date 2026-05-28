# Example prompts from recent Codex sessions (last few days)

Source window: `~/.codex/sessions/2026/01/14`–`2026/01/16` (rollout `.jsonl` files).  
These are **actual prompt examples** observed in recent sessions, curated for clarity.

---

## High‑frequency implementation directives
- “now your job is to fully implement docs/psv2-psmobile3-lessons-parity-alignment-plan.md systematically and thoughtfully, updating the doc as you make progress. Call out any issues in the doc as you go but do not become blocked. When you're done get a review from opus/gemini give them any files they need. Make sure tests pass and maek dev works. Then open a detailed PR using docs/PR_TEMPLATES.txt .”
- “now your job is to fully implement rustai2/docs/PLAY_VS_AI_HERO_TURN_SIZING_CONTRACT.md systematically updating the document as you go, calling out issue you encounter in the doc. When you finish get a code review from opus/gemini, then open a detailed pr using docs/PR_TEMPLATES.txt”
- “I want you to systematically implement psmobile/docs/play-vs-ai-bet-sizing-ux-synthesis.md thoughtfully, and update the plan as you go completing each phase in the doc and as you finish get a code review from gemini/opus both on quality of code, compliance with our UX we outliend in the doc both literally and by intent and completion fully end to end of our specification as well as idiomatic usage of skia and RN fully aware of our existing paradigms and components. Commit and push when done then update the existing PR to indicate the work.”
- “now your job is to fully and systematically implement docs/psv2-psmobile3-skia-ux-parity-plan.md, updating the document as you go and comparing it to the ground truth files in ../psmobile3 (skia versions) systematically, as you finish a phase get a code review from opus/gemini (give them files they need) for completeness and UX parity as well as idiomatic implementation relative to our existing patterns. Commit and push and when done open a detailed PR using docs/PR_TEMPLATES.txt. You should also be able to test your work using make dev and all tests should pass and analyze should be clean.”
- “Then start systematically building your new skia -> 2d canvas engine for PLAYABLES AND LESSONS, working your way through your document and updating it as you go. Write down any issues you encounter but do not get stuck and do not gate on UI testing. As you finish a phase get a code review from gemini/opus and take the parts you agree with that are idiomatic to the plan.”
- “alright now I want you to implement docs/psmobile-journey-audit-source-of-truth.md systematically, updating the document as you go. You should keep notes on your progress calling out any issues or deviations from the plan. As you finish a phase get a review from opus/gemini EXPLICITLY ASKING IF IT IS BOTH IDIOMATIC AND COMPLETE RELATIVE TO THE PLAN AND GIVING THEM ANY FILES THEY NEED, ITERATE UNTIL ALIGNED. Then Commit and push and move to the next phase. Reference ground truth files for behaviors/UX do not invent user experience.”
- “you should systematically implement the psmobile/docs/PLAY_VS_AI_CLIENT_AUTHORITY_2026-01-13.md fully updating the document as you go, paying attention to elegance and idiomatic and clean architectural solutions as you build, updating the document as you go and finish things. Get code reviews from opus/gemini for idiomatic and COMPLETE implementation according to the plan phases do not move past until you are aligned but DO NOT SCOPE CREEP OR OVERBUILD ON HYPOTHETICALS THIS IS STILL AN MVP. Commit and push and move to the next phase.”
- “I want you to fully implement this docs/psv2-animation-architecture-source-of-truth.md. systematically and thoughtfully, updating the document as you go. Specifically get code reviews from opus/gemini (give them anythign they want) as you complete a phase and SPECIFICALLY ASK if it is IDIOMATIC to our patterns and if the phase is FULLY IMPLEMENTED and do not proceed until you are aligned with them. Commit and push to your branch freely and when you're done open the world's most thoughtful architectural PR that is highly detailed (and watch for \\n in description).”
- “I want you to choose a batch of related components, develop a plan to port them onto our clean hierarchical architecture patterns minimizing unique code where possible, wiring up our UI interaction patterns, fully develop this into the docs, then fully implement it and update the docs as you are finishing. Get code reviews from opus/gemini then fully commit everything.”
- “now your job is to fully implement docs/skia_playables/PLAYABLES_V2_SKIA_RN_GROUND_TRUTH_AUDIT_2026-01-10.md systematically updating the document as you go systematically and thoughtfully, updating the document as you go. Specifically get code reviews from opus/gemini (give them anythign they want) as you complete a phase and SPECIFICALLY ASK if it is IDIOMATIC to our patterns and if the phase is FULLY IMPLEMENTED and do not proceed until you are aligned with them. Commit and push to your branch freely and when you're done open the world's most thoughtful architectural PR that is highly detailed (and watch for \\n in description)”
- “I want you to fully implement this psv2-offline-first-architecture.md. systematically and thoughtfully, updating the document as you go. Specifically get code reviews from opus/gemini (give them anythign they want) as you complete a phase and SPECIFICALLY ASK if it is IDIOMATIC to our patterns and if the phase is FULLY IMPLEMENTED and do not proceed until you are aligned with them. Remember your ground truth references and be VERY THOUGHTFUL this layer is CRITICAL. Commit and push to your branch freely and when you're done open the world's most thoughtful architectural PR that is highly detailed (and watch for \\n in description).”
- “You were working on: I want you to systematically begin implementation of psmobile/docs/PLAY_VS_AI_HAND_END_PRESENTATION_AUTHORITY_2026-01-13.md, updating the document as you go noting any issues you encounter as you build but not getting stuck, as you finish phases get reviews from opus/gemini (give them anything they ask for) on compliance with our idiomatic patterns and architecture document and if we REALLY finished the phase we think we did. Keep the document up to date, commit and push as you finish phases. When you're fully done open a detailed pr using docs/PR_TEMPLATES.txt.”
- “I want you to fully implement this docs/SKIA_ASSET_FONT_PRELOAD_AUTHORITATIVE_2026-01-11.md. systematically and thoughtfully, updating the document as you go. Specifically get code reviews from opus/gemini (give them anythign they want) as you complete a phase and SPECIFICALLY ASK if it is IDIOMATIC to our patterns and if the phase is FULLY IMPLEMENTED and do not proceed until you are aligned with them. Commit and push to your branch freely and when you're done open the world's most thoughtful architectural PR that is highly detailed (and watch for \\n in description).”
- “I want you to fully implement this docs/skia_playables/PLAYABLES_V2_SKIA_RN_GROUND_TRUTH_AUDIT_2026-01-11_V2_OC.md systematically and thoughtfully, updating the document as you go. Specifically get code reviews from opus/gemini (give them anythign they want) as you complete a phase and SPECIFICALLY ASK if it is IDIOMATIC to our patterns and if the phase is FULLY IMPLEMENTED and do not proceed until you are aligned with them. Remember your ground truth references and be VERY THOUGHTFUL this layer is CRITICAL. Commit and push to your branch freely and when you're done open the world's most thoughtful architectural PR that is highly detailed (and watch for \\n in description). I'm doing other stuff in the repo too so don't get all freaked out when you see other dirty files please.”
- “Your job is to build the full scope of docs/psv2-auth-backend-login-roadmap.md one phase at a time, as a stack of branches, one branch per phase. You will update the document as you go and as you finish you'll ask opus/gemini for a code review AND YOU WILL EXPLICITLY ASK THEM TO AUDIT THE CODE VERSUS THE FULL REQUIREMENTS OF THE PHASE AND ITERATE UNTIL THEY AGREE IT IS COMPLETED. For any blockers you should record them in the document and proceed as best you can given the blocker, looking to get as much built as possible. For example, using a placeholder value to unblock yourself if you don't have a credential, etc. You should commit and push as you complete phases after making sure all tests pass and analyze is clean. Iterate autonomously and as you finish a phase, cut the next phases branch and proceed. IT IS CRITICAL that you're referencing the ground truths in ../psmobile4. Keep context on our overall goal reminding yourself often that we're looking to intelligently port ../psmobile4 front end to flutter natively while maintaining full backend, iOS app store and google play store compatibility, as well as our other deps such as clerk, etc.”
- “once you've got your phased plan together, cut a branch and implement each phase systematically updating the document as you finish and getting code reviews from opus and gemini. Continue this way through each phase acting on any code review feedback you agree with. Stay elegant and idiomatic, to the plan. Commit and push after each phase finishes.”

---

## More long directives (history.jsonl samples)
- “if done with this phase - get a code review from gemini/opus, integrate what you agree with before updating document, committing JUST THE FILES WE CHANGED IGNORING OTHER FILES THAT ARE DIRTY (THAT IS MY WORK), then move to the next phase of the plan”
- “autonomously iterate, running agents, finding significant bottlenecks in yield, developing evals per docs/AGENT_EVALS.md using GROUND TRUTH REAL DATA, adjust prompt using docs/PREFERRED_PROMPT_PATTERN.md and then test improvements. Your goal is to double real end to end yield … (long prompt about validator, concurrent workers, second opinions, code reviews)”
- “I want you to fully implement this docs/skia_playables/PLAYABLES_V2_SKIA_CORRECT_FEEDBACK_AUDIT_2026-1-11.md systematically … get code reviews from opus/gemini … open architectural PR …”
- “now your job is to fully and systematically implement docs/psv2-psmobile3-skia-ux-parity-plan.md … compare to ground truths … get opus/gemini review … tests/analysis clean … PR template”
- “Your job is to build the full scope of docs/skia_playables/PLAYABLES_V2_SKIA_ROADMAP_2026-01-09.md one phase at a time … branch-per-phase … code reviews required … RN playable/lesson behavior is ground truth … commit/push per phase”
- “okay I want you to build this docs/psv2-psmobile4-asset-audit.md in a branch per phasis … ground truth ../psmobile4 … reviews per phase … detailed PR”
- “alright now I want you to implement docs/psmobile-journey-audit-source-of-truth.md … (same as earlier but with PR requirement and formatting note)”
- “now fully implement docs/skia_playables/PLAYABLES_V2_SKIA_SCRIPTED_HAND_DEEP_AUDIT_2026-01-12.md … reviews per phase … ignore dirty files you don’t recognize”
- “okay proceed with your test list, getting it working on android … add tests to authoritative reference … opus/gemini review on ‘did we test what we wanted to’”
- “update docs to indicate what is done, then cut the branch for the next PR from this branch … push and open PR against this branch not main”
- “(long CFR/ES CFR investigation directive about passive AA, ESCFR correctness, tracing, reviewing papers, worklog, code reviews with gemini/gpt5.2)”
- “fully implement your hello world plan … Flutter best practices, iOS/Android builds, Galaxy A55 sim, iPhone sim … code reviews … production-ready-ish”
- “make sure you’ve fully implemented the phase you were working on … get code review … update doc/commit files you changed, ignore dirty files”
- “if we’re good commit, push, cut a branch for the next phase … code review from opus & gemini 3 pro preview … update plan doc”
- “(gym note) iPhone 13 sim running … get Skia puzzles working … reference listed docs … keep work log”
- “fully implement the plan end to end … test on iPhone 16 sim … code review … add QA commands to skills if added … thoughtful PR”
- “systematically implement docs/skia-playground-port-plan.md … commit/push then code review”
- “great now fully implement the plan end to end systematically phase by phase updating the document as you go, getting code reviews as you finish a phase from opus/gemini”
- “i want you to autonomously INCREASE YIELD … build evals for real failures … tweak prompts … avoid poisoning … etc.”
- “then I want you to fully implement the next phase from the plan docs/animation-refactor/ANIMATION_INVENTORY_2026-01-02.md … code review … do not revert/delete/stash other work”

---

## Additional long directives (history.jsonl samples)
- “after you've done the current phase - I want you to implement the next phase, get code reviews from opus/gemini and integrate any findings you agree with, then update the document to indicate what is done. Commit only after you've incorporated feedback and IGNORE FILES YOU DID NOT CHANGE I AM DOING THINGS IN THIS REPO DO NOT TOUCH THEM JUST COMMIT THE FILES YOU TOUCHED.”
- “something is insanely broken. On ios sim we're going down to 1 js FPS and UI during periods on an unanimated playable when I'm doing literally nothing is showing like 50 FPS instead of 60. I need you to figure out what is going on. You have full access to my iphone 13 sim. The whole app feels insanely lagged and regressed”
- “that worked, proceed per your best judgement on how to advance forward incrementally towards our real world use case that we're trying to get to so we can find the point of failure.”
- “When you've fully finished I want you to get your work fully committed and pushed. Then I want you to merge in main and thoughtfully adopt the patterns for UI <> JS from main.”
- “proceed with implementing PR2 systematically updating docs/skia_playables/PR2_PLAYABLES_V2_SKIA_COMPONENT_PORT_PLAN_2026-01-07.md periodically”
- “your job is to review the work we've done on this branch … enhance maestro testing for no-collections branch … plan doc … iPhone 16/13 … then android … document and amend PR”
- “ramp up on docs/wishlist/implementation-plan.md … review existing implementations for elegance/alignment … design UX where mocks missing … multiple branches … pass CI … I’ll read in the morning”
- “no look the goal is not the lesson the goal is to make our agents work right … use eval-first strategy per docs/AGENT_EVALS.md and docs/PREFERRED_PROMPT_PATTERN.md … lessons just vehicles … iterate and log; PR in the morning”
- “Your job is to autonomously figure out how to train a 2p NLHE policy that plays reasonably well … keep work log … iterative tests … avoid big speculative runs … AA/KK must not collapse … commit freely”
- “Only do ios for now. implement systematically and exactly on plan per @apps/mobile/docs/SKIA_TABLE_TASK_PLAN.md … work log … audit for visual parity … code reviews for pattern compliance”
- “okay your job is to read docs/skia_playables/PLAYABLES_V2_SKIA_SURFACE_ROADMAP_2026-01-07.md and then fully implement docs/skia_playables/PR1_PLAYABLES_V2_SKIA_COMPONENT_KIT_PLAYGROUND_PLAN_2026-01-07.md … notes, elegant solutions, code review”
- “Then start systematically building your new skia -> 2d canvas engine for PLAYABLES AND LESSONS … update document … code reviews per phase”
- “› okay now for solutions I prefer architectural solutions that make things work better by default going forward … prefer elegant, simple, architectural with clean APIs. What is your proposed solution?”
- “You're working to fully implement docs/puzzles-demo-plan.md … update document, test major phases, keep work log, commit/push regularly”
- “proceed per your best judgement on how to advance forward incrementally towards our real world use case that we're trying to get to so we can find the point of failure.”
- “port the remaining items onto the new fraemwork per the docs/reanimation-refactor autonomously execute the plan code reviewing as you go. commit as you finish items.”
- “Your goal is to get to the bottom of the issues in our docs/KEY* by implementing and testing per docs/KEY_THEORIES3.md … log work in new doc … high-signal tests … aim for core intent solution … PR desired”
- “figure out where this sentry setting comes form and how its set up in the prod/staging/dev apps … understand the crash cause, no speculative fixes … sentry has been on for months”
- “You're to fully build our docs/PUZZLE_COLLECTION_BUILDER_AGENT_PLAN.md … use evals as fulcrum … prompts per preferred pattern … avoid poisoning … work log … test agent … best PR”
- “something is insanely broken … (expanded FPS lag version with more detail about 1 js FPS, 50 UI FPS, never seen before, high-end m3 max)”
- “Your job is to autonomously figure out how to train a 3p NLHE policy that plays reasonably well … work log … iterative tests … AA/KK must not collapse … commit freely”
- “review your plan and fully implement it! … log progress … test skill on open sims … update SKILL.md … open PR”
- “I want you to do is use maestro flows / mobile sim to make sure the startup seems strong with these changes in … gather confidence, fix obvious issues (chore branch), full writeup, optional gemini review”
- “we're on a branch for this. fully implement the plan … ignore files you don’t recognize … ensure CI checks pass … work log … world’s best PR”
- “autonomously iterate, running agents, finding significant bottlenecks in yield … double end-to-end yield … eval-first … prompt tuning … (shorter version)”
- “okay great your job is to fully build this cleanly, idiomatically and elegantly … impress top RN architects … work log … PR when ready”
- “okay heres what I want you to do fully implement the next phase, get code reviews from opus/gemini integrate any feedback you think is good, udpate the doc … commit just the files you changed IGNORE ANY CHANGES IN THE PROJECT YOU DIDNT MAKE”
- “proceed with fully porting and testing per docs/V4_PULL_OVER_GUIDED_WALKTHROUGH_RUNTIME_PLAN_2026-01-07.md onto the .worktrees/gw-authoring-tools … stop after porting authoring tools”
- “when you're fully aligned, systematically build out your plan for making our skia playables testable … update document … code reviews … commit/push … ignore other dirty files”
- “get our profile defaults stuff fully tested via maestro on both ios and android … no hacks … keep work log … fully commit work”

---

## Planning + architecture doc requests
- “put a phased impleentation plan, depth first systematic build at top of document fully specify each phase its exit criteria leave nothing out, more phases better than fewer”
- “i want it to cross link to the audits and ground truths in each phase and be much more exhaustive”
- “fully specify the fulla rchitecture for this plan, files on disk, all patterns (idiomatic, flutter native), for eahc phase point to the architecture that matters really go deep on each component and all the parts that must get built and fully specify them, control flow, object hierarchies, test patterns, everything.”
- “obviously we want feedback above the scrim go super deep on this architecturally and build a new doc out using one of the planning doc templates in docs dir”
- “Okay now I want you to review our research in @docs/2d_gaming_engine_paradigm_research.md and I'd like for you to read @docs/skia_playables/PLAYABLES_V2_SKIA_REACT_ENGINE_MISMATCH_WRITEUP_2026-01-16.md again and I'd like for you to create a new document which proposes a concrete refactored Skia playable and lessons architecture. It should show all core primitives, all the public APIs, the fully realized structure on disk, the idiomatic patterns and why they solve the problems we're having today and why they are elegant/clean. It should show how *EVERY SINGLE ONE OF OUR PLAYABLES WE PORTED TO SKIA* will be ported, what objects they share, how all structure on disk looks, how all transitions are handled.”

---

## PSV2 planning + architecture directives (recent)
- “› now I want you to fully implement docs/psv2-lesson-runner-plan.md systematically updating the document as you go, call out any issues you encountered along the way and as you complete phases have opus/gemini code review for idiomatic compliance with patterns and plan, accomplishing the *INTENT* of the plan and *COMPLETELY finishing the phase as well as UX compliance with our RN ground truths. Commit and push as you finish phases.”
- “okay now your job is to fully and systematically implement docs/psv2-lessons-porting-guide.md updating the document and testing as you go, as you finish a phase get a code review from opus/gemini and commit/push and then move to the next phase. Have opus/gemini review for idiomatic nature adn compliance to ground truth ../psmobile3 UX and only move forward when you are aligned with them (give them files they need) but youd ont' have to take all pedantic or purely hypothetical advice they offer. When you're fully complete use docs/PR_TEMPLATES.txt to open a detailed PR.”
- “your job is to fully and systematically implement docs/psv2-puzzles-ux-parity-architecture-plan.md, updating the document as you go. As you finish a phase get a code review from opus/gemini (give them files they need) for fidelity of UX vs ground truth in ../psmobile and idiomatic implementation using our elegant flutter patterns and architecture. Commit/push freely. When you're fully implemented open a detailed pr using docs/PR_TEMPLATES.txt”
- “now your job is to sytematically implement docs/psv2-qa-automation-architecture-plan.md updating the document as you finish items, noting any issues you encounter. Test as it makes sense you can use existin gandroid sim. Commit and push after each phase, and when you finish get a code review from opus/gemini. Then open a detailed pr using docs/PR_TEMPLATES.txt”
- “now your job is to fully and systematically implement docs/psv2-psmobile3-skia-ux-parity-plan.md, updating the document as you go and comparing it to the ground truth files in ../psmobile3 (skia versions) systematically, as you finish a phase get a code review from opus/gemini (give them files they need) for completeness and UX parity as well as idiomatic implementation relative to our existing patterns. Commit and push and when done open a detailed PR using docs/PR_TEMPLATES.txt. You should also be able to test your work using make dev and all tests should pass and analyze should be clean.”
- “now your job is to fully implement docs/psv2-psmobile3-lessons-parity-alignment-plan.md systematically and thoughtfully, updating the doc as you make progress. Call out any issues in the doc as you go but do not become blocked. When you're done get a review from opus/gemini give them any files they need. Make sure tests pass and maek dev works. Then open a detailed PR using docs/PR_TEMPLATES.txt .”

---

## Architecture deep‑dives + audits
- “I want you to step back, start a document outlining the architecture of the snapshot system, the structure on disk, full object hierarchy, the call sites, flow of data, everything get all details into the document”
- “i want you to propose the most idiomatic and elegant architectural solution that creates clean central patterns and abstractions, doesn't create dual path patterns, no code duplication. Clean public APIs, etc. Award winning and stunning in elegance. put it in doc fully formed.”
- “I want you to take the best of our research, and the reecommendations and update the proposed architecture document to have the cleanest and most idiomatic, centralized and elegant solution. Minimal complexity or chances of drift, no scope creep. It should be shockingly simple but highly effective and elegant.”
- “I want you to integrate this JS thread work into the plan as part of the phases and the report card: PLAYABLES_V2_SKIA_JS_UI_THREAD_AUDIT_2026-01-13.md. Then I want you to make your process for each phase include updating the report cards by re-auditing the code against them:.”
- “I want you to get everything that is about our actual architectural plan out of the research doc”
- “i want you to fully document this pattern exactly as you see it in the logs in a new doc, ground the behavior in the code citing ground truth references”
- “ramp up on docs/skia_confetti_effects_bus_arch_plan_2026-01-14.md and audit the plan to figure out if it is introducing additional sources of truth or reducing complexity”
- “i want you to deeply audit our full skia_playables port (docs/skia_playables) code end to end and find all places we're doing shit painfully in JS or unecessarily back and forth between JS/UI threads building the worlds most complete and authoritative audit, save it as a new doc”

---

## UI/UX planning + audit prompts
- “ramp up on the play vs AI tab in psmobile, and go find the safe area policy we use on other tabs and the header we use on other tabs, and give me a plan to add a "Play" header and fix the safe area and remove the "X" button on the play tab”
- “lets keep the skia header and fix safe area + remove the X”
- “› also theres a HUGE space below action buttons, its like double the size of the button area itself that is causing the whole canvas to shrink unecessarily small during play.
  Figure out why taht is there update the plan to remove the double height spacing. Its like a 4 row grid basically.”
- “no you're not hearing me dude the problem sin't sometimes theres 2 sometimes theres four the problem is THERE IS ROOM FOR EIGHT BUTTONS [codex-clipboard-e4Hv1m.png 1764x1638]”
- “I want you start a new doc for a new set of action controls tha twill be built entirely in skia, so we're corner to corner skia based on the play vs AI. These will work differently than our current controls. 1) They will have 3 buttons visible one row at all times, some buttons may be disabled depending on legal actions in general the buttons will be a) Fold (always there sometimes active sometimes not) b) check or call (again always there, text depends on if facing a bet)  c) bet/raise always there text depends on if facing a bet or not and if the player has enough chips to bet or raise 2) when they click bet or raise they get a pop up slider and concenivence amount buttons that are scaled thoughtfully based on the pot size and the players remaining chip stack and the previous bet c) The behavior is coming from this old figma mock: https://www.figma.com/design/3YYekV0dpuVXvV3B1lPtJU/Poker-Skill---App?node-id=1227-46469&t=yoXDjp4uSH1ejgla-4 which you should download and analyze in detail. The look and feel should be our current application look and feel for all buttons, colors, styles, etc. It is important to note that we now support custom bet actions of any size per our rustai2/docs/PLAY_VS_AI.md . I want you to go insanely deep on this start a new document documenting all of the different states for the buttons, and surface any data you need from server you don't currently get so I can implement it. I want you to fully specify the UX with simple ascii wireframes and link to the figma for reference. I want a full on disk architecture plan as well as an object hierarchy, control flows, data hierarchy. I want you to specify enabled/disabled states for buttons *AND* i want you to specify the state for the buttons when it is not the players turn - they should change be present but disabled. Get the ascii mocks for the slider/convenience sizing in place in the doc. Show the heuristic you'll use to figure out the convenience button amounts. Walk through all the edge cases (can't afford to raise, all in with a call, blind play, all in on the big blind, everything). Make this a definitive and fully specified document”

---

## QA / automation / ops
- “ramp up on our qa psv2-qa-automation-architecture-plan.md I just want a simple command I can run to personally see some automation happening, give me a few options”
- “now your job is to sytematically implement docs/psv2-qa-automation-architecture-plan.md updating the document as you finish items, noting any issues you encounter. Test as it makes sense you can use existin gandroid sim. Commit and push after each phase, and when you finish get a code review from opus/gemini. Then open a detailed pr using docs/PR_TEMPLATES.txt”

---

## Simulator + tooling commands
- “find the latest build of the app and install it on the iphone 13 and iphone 16 pro sims, leave the regular iphone 16 sim alone. They are all running already adn metro is too just install thea pps”
- “I'm noticing that I think sometimes when we start metro its listening on localhost, and other times its on my tailscale domain. Can you see why?”
- “i always run either make ios-fresh or make metro-clean, compare those two”
- “turn on the qa bridge overlay in iphone 13 sim”
- “omfg turn  off the animations disabled flag”
- “turn animations back off”
- “turn them back on”

---

## Reviews + audits
- “great now do a full code review on this branch for compliance with our idiomatic and elegant patterns, also have opus/gemini do one (give them any files they need) and save your full code review as a comment on the PR”
- “diff this branch against origin/main and look for logging that is in hot loops and may affect performance give me a full audit”
- “read docs/skia_playables/PLAYABLES_V2_UX_LOAD_TRANSITIONS_2026-01-13.md and then diff this branch against origin/main and look for looping that may affect performance, look for logging in hot loops, and just spam”

---

## Document / asset ops
- “copy downloads dir latest file (-rw-r--r--@    1 aelaguiz  staff        23092 Jan 15 11:48 MVP recommendation_ “Play vs AI — Challenge Runs” .md) into our docs dir, rename it so it has no spaces”
- “commit just that file ignore other dirty files”

---

## Short approvals / follow‑ups
- “do it”
- “do that”
- “yeah commit it”
- “okay I'm going to make server changes but it'll take a while, can we build without those or do we need to wait for them to land?”
