import sys
import os

TEMPLATE_SYSY = """/* Description:
 *   [Add description here]
 */

int main() {
    return 0;
}
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: init_case.py <target_directory>")
        sys.exit(1)

    target_dir = sys.argv[1]
    
    # 创建目录
    os.makedirs(target_dir, exist_ok=True)
    
    # 路径定义
    paths = {
        "testfile": os.path.join(target_dir, "testfile.txt"),
        "in": os.path.join(target_dir, "in.txt"),
        "ans": os.path.join(target_dir, "ans.txt")
    }

    # 创建 testfile.txt (如果不存在)
    if not os.path.exists(paths["testfile"]):
        with open(paths["testfile"], "w", encoding="utf-8") as f:
            f.write(TEMPLATE_SYSY)
        print(f"[+] Created {paths['testfile']}")
    else:
        print(f"[!] {paths['testfile']} already exists, skipping.")

    # 创建空的 in.txt (如果不存在)
    if not os.path.exists(paths["in"]):
        with open(paths["in"], "w", encoding="utf-8") as f:
            f.write("") # Empty input file
        print(f"[+] Created {paths['in']}")
    
    # 清理旧的 ans.txt
    if os.path.exists(paths["ans"]):
        os.remove(paths["ans"])

    print(f"SUCCESS: Environment initialized in {target_dir}")

if __name__ == "__main__":
    main()