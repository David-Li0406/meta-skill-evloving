import re
import os
import glob
import ast

def get_attributes_from_file(file_path, class_name):
    """
    Parses a python file to find attributes/methods of a specific class.
    """
    defined_attrs = set()
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found.")
        return defined_attrs
        
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return defined_attrs

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            # Check for inherited bases (Mixins)
            for base in node.bases:
                if isinstance(base, ast.Name):
                    # Recursive check for Mixins if they are imported locally
                    # This is a simple heuristic: assumes mixins are in 'states' dir
                    mixin_name = base.id
                    # Try to find the file for this mixin
                    # Assuming standard naming convention: AuthState -> auth_state.py
                    # Or check imports (complex), let's try standard locations first.
                    
                    # Convert CamelCase to snake_case
                    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', mixin_name)
                    mixin_filename = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower() + ".py"
                    
                    # Look in 'states' subdirectory relative to current file
                    current_dir = os.path.dirname(file_path)
                    states_dir = os.path.join(current_dir, "states")
                    mixin_path = os.path.join(states_dir, mixin_filename)
                    
                    # If not found in /states, try current directory (already in states dir)
                    if not os.path.exists(mixin_path):
                        mixin_path = os.path.join(current_dir, mixin_filename)
                        
                    if os.path.exists(mixin_path):
                        print(f"Scanning Mixin: {mixin_name} at {mixin_path}")
                        mixin_attrs = get_attributes_from_file(mixin_path, mixin_name)
                        print(f"  -> Found {len(mixin_attrs)} attrs in {mixin_name}: {list(mixin_attrs)}")
                        defined_attrs.update(mixin_attrs)

            for body_item in node.body:
                # Variables (annotated assignments)
                if isinstance(body_item, ast.AnnAssign):
                    if isinstance(body_item.target, ast.Name):
                        defined_attrs.add(body_item.target.id)
                # Assignments (e.g. x = 1)
                elif isinstance(body_item, ast.Assign):
                    for target in body_item.targets:
                        if isinstance(target, ast.Name):
                            defined_attrs.add(target.id)
                # Methods
                elif isinstance(body_item, ast.AsyncFunctionDef) or isinstance(body_item, ast.FunctionDef):
                    defined_attrs.add(body_item.name)
                    # Computed vars (@rx.var)
                    for decorator in body_item.decorator_list:
                         if (isinstance(decorator, ast.Attribute) and decorator.attr == 'var') or \
                            (isinstance(decorator, ast.Name) and decorator.id == 'var'):
                             defined_attrs.add(body_item.name)
    return defined_attrs

def get_state_attributes(state_file_path):
    """
    Parses state.py to find all defined attributes and methods in the State class,
    including those inherited from Mixins in ./states/
    """
    return get_attributes_from_file(state_file_path, "State")

def check_pages_for_integrity(app_dir, state_attrs):
    """
    Scans all .py files in pages/ and components/ for State.usage calls
    and verifies if they exist in state_attrs.
    """
    issues = []
    # Regex to find State.attribute usage
    # Matches State.attr_name but stops at ( or . or space or end of line
    # Doesn't handle State.attr.subattr perfectly but good enough for 1st level
    state_usage_pattern = re.compile(r'(?<!rx\.)State\.([a-zA-Z0-9_]+)')
    
    files_to_scan = glob.glob(os.path.join(app_dir, "**/*.py"), recursive=True)
    
    for file_path in files_to_scan:
        if "state.py" in file_path: continue # Skip state definition itself
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.readlines()
            
        for i, line in enumerate(content):
            matches = state_usage_pattern.findall(line)
            for attr in matches:
                # Ignore common internal or false positives if needed
                if attr not in state_attrs:
                    # Check for implicit Reflex setters (set_varname)
                    if attr.startswith("set_"):
                        var_name = attr[4:]
                        if var_name in state_attrs:
                            continue

                    # Double check if it's not a false positive (e.g. State.metrics['key'])
                    issues.append(f"[{os.path.basename(file_path)}:{i+1}] State.{attr} not found in State definition.")

    return issues

def main():
    base_dir = os.getcwd()
    # Adjust paths relative to where script might be run or hardcoded to project struct
    # Assuming script run from project root, or we find biodiagnostico_app
    
    app_root = os.path.join(base_dir, "biodiagnostico_app", "biodiagnostico_app")
    state_file = os.path.join(app_root, "state.py")
    
    if not os.path.exists(state_file):
        print(f"Could not find state.py at {state_file}")
        return

    print(f"Analyzing State definition in {state_file}...")
    state_attrs = get_state_attributes(state_file)
    print(f"Found {len(state_attrs)} attributes/methods in State.")

    print(f"Scanning pages and components in {app_root}...")
    issues = check_pages_for_integrity(app_root, state_attrs)

    if issues:
        print("\n[FAILED] INTEGRITY ISSUES FOUND:")
        for issue in issues:
            print(issue)
        print("\nFix these issues to prevent AttributeError crash loop.")
        exit(1)
    else:
        print("\n[OK] State Integrity Check Passed: All State calls seem to match definitions.")
        exit(0)

if __name__ == "__main__":
    main()
