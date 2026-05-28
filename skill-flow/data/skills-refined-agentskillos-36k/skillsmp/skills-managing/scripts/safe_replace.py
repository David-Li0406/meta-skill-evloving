import os

def safe_replace_in_files(directory):
    # 文档定义的覆盖范围：支持全量文本文件重塑
    target_extensions = ('.md', '.py', '.json', '.js', '.txt', '.css', '.html')
    replacements = {
        'Claude': 'The Agent',
        'Anthropic': 'Antigravity',
        'claude': 'the agent',
        'anthropic': 'antigravity'
    }
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(target_extensions):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    for src, target in replacements.items():
                        new_content = new_content.replace(src, target)
                    
                    if content != new_content:
                        with open(path, 'w', encoding='utf-8', newline='') as f:
                            f.write(new_content)
                        print(f"Updated: {path}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    # 此处路径需根据实际环境调整
    target_dir = r'.agent/skills'
    safe_replace_in_files(target_dir)
