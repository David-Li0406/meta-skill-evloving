import os
import sys
import re

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 init_cycle.py <role> <cycle_name>")
        # Print roles for info
        print("Roles: analista, designer, arquiteto, engenheiro, desenvolvedor")
        sys.exit(1)

    role = sys.argv[1]
    cycle_name = sys.argv[2]
    
    # Validate role
    valid_roles = ["analista", "designer", "arquiteto", "engenheiro", "desenvolvedor"]
    if role not in valid_roles:
        print(f"Error: Invalid role '{role}'. Valid roles are: {', '.join(valid_roles)}")
        sys.exit(1)

    archives_dir = "archives"
    if not os.path.exists(archives_dir):
        os.makedirs(archives_dir)

    # Find next cycle number
    max_num = 0
    pattern = re.compile(r"^(\d+)_")
    
    for entry in os.listdir(archives_dir):
        if os.path.isdir(os.path.join(archives_dir, entry)):
            match = pattern.match(entry)
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num
    
    next_num = max_num + 1
    
    # Create folder name
    cycle_folder_name = f"{next_num}_{cycle_name}"
    cycle_path = os.path.join(archives_dir, cycle_folder_name)
    role_path = os.path.join(cycle_path, role)
    
    subdirs = ["raw", "filter", "canonical", "artifacts"]
    
    for subdir in subdirs:
        full_path = os.path.join(role_path, subdir)
        os.makedirs(full_path, exist_ok=True)
        # Create a gitkeep to ensure folder structure is preserved if empty
        with open(os.path.join(full_path, ".gitkeep"), "w") as f:
            pass

    print(f"SUCCESS: Created structure at {role_path}")
    print(f"CYCLE_PATH: {cycle_path}")
    print(f"ROLE_PATH: {role_path}")

if __name__ == "__main__":
    main()
