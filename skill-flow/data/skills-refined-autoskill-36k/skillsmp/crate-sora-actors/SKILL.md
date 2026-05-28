---
name: crate_sora_actors
description: instructions how to create & store sora actors so they can be used in openpromo.
---

# Role
you will use Chrome to automate the tool and maintain sora actors/persona/characters so that they're reusbale in OpenPromo.

# Terms & defs
sora character: on sora.com, you can create text2video via prompt to create actors, then you can click three-dot 

## instructions for creating prompt to create a new sora actor
<<role>>
im trying to create a ugc farm by using sora2 to create multiple ugc actors, they are generic enough to use to use in downstream video generation for creating ugc ads in batch.

your goal is to give me prompts for those, ensure the actors are different each time w/ demographics, scenarios, etc, suitable/covering most revenue-dense industry/small businesses, are are often yielding high conversions in tiktok/instagram shorts, etc. specifyc those details, and direclty give me the prompt to copy paste and reuse.

prompt should be, e.g. tiktok ugc style, 25yo mixed race,  shot on iphone, etc. in a cozy kitcehn, etc structure, these are to shwocase the persona/settings and later they will be holding products

and because the video will be added to DB to showcase, specify the dialogue "hi, i'm the ai actor on openpromo to help you create winning ads" in the prompt!

the workflow is: you give me a prompt for the avatar -> i create a sora video -> create character from that sora video, got a @handle -> ingest it to our DB for actors

// example of realistic ugc prompts!!
TikTok UGC style vertical video, 9:16 aspect ratio. 42 year old South Asian man with short salt-and-pepper hair, neatly trimmed beard, warm brown eyes, friendly confident smile showing slight crow's feet. Wearing casual navy blue henley shirt. Seated at modern minimalist home office desk, soft golden morning light from window, monstera plant in background, clean aesthetic. Direct eye contact to camera, professional yet approachable energy, slight head tilts while speaking. Speaking to camera: "Hi, I'm an AI actor on OpenPromo to help you create winning ads." Shot on iPhone 15 Pro, 24mm front camera, 4K resolution, 30fps. Handheld natural micro-movements. Realistic skin texture with subtle laugh lines, natural skin tone variation, visible pores. Soft ambient room tone. &lt;neg_prompt&gt;cartoon, anime, unrealistic, blurry, low resolution, distorted face, extra limbs, watermark, text overlay, oversaturated, artificial lighting, studio backdrop, plastic skin, uncanny valley&lt;/neg_prompt&gt;


<prompt> TikTok UGC style vertical video, 9:16 aspect ratio. 27 year old Middle Eastern woman with long dark wavy hair, olive skin, thick natural brows, subtle winged liner, elegant effortless beauty, soft closed-lip smile. Wearing white linen button-down slightly oversized. Standing near hotel-style window with sheer drapes, neutral cream armchair visible, golden hour light casting warm glow, chic minimalist travel aesthetic. Direct eye contact to camera, polished yet approachable energy, gentle head tilt while speaking. Speaking to camera: "Hi, I'm an AI actor on OpenPromo to help you create winning ads." Shot on iPhone 15 Pro, 24mm front camera, 4K resolution, 30fps. Handheld soft sway, natural hair movement catching light. Realistic skin with natural olive undertones, visible texture on forehead, soft undereye tone, authentic golden highlight on cheekbones. Quiet interior ambiance with faint city hum through window. </prompt> <neg_prompt> Heavy glam makeup, influencer ring light, studio beauty lighting, green screen hotel room, static tripod shot, stock travel imagery, facetune smoothing, plastic skin, uncanny symmetry, overly posed luxury aesthetic, robotic expression, fake window light, oversaturated warm tones, lip sync errors, magazine editorial look </neg_prompt> <specs> Resolution: 4K (2160x3840) Duration: 5-7 seconds Style: Effortless elevated travel aesthetic Industry fit: Jewelry brands, luggage, travel apps, boutique hotels, wellness retreats, luxury skincare, meditation apps, perfume, watches, premium subscriptions </specs>





<<Rules>>
1. detailed prompt btu not too long!! 1500 char most!!, declarative prompts, w/ neg_prompt section in xml formats to sepcify unwanted; promot should be coveirng realisitc elements, e.g. shot on iphone 15 pro, 35mm, natural slight imperfections/motion blurs. etc.
2. explicit prompt for high-resolution/clarity!!


# Task
there're differnt tasks you will execute, follow the instructions based on the task you're given.
## Task1 -- create new sora actor
instructions
0. goto https://sora.chatgpt.com/profile, type in the prompt follwoing above instrucitos for new char creation, ensure portrait + 10s setting, then generate.
1. when video done. it's available at https://sora.chatgpt.com/drafts, click on it, click three-dot btn on top right. if there's NO create character, skip, this one might not be available. If yes, click the btn to open create character flow. DO NOT create it it's not realisitc!! we only want realistic avatar. if not realistic, delete it. and start again.
2. by default it will trim couple seconds, that's fine, you can click next. This may/may not fail due to content violatin policy. try clcik it agian if it failed, skip this creation.
3. if passed, follow instruction, make this actor public, name it as @openpromo.actor.xxx, where `xxx` is random string.


## Task 2 -- add actor to openpromo's actor registry.
in our persona infra, we got different types of persona, one of which is sora actors. this requires u to mirror the sora2 characters to our persona lib so we can store them.
0. similar to task1, check exisitng sora2 characters.
1. compare that to list all personas that are sora using the mcp tool.
2. for missing ones that're relistic ugc char, create persona via mcp tool so that. The key for creating sora2 character is via thumbnail url as well as demo vidoe url. you should inspect the sora2.com canvas elemnt to grab the right CDN url to those!!.
3. verify that newly created persona exist in DB


## Task 3 -- Automated URL Extraction Script

**Script Location**: `./scripts/extract-character.js`

### Method: Console Log Extraction (Recommended)

Browser automation blocks direct JavaScript responses, so we use console logging to capture URLs.

**Workflow**:
1. Navigate to character page: `https://sora.chatgpt.com/profile/openpromo.actor.xxx`
2. Run extraction script via browser automation
3. Use `read_console_messages` tool with pattern `HANDLE|NAME|THUMB|VIDEO` to capture logged data
4. Parse console output and create persona

**Simplified extraction script** (logs to console):
```javascript
async function extract() {
  const h = window.location.pathname.split("/").pop();
  const n = document.querySelector("h1")?.textContent?.trim() || "";
  const img = document.querySelector('img[class*="mask-blossom"]');
  const t = img?.src || "";

  const btn = Array.from(document.querySelectorAll("button")).find(b => b.textContent.includes("Edit character"));
  if (btn) {
    btn.click();
    await new Promise(r => setTimeout(r, 800));
    const v = document.querySelector("video");
    const vu = v?.src || v?.currentSrc || "";

    console.log("HANDLE:", h);
    console.log("NAME:", n);
    console.log("THUMB:", t);
    console.log("VIDEO:", vu);

    return {handle: h, name: n, thumb: t, video: vu};
  }
}
extract();
```

**What it extracts**:
- Character handle (from URL) → use as `soraHandle`
- Character name (from h1) → use as `name`
- Thumbnail URL (from profile avatar) → use as `avatarImageUrl`
- Demo video URL (from edit dialog video element) → use as `demoVideoUrl`

**Example console output**:
```
HANDLE: openpromo.actor.jac
NAME: Sunny Backyard Buddy
THUMB: https://videos.openai.com/az/files/...
VIDEO: https://videos.openai.com/az/files/...
```

Use the extracted URLs when calling `createPersona` MCP tool with `type: "sora"`.
