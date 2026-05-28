import os
import sys
import textwrap


def create_skill(
    name: str,
    description: str,
    instructions: str = "## Instructions\nAdd step-by-step guidance here.\n",
):
    safe_name = name.lower().replace(" ", "-")
    skill_dir = f".claude/skills/{safe_name}"  # Adjust for personal: ~/.claude/skills/
    os.makedirs(skill_dir, exist_ok=True)

    skill_md = textwrap.dedent(
        f"""\
    ---
    name: {safe_name}
    description: {description}
    ---
    # {name}

    {instructions}

    ## Examples
    Add usage examples here.
    """
    )

    with open(f"{skill_dir}/SKILL.md", "w") as f:
        f.write(skill_md)

    print(f"Created new skill at {skill_dir}")
    print("Edit SKILL.md to refine, then add supporting files as needed.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python scripts/scaffold_skill.py 'Skill Name' 'Brief description with triggers'"
        )
        sys.exit(1)
    name = sys.argv[1]
    desc = sys.argv[2]
    create_skill(name, desc)
