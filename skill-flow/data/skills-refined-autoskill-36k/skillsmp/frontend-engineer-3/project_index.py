import os
import json

def generate_index():
    base_dir = r"d:\Alders360"
    ignore_dirs = {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}
    
    project_map = {}
    
    for root, dirs, files in os.walk(base_dir):
        # Filter ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == ".": rel_path = "root"
        
        # Keep only relevant files (code, config, docs)
        relevant_files = [f for f in files if f.endswith(('.py', '.ts', '.tsx', '.css', '.md', '.json'))]
        
        if relevant_files:
            project_map[rel_path] = relevant_files

    # Output as a compressed Markdown Index
    with open(os.path.join(base_dir, ".agent", "project_index.md"), "w", encoding="utf-8") as f:
        f.write("# 📂 Project Codebase Index\n\n")
        f.write("> [!NOTE]\n")
        f.write("> Use this index to find files quickly without multiple `list_dir` calls.\n\n")
        for folder, files in sorted(project_map.items()):
            f.write(f"### 📁 `{folder}`\n")
            f.write("- " + ", ".join([f"`{file}`" for file in files]) + "\n\n")
            
    print(f"Project index generated at: {os.path.join(base_dir, '.agent', 'project_index.md')}")

if __name__ == "__main__":
    generate_index()
