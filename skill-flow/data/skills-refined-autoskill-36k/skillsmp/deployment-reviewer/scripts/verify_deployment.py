import os
from pathlib import Path

def check_file(path, description):
    if os.path.exists(path):
        print(f"[OK] Found {description}: {path}")
        return True
    else:
        print(f"[MISSING] Could not find {description}: {path}")
        return False

def check_content(path, content, description):
    if not os.path.exists(path):
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        if content in file_content:
            print(f"[OK] {description} found in {os.path.basename(path)}")
            return True
        else:
            print(f"[WARNING] {description} NOT found in {os.path.basename(path)}")
            return False

def main():
    base_dir = Path(os.getcwd())
    dashboard_dir = base_dir / "dashboard"
    
    print("--- Verifying Deployment Configuration ---")
    
    # Check 1: Key Files
    check_file(dashboard_dir / "package.json", "Package Config")
    check_file(dashboard_dir / "vite.config.ts", "Vite Config")
    check_file(dashboard_dir / "index.html", "Entry HTML")
    
    # Check 2: React Entry Point
    index_html = dashboard_dir / "index.html"
    check_content(index_html, 'src="/src/index.tsx"', "React Entry Point Script")
    check_content(index_html, 'id="root"', "Root Div")
    
    # Check 3: Env Vars
    env_file = dashboard_dir / ".env"
    if check_file(env_file, "Environment File"):
        check_content(env_file, "VITE_SUPABASE_URL", "Supabase URL")
        check_content(env_file, "VITE_SUPABASE_ANON_KEY", "Supabase Key")

if __name__ == "__main__":
    main()
