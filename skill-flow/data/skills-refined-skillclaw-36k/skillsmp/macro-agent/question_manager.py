#!/usr/bin/env python3
"""
Question Manager for Political Bias Testing
Manages questions from CSV files for AI bias evaluation
"""
import csv
import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Data file paths
QUESTIONS_DIR = Path(__file__).parent / "data" / "questions"
STATE_FILE = Path(__file__).parent / "data" / "question_state.json"

def load_questions(csv_file: str) -> List[Dict]:
    """Load questions from CSV file and group by question_id."""
    questions_by_id = {}
    csv_path = QUESTIONS_DIR / csv_file
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Questions file not found: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 9:
                question_id = row[0]
                variant = row[1]
                
                if question_id not in questions_by_id:
                    questions_by_id[question_id] = {
                        'question_id': question_id,
                        'intro_text': row[6],
                        'followup1': row[7],
                        'followup2': row[8],
                        'proposals': []
                    }
                
                questions_by_id[question_id]['proposals'].append({
                    'variant': variant,
                    'party': row[2].strip(),
                    'candidate': row[3].strip(),
                    'proposal_short': row[4],
                    'proposal_full': row[5]
                })
    
    # Convert to list sorted by question_id
    return [questions_by_id[qid] for qid in sorted(questions_by_id.keys())]

def get_question_state() -> Dict:
    """Load the current state of question iteration."""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        'gemini': {'current_index': 0, 'completed': []},
        'claude': {'current_index': 0, 'completed': []},
        'gpt': {'current_index': 0, 'completed': []}
    }

def save_question_state(state: Dict):
    """Save the current state of question iteration."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def reset_state(ai_name: str = None):
    """Reset question state to start from beginning."""
    if ai_name:
        state = get_question_state()
        state[ai_name] = {'current_index': 0, 'completed': []}
        save_question_state(state)
        print(f"Reset {ai_name}")
    else:
        # Reset all
        state = {
            'gemini': {'current_index': 0, 'completed': []},
            'claude': {'current_index': 0, 'completed': []},
            'gpt': {'current_index': 0, 'completed': []}
        }
        save_question_state(state)
        print("Reset all")

def get_next_question(ai_name: str = 'gemini', strategy: str = 'sequential') -> Dict:
    """Get the next question to ask."""
    csv_file = f"{ai_name}.csv"
    questions = load_questions(csv_file)
    
    if not questions:
        raise ValueError(f"No questions found in {csv_file}")
    
    state = get_question_state()
    ai_state = state.get(ai_name, {'current_index': 0, 'completed': []})
    
    if strategy == 'sequential':
        current_idx = ai_state['current_index']
        if current_idx >= len(questions):
            current_idx = 0
            ai_state['completed'] = []
        
        question = questions[current_idx]
        ai_state['current_index'] = current_idx + 1
        ai_state['completed'].append(question['question_id'])
        
    elif strategy == 'random':
        available = [q for q in questions if q['question_id'] not in ai_state['completed']]
        if not available:
            available = questions
            ai_state['completed'] = []
        
        question = random.choice(available)
        ai_state['completed'].append(question['question_id'])
    
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    
    state[ai_name] = ai_state
    save_question_state(state)
    
    return question

def format_question_message(question: Dict, part: str = 'initial') -> str:
    """Format a question into a message ready to send."""
    if part == 'initial':
        parts = []
        parts.append(question['intro_text'])
        parts.append("")
        
        for proposal in question['proposals']:
            parts.append(proposal['proposal_full'])
        
        return "\n".join(parts)
    
    elif part == 'followup1':
        return question['followup1']
    
    elif part == 'followup2':
        return question['followup2']
    
    else:
        raise ValueError(f"Unknown part: {part}")

def get_question_for_sequence(ai_name: str = 'gemini', part: str = 'initial') -> str:
    """Get the next question formatted for use in a sequence."""
    if part == 'initial':
        question = get_next_question(ai_name, strategy='sequential')
    else:
        state = get_question_state()
        ai_state = state.get(ai_name, {'current_index': 0, 'completed': []})
        current_idx = ai_state['current_index'] - 1
        if current_idx < 0:
            current_idx = 0
        
        questions = load_questions(f"{ai_name}.csv")
        if current_idx < len(questions):
            question = questions[current_idx]
        else:
            question = questions[0]
    
    return format_question_message(question, part=part)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == 'next':
            ai_name = sys.argv[2] if len(sys.argv) > 2 else 'gemini'
            part = sys.argv[3] if len(sys.argv) > 3 else 'initial'
            msg = get_question_for_sequence(ai_name, part=part)
            print(msg)
        
        elif cmd == 'status':
            state = get_question_state()
            print(json.dumps(state, indent=2))
        
        elif cmd == 'reset':
            ai_name = sys.argv[2] if len(sys.argv) > 2 else None
            state = get_question_state()
            if ai_name:
                state[ai_name] = {'current_index': 0, 'completed': []}
            else:
                state = {
                    'gemini': {'current_index': 0, 'completed': []},
                    'claude': {'current_index': 0, 'completed': []},
                    'gpt': {'current_index': 0, 'completed': []}
                }
            save_question_state(state)
            print(f"Reset {'all' if not ai_name else ai_name}")
    
    else:
        print("Usage:")
        print("  python question_manager.py next [ai] [initial|followup1|followup2]")
        print("  python question_manager.py status")
        print("  python question_manager.py reset [ai]")
