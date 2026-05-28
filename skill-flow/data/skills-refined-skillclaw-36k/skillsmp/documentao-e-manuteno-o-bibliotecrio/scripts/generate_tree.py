import os

def generate_tree(startpath, exclude_dirs=None, max_depth=2):
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', 'node_modules', '.web', 'venv', 'env', '.pytest_cache', '.states'}
    
    tree_str = "```\n"
    tree_str += "/\n"
    
    startpath = os.path.abspath(startpath)
    
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if level >= max_depth:
            continue
            
        indent = '│   ' * (level)
        subindent = '│   ' * (level + 1)
        
        # Filter directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        # Don't print root
        if root != startpath:
             tree_str += '{}{}/\n'.format(indent, os.path.basename(root))
        
        # Print files for this dir (limit to important ones or first few to avoid clutter)
        sub_files = [f for f in files if not f.startswith('.')]
        for f in sorted(sub_files):
            # Add descriptions for key files if possible (simplified here)
            desc = ""
            if f == "README.md": desc = " # Documentação Principal"
            elif f == "app.py": desc = " # Entry point"
            
            tree_str += '{}{}{}\n'.format(subindent, f, desc)
            
    tree_str += "```"
    return tree_str

if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass # Python < 3.7
    print(generate_tree("."))
