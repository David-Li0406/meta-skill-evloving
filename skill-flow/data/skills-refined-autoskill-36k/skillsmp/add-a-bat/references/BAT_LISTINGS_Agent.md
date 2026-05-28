# Master Bat Listing Prompt

This master prompt organizes the three major prompts required to create a new bat
for Bat Digest's database. When complete, it will create a bat, its ratings, and images
correctly linked and stored in the bats and images yaml files.

## Prompt Order

Your task is to follow these three prompts in order. Do not skip.
Read each prompt fully before taking action and stop if required inputs are missing.

PROMPTS
```
AGENTS/Content_Creation/BAT_LISTINGS_Agent/Bat_Entry_Agent.md
AGENTS/Content_Creation/BAT_LISTINGS_Agent/Bat_Ratings_Agent.md
AGENTS/Content_Creation/BAT_LISTINGS_Agent/Bat_Image_Attach_Agent.md
```

yaml files used:

```
data/bats.yaml
data/images.yaml
```

---

## Notes and Constraints

* When in doubt, as the prompts suggest, ask the user to get correct information.
* Do **not** invent specifications when reliable data is unavailable.
* Ratings should follow the `Bat_Ratings_Agent.md` guidance (same-year variants first).

