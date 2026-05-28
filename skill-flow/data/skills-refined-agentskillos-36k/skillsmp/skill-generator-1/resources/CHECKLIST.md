# Skill Authoring Checklist

## Pre‑Upload
- [ ] Name ≤ 64 chars; Description ≤ 200 chars
- [ ] YAML frontmatter includes `name` and `description`
- [ ] Single, focused workflow; "Out of scope" is explicit
- [ ] At least one example input and output
- [ ] Long details moved to `resources/` and referenced from `Skill.md`
- [ ] No secrets or credentials in any file
- [ ] If scripts are included: dependencies declared in frontmatter `dependencies:`

## Post‑Upload
- [ ] Enable the Skill and try prompts that should trigger it
- [ ] Confirm Claude loads the Skill when expected
- [ ] If not, tighten or clarify the description and triggers
- [ ] Iterate on examples until outputs match success criteria

Reference: Claude Skills how‑to https://support.claude.com/en/articles/12512198-how-to-create-custom-skills


