import os

skill_name = "designing-nextjs-ui"
required_files = [
    "SKILL.md",
    "references/ui-patterns.md",
    "references/visual-effects.md",
    "references/layout-patterns.md",
    "references/typography-advanced.md"
]

def verify():
    print(f"Verifying {skill_name}...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    missing = []
    for f in required_files:
        path = os.path.join(base_dir, f)
        if not os.path.exists(path):
            missing.append(f)
    
    if missing:
        print(f"Missing files: {missing}")
        exit(1)
    
    print(f"[OK] {skill_name} skill ready")

if __name__ == "__main__":
    verify()
