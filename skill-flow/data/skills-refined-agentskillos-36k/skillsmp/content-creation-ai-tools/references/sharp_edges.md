# Content Creation - Sharp Edges

## Midjourney Prompt Length

### **Id**
midjourney-prompt-length
### **Summary**
Longer prompts don't mean better images
### **Severity**
medium
### **Tools Affected**
  - midjourney
  - flux
  - dall-e-3
### **Situation**
Writing paragraph-length prompts expecting better results
### **Why**
  AI image models have attention limits. After ~60-80 words, later
  concepts get ignored or muddy. The model can't focus on everything.
  
  Ironically, shorter focused prompts often produce better results
  than detailed essays.
  
### **Solution**
  1. Focus on 2-3 key concepts maximum
  2. Use weighted syntax (::2) for important elements
  3. Put important concepts first
  4. Use style references instead of describing style
  
  ```
  # Bad: Too long, conflicts
  A beautiful majestic mountain landscape at sunset with
  golden light streaming through clouds and a small cabin
  in the foreground with smoke coming from chimney and
  birds flying overhead and a river running through...
  
  # Good: Focused
  Mountain cabin at golden hour, smoke from chimney,
  dramatic clouds --ar 16:9 --style raw
  ```
  
### **Symptoms**
  - Images ignore parts of prompt
  - Muddy, confused outputs
  - Results don't match description

## Ai Art Copyright

### **Id**
ai-art-copyright
### **Summary**
AI-generated images have murky copyright status
### **Severity**
high
### **Tools Affected**
  - midjourney
  - flux
  - dall-e-3
  - stable-diffusion
  - ideogram
  - leonardo-ai
### **Situation**
Using AI images for commercial products without understanding legal risk
### **Why**
  As of 2024, AI-generated images have unclear copyright status:
  - US Copyright Office says "no copyright for purely AI-generated works"
  - Human creative input MAY establish some rights
  - Training data lawsuits ongoing (Getty vs Stability AI)
  - Different countries have different rules
  
  Using AI art commercially carries legal uncertainty.
  
### **Solution**
  1. Add significant human creative modification
  2. Don't use for trademark/logo without legal review
  3. Keep generation records (prompts, seeds)
  4. Consider stock images for legally-sensitive uses
  5. Watch for regulatory developments
  6. Some tools (Adobe Firefly) train only on licensed content
  
### **Symptoms**
  - Can't register copyright
  - Legal challenges from artists
  - Platform terms changes

## Style Artist Name Ethics

### **Id**
style-artist-name-ethics
### **Summary**
Using artist names in prompts is ethically contentious
### **Severity**
medium
### **Tools Affected**
  - midjourney
  - stable-diffusion
### **Situation**
Prompting 'in the style of [living artist]'
### **Why**
  Using living artists' names to replicate their style:
  - Potentially devalues their original work
  - May violate their publicity rights
  - Contributes to training data concerns
  - Some platforms now block artist names
  
  Dead artists (Monet, Van Gogh) are generally safer.
  
### **Solution**
  1. Use style descriptors instead of names ("impressionist" not "Monet")
  2. Use movement/era names ("art nouveau", "bauhaus")
  3. Describe specific techniques ("heavy impasto", "pointillism")
  4. Commission original style training on your own art
  
### **Symptoms**
  - Prompts rejected by platform
  - Ethical concerns from team
  - Artist community backlash

## Consistent Characters Hard

### **Id**
consistent-characters-hard
### **Summary**
Character consistency across images is extremely difficult
### **Severity**
high
### **Tools Affected**
  - midjourney
  - dall-e-3
  - flux
### **Situation**
Need same character in multiple scenes for story/brand
### **Why**
  Base image models generate independently. Each image is new.
  "Same person" means nothing to the model - it will create
  similar but different faces every time.
  
  This is a fundamental limitation, not a prompting problem.
  
### **Solution**
  1. Use specialized tools (Leonardo AI character training)
  2. Use reference images with --cref (Midjourney V6)
  3. Use ControlNet with face reference (Stable Diffusion)
  4. Accept variation and use for non-hero shots
  5. Consider 3D character rendering for perfect consistency
  
  ```
  # Midjourney V6 character reference
  /imagine [description] --cref [image_url] --cw 100
  ```
  
### **Symptoms**
  - Character looks different in every image
  - Brand mascot is inconsistent
  - Story visuals don't match

## Video Credit Burn

### **Id**
video-credit-burn
### **Summary**
AI video credits burn extremely fast
### **Severity**
high
### **Tools Affected**
  - runway
  - pika
  - kling
  - luma
### **Situation**
Running out of video credits mid-project
### **Why**
  Video generation is expensive:
  - Each 4-second clip might cost $0.50-2.00
  - Iterations multiply cost (5 tries = 5x cost)
  - Upscaling and extending cost extra
  - Easy to burn $50-100 in an afternoon
  
  Unlike images (pennies each), video adds up fast.
  
### **Solution**
  1. Perfect your image FIRST, then animate it
  2. Use image-to-video (more predictable than text-to-video)
  3. Batch your generation sessions
  4. Start with shorter clips to test
  5. Budget credits per project upfront
  6. Use free tiers for experimentation
  
### **Symptoms**
  - Hit monthly limit in first week
  - Project stalls waiting for credits
  - Unexpected billing

## Uncanny Valley Avatars

### **Id**
uncanny-valley-avatars
### **Summary**
AI avatars can feel creepy to viewers
### **Severity**
medium
### **Tools Affected**
  - heygen
  - synthesia
### **Situation**
Creating talking head videos that make viewers uncomfortable
### **Why**
  AI avatars hit uncanny valley:
  - Micro-expressions are off
  - Eye movement is unnatural
  - Lip sync timing slightly wrong
  - Viewers feel "something's wrong" even if they can't articulate it
  
  This affects trust and engagement.
  
### **Solution**
  1. Use for internal/training videos first (more forgiving audience)
  2. Keep clips short (under 60 seconds)
  3. Add b-roll to break up talking head
  4. Use clearly-stylized avatars (less uncanny)
  5. Test with real audience before launch
  6. Consider real human for trust-critical content
  
### **Symptoms**
  - Low engagement on avatar videos
  - Viewers comment 'creepy'
  - Lower conversion than human videos

## Video Motion Artifacts

### **Id**
video-motion-artifacts
### **Summary**
AI video creates impossible physics and artifacts
### **Severity**
medium
### **Tools Affected**
  - runway
  - pika
  - kling
  - luma
### **Situation**
Generated video has weird distortions, morphing, or physics breaks
### **Why**
  Current AI video models don't understand physics:
  - Objects morph unexpectedly
  - Hands/fingers multiply or disappear
  - Motion can be jittery or unnatural
  - Scene elements drift or change
  
  This is the current state of the art, not a user error.
  
### **Solution**
  1. Keep camera movement simple (or static)
  2. Avoid complex hand/finger movements
  3. Use shorter clips (less time for errors)
  4. Pick best 2-3 seconds from longer generation
  5. Use motion brush to control specific areas
  6. Accept some imperfection for speed/cost benefit
  
### **Symptoms**
  - Hands morph weirdly
  - Objects change mid-video
  - Physics feel wrong

## Voice Clone Consent

### **Id**
voice-clone-consent
### **Summary**
Voice cloning without consent is illegal in many places
### **Severity**
critical
### **Tools Affected**
  - elevenlabs
  - murf
### **Situation**
Cloning someone's voice without their permission
### **Why**
  Voice cloning laws are tightening rapidly:
  - California, Tennessee have voice protection laws
  - EU AI Act has requirements
  - Platforms require consent verification
  - Can be used for fraud (family scams)
  
  Even if technically possible, may be illegal.
  
### **Solution**
  1. Only clone voices with explicit written consent
  2. Keep consent records for compliance
  3. Use only your own voice or licensed voices
  4. Check local laws before commercial use
  5. Use pre-made voices for lower risk
  6. Add watermarking where possible
  
### **Symptoms**
  - Platform account banned
  - Legal demand letters
  - Reputation damage

## Ai Music Licensing

### **Id**
ai-music-licensing
### **Summary**
AI-generated music licensing is legally uncertain
### **Severity**
high
### **Tools Affected**
  - suno
  - udio
### **Situation**
Using AI music in commercial projects
### **Why**
  AI music has unclear rights:
  - Generated from copyrighted training data
  - May inadvertently replicate existing songs
  - Streaming platforms may reject
  - Lawsuits ongoing (RIAA vs Suno/Udio)
  
  Not safe for revenue-generating projects.
  
### **Solution**
  1. Use for personal/internal projects only
  2. For commercial: use licensed stock music
  3. Check for melody matches before publishing
  4. Keep platform terms updated (they change)
  5. Consider tools trained on licensed data
  
### **Symptoms**
  - Content ID claims
  - Platform takedowns
  - Can't monetize

## Voice Uncanny Detection

### **Id**
voice-uncanny-detection
### **Summary**
Audiences are increasingly detecting AI voices
### **Severity**
medium
### **Tools Affected**
  - elevenlabs
  - murf
### **Situation**
Using AI voice where authenticity matters
### **Why**
  As AI voice becomes common:
  - Listeners are learning to spot it
  - Slight unnatural patterns emerge
  - Trust decreases when detected
  - Some platforms may require disclosure
  
  The "just as good as human" claim is becoming less true
  as audiences develop detection skills.
  
### **Solution**
  1. Use AI voice for draft/internal content
  2. Record human for final/trust-critical content
  3. Disclose AI voice use proactively
  4. Focus on high quality over quantity
  5. Use AI for languages you don't speak (expected)
  
### **Symptoms**
  - Comments calling out AI voice
  - Lower engagement than human narration
  - Trust concerns from audience

## Ai Detection Penalties

### **Id**
ai-detection-penalties
### **Summary**
AI-detected content may be penalized or rejected
### **Severity**
high
### **Tools Affected**
  - claude
  - chatgpt
  - jasper
  - copy-ai
### **Situation**
Publishing AI-written content without human editing
### **Why**
  AI detection is everywhere:
  - Google may downrank AI content (unconfirmed but suspected)
  - Academic/professional settings flag it
  - Clients may reject AI-written deliverables
  - AI has detectable patterns (hedging, certain phrases)
  
  Even if "allowed", detection can hurt credibility.
  
### **Solution**
  1. ALWAYS edit AI output substantially
  2. Add personal examples and voice
  3. Rewrite key sections completely
  4. Don't publish first drafts
  5. For SEO: add original research/data
  6. Disclose AI assistance where appropriate
  
### **Symptoms**
  - Content flagged by detection tools
  - SEO rankings drop
  - Client rejects work

## Ai Hallucination Facts

### **Id**
ai-hallucination-facts
### **Summary**
AI confidently makes up facts, quotes, and citations
### **Severity**
critical
### **Tools Affected**
  - claude
  - chatgpt
  - jasper
  - copy-ai
### **Situation**
Publishing AI-generated facts without verification
### **Why**
  LLMs hallucinate:
  - Invent plausible-sounding statistics
  - Create fake quotes attributed to real people
  - Generate non-existent citations
  - Mix up facts between similar topics
  
  This can destroy credibility and create legal liability.
  
### **Solution**
  1. VERIFY every fact, statistic, and quote
  2. Don't trust ANY citation without checking
  3. Use AI for structure, not facts
  4. Add your own verified research
  5. For critical content: fact-check with multiple sources
  
  ```
  # Bad: Trust AI
  "Studies show 73% of users prefer..." <- AI made this up
  
  # Good: Verify
  Take AI stat -> Google it -> Find real source -> Cite properly
  ```
  
### **Symptoms**
  - Readers call out fake stats
  - Cited paper doesn't exist
  - Quote attributed to wrong person

## Generic Ai Tone

### **Id**
generic-ai-tone
### **Summary**
AI content sounds like everyone else's AI content
### **Severity**
medium
### **Tools Affected**
  - claude
  - chatgpt
  - jasper
  - copy-ai
### **Situation**
All your content sounds the same as competitors using same tools
### **Why**
  Default AI output has recognizable patterns:
  - "In today's fast-paced world..."
  - "It's important to note that..."
  - Lists of exactly 5 points
  - Hedging language ("can", "may", "might")
  
  If everyone uses AI defaults, everyone sounds identical.
  
### **Solution**
  1. Develop custom prompt templates with your voice
  2. Train on your existing content
  3. Inject strong opinions (AI is neutral by default)
  4. Add personal anecdotes AI can't know
  5. Use AI for structure, write voice yourself
  6. Delete AI-isms in editing
  
### **Symptoms**
  - Content feels generic
  - Sounds like competitors
  - No distinctive voice

## Over Reliance Creativity

### **Id**
over-reliance-creativity
### **Summary**
AI tools can atrophy your creative skills
### **Severity**
medium
### **Tools Affected**
  - all
### **Situation**
Using AI for everything without developing own skills
### **Why**
  If you only use AI:
  - You can't create without it
  - You can't evaluate quality properly
  - You become a "prompt monkey"
  - When AI fails, you're stuck
  
  AI should augment skills, not replace learning them.
  
### **Solution**
  1. Learn fundamentals of each craft
  2. Use AI for speed, not for avoiding learning
  3. Practice without AI regularly
  4. Understand what makes outputs good or bad
  5. Be able to do basic version manually
  
### **Symptoms**
  - Can't work when AI is down
  - Can't explain why something works
  - Quality judgment declining

## Terms Of Service Trap

### **Id**
terms-of-service-trap
### **Summary**
Platform ToS can change and remove your rights
### **Severity**
high
### **Tools Affected**
  - all
### **Situation**
Building business on AI tool that changes terms
### **Why**
  AI platforms are new and volatile:
  - Terms change frequently
  - Output ownership varies by platform
  - Training on your inputs may be default
  - Platforms can shut down or pivot
  
  Building core business on third-party AI is risky.
  
### **Solution**
  1. Read ToS, especially ownership sections
  2. Keep local copies of important outputs
  3. Don't build on a single tool
  4. Check if outputs can be used commercially
  5. Understand training data policies
  6. Have backup tools for critical workflows
  
### **Symptoms**
  - Terms change, lose output rights
  - Platform shuts down
  - Outputs used to train competitors