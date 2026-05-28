import os
import datetime
import re
import sys

def create_task_file():
    # Get current date
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    
    # Define directory
    tmp_dir = '.tmp'
    
    # Create directory if it doesn't exist
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
        print(f"Created directory: {tmp_dir}")
    
    # Find existing files to determine sequence
    pattern = re.compile(f"task-{date_str}-(\d+)\.md")
    max_seq = 0
    
    for filename in os.listdir(tmp_dir):
        match = pattern.match(filename)
        if match:
            seq = int(match.group(1))
            if seq > max_seq:
                max_seq = seq
    
    # Next sequence
    next_seq = max_seq + 1
    
    # Create new file
    new_filename = f"task-{date_str}-{next_seq}.md"
    new_filepath = os.path.join(tmp_dir, new_filename)
    
    with open(new_filepath, 'w') as f:
        pass # Create empty file
    
    print(f"Created task file: {new_filepath}")

if __name__ == "__main__":
    create_task_file()
