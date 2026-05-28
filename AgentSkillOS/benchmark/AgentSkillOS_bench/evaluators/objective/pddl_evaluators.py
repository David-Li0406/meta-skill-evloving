"""
PDDL plan validation evaluators.

Provides objective validation of PDDL plans against domain and problem files.
"""
import re
import subprocess
from pathlib import Path
from typing import Dict, Any, Tuple, Set, List, Optional

from ...registry import evaluator
from ...utils.file_utils import resolve_path, read_file


def parse_pddl_predicates(text: str) -> Set[str]:
    """Parse predicates from PDDL init section."""
    predicates = set()
    # Match predicates like (on crate0 pallet0) or (clear crate0)
    pattern = r'\((\w+(?:\s+\w+)*)\)'
    for match in re.finditer(pattern, text):
        pred = match.group(1).lower()
        # Skip keywords
        if not pred.startswith(('define', 'domain', 'problem', 'objects',
                                 'init', 'goal', 'and', 'or', 'not')):
            predicates.add(pred)
    return predicates


def parse_pddl_objects(text: str) -> Dict[str, str]:
    """Parse objects from PDDL problem file, return name->type mapping."""
    objects = {}
    # Find :objects section
    obj_match = re.search(r'\(:objects\s+(.*?)\)', text, re.DOTALL | re.IGNORECASE)
    if obj_match:
        obj_text = obj_match.group(1)
        # Parse simple object list (without types)
        for name in obj_text.split():
            name = name.strip().lower()
            if name and not name.startswith(('-', ':')):
                objects[name] = 'object'
    return objects


def parse_plan_actions(plan_text: str) -> List[Tuple[str, List[str]]]:
    """Parse plan file into list of (action_name, [params]).

    Supports two formats:
    - Space-separated: ``pick-up a`` or ``(pick-up a)``
    - Function-call:   ``pick-up(a)`` or ``stack(c, a)``
    """
    actions = []
    for line in plan_text.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith(';'):
            continue
        # Remove outer parentheses for PDDL-style "(pick-up a)"
        if line.startswith('(') and line.endswith(')') and '(' not in line[1:]:
            line = line[1:-1]
        # Handle function-call format: "action(param1, param2)"
        fc_match = re.match(r'([\w-]+)\(([^)]*)\)', line)
        if fc_match:
            action_name = fc_match.group(1).lower()
            params_str = fc_match.group(2).strip()
            if params_str:
                params = [p.strip().lower() for p in params_str.split(',')]
            else:
                params = []
            actions.append((action_name, params))
            continue
        # Space-separated format: "pick-up a" or "(pick-up a)"
        line = line.strip('()')
        parts = line.lower().split()
        if parts:
            action_name = parts[0]
            params = parts[1:] if len(parts) > 1 else []
            actions.append((action_name, params))
    return actions


def _extract_balanced_paren(text: str, start: int) -> str:
    """Extract text inside balanced parentheses starting at ``text[start]``."""
    if start >= len(text) or text[start] != '(':
        return ''
    depth = 0
    for i in range(start, len(text)):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
    return text[start + 1:]


def parse_domain_actions(domain_text: str) -> Dict[str, Dict]:
    """Parse domain file to extract action definitions."""
    actions = {}

    # Split by :action
    parts = re.split(r'\(:action\s+', domain_text, flags=re.IGNORECASE)

    for part in parts[1:]:  # Skip first empty part
        # Get action name (supports hyphens like pick-up, put-down)
        name_match = re.match(r'([\w-]+)', part)
        if not name_match:
            continue
        action_name = name_match.group(1).lower()

        # Parse parameters
        params_match = re.search(r':parameters\s*\((.*?)\)', part, re.DOTALL | re.IGNORECASE)
        params = []
        if params_match:
            params_text = params_match.group(1)
            for p in params_text.split():
                p = p.strip()
                if p.startswith('?'):
                    params.append(p.lower())

        # Parse preconditions
        precond_match = re.search(r':precondition\s*\(and\s*(.*?)\)\s*:effect', part, re.DOTALL | re.IGNORECASE)
        if not precond_match:
            precond_match = re.search(r':precondition\s*(\(.*?\))\s*:effect', part, re.DOTALL | re.IGNORECASE)
        preconditions = []
        if precond_match:
            precond_text = precond_match.group(1)
            for pred in re.finditer(r'\((\w+(?:\s+[\?\w]+)*)\)', precond_text):
                preconditions.append(pred.group(1).lower())

        # Parse effects using balanced-paren extraction (handles nested parens)
        effect_pos = re.search(r':effect\s*', part, re.IGNORECASE)
        add_effects = []
        del_effects = []
        if effect_pos:
            # Find the opening '(' after :effect
            open_idx = part.find('(', effect_pos.end())
            if open_idx != -1:
                effect_text = _extract_balanced_paren(part, open_idx)
                # Strip outer 'and' wrapper if present
                effect_inner = effect_text.strip()
                if effect_inner.lower().startswith('and'):
                    effect_inner = effect_inner[3:]
                # Find deletions (not ...)
                for del_pred in re.finditer(r'\(not\s*\((\w+(?:\s+[\?\w]+)*)\)\)', effect_inner, re.IGNORECASE):
                    del_effects.append(del_pred.group(1).lower())
                # Find additions (predicates not inside 'not')
                clean_text = re.sub(r'\(not\s*\([^)]+\)\)', '', effect_inner)
                for add_pred in re.finditer(r'\((\w+(?:\s+[\?\w]+)*)\)', clean_text):
                    add_effects.append(add_pred.group(1).lower())

        actions[action_name] = {
            'params': params,
            'preconditions': preconditions,
            'add_effects': add_effects,
            'del_effects': del_effects
        }

    return actions


def substitute_params(predicate: str, param_map: Dict[str, str]) -> str:
    """Substitute parameters in a predicate."""
    parts = predicate.split()
    result = [parts[0]]  # action/predicate name
    for p in parts[1:]:
        if p.startswith('?'):
            result.append(param_map.get(p, p))
        else:
            result.append(p)
    return ' '.join(result)


def simulate_plan(domain_text: str, problem_text: str, plan_actions: List[Tuple[str, List[str]]]) -> Tuple[bool, str, Set[str]]:
    """
    Simulate a PDDL plan and check if it reaches the goal.

    Returns: (success, message, final_state)
    """
    # Parse domain actions
    domain_actions = parse_domain_actions(domain_text)

    # Parse initial state from problem
    init_match = re.search(r'\(:init\s+(.*?)\)\s*\(:goal', problem_text, re.DOTALL | re.IGNORECASE)
    if not init_match:
        return False, "Cannot parse :init section from problem file", set()

    init_text = init_match.group(1)
    state = set()
    for match in re.finditer(r'\((\w+(?:\s+\w+)*)\)', init_text):
        pred = match.group(1).lower()
        state.add(pred)

    # Parse goal state
    goal_match = re.search(r'\(:goal\s*\(and\s*(.*?)\)\s*\)', problem_text, re.DOTALL | re.IGNORECASE)
    if not goal_match:
        goal_match = re.search(r'\(:goal\s*(\(.*?\))\s*\)', problem_text, re.DOTALL | re.IGNORECASE)

    goal_predicates = set()
    if goal_match:
        goal_text = goal_match.group(1)
        for match in re.finditer(r'\((\w+(?:\s+\w+)*)\)', goal_text):
            pred = match.group(1).lower()
            goal_predicates.add(pred)

    if not goal_predicates:
        return False, "Cannot parse :goal section from problem file", set()

    # Simulate each action
    for i, (action_name, params) in enumerate(plan_actions):
        if action_name not in domain_actions:
            return False, f"Step {i+1}: Unknown action '{action_name}'", state

        action_def = domain_actions[action_name]

        # Create parameter mapping
        if len(params) != len(action_def['params']):
            return False, f"Step {i+1}: Action '{action_name}' expects {len(action_def['params'])} params, got {len(params)}", state

        param_map = {action_def['params'][j]: params[j] for j in range(len(params))}

        # Check preconditions
        for precond in action_def['preconditions']:
            grounded = substitute_params(precond, param_map)
            # Handle negated preconditions
            if grounded.startswith('not '):
                actual_pred = grounded[4:].strip()
                if actual_pred in state:
                    return False, f"Step {i+1}: Precondition 'not ({actual_pred})' failed - predicate is true", state
            else:
                if grounded not in state:
                    return False, f"Step {i+1}: Precondition '({grounded})' failed - predicate not in state", state

        # Apply effects
        for del_eff in action_def['del_effects']:
            grounded = substitute_params(del_eff, param_map)
            state.discard(grounded)

        for add_eff in action_def['add_effects']:
            grounded = substitute_params(add_eff, param_map)
            state.add(grounded)

    # Check if goal is reached
    missing_goals = goal_predicates - state
    if missing_goals:
        return False, f"Goal not reached. Missing: {list(missing_goals)[:5]}", state

    return True, "Plan valid - goal reached", state


@evaluator("pddl_plan_validates")
async def eval_pddl_plan_validates(workspace: Path, op_args: Dict[str, Any],
                                    value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Objectively validate a PDDL plan against domain and problem files.

    op_args:
        plan_path: Path to the plan file (e.g., "solution.plan")
        domain_path: Path to domain PDDL file (e.g., "depot_domain.pddl")
        problem_path: Path to problem PDDL file (e.g., "depot_problem.pddl")

    Validates:
        1. All actions in plan exist in domain
        2. All action preconditions are satisfied at execution time
        3. Final state satisfies all goal conditions
    """
    plan_path = op_args.get("plan_path", "solution.plan")
    domain_path = op_args.get("domain_path")
    problem_path = op_args.get("problem_path")

    if not domain_path or not problem_path:
        return False, "domain_path and problem_path are required in op_args"

    # Read files
    plan_text = read_file(workspace, plan_path)
    if plan_text is None:
        return False, f"Cannot read plan file: {plan_path}"

    domain_text = read_file(workspace, domain_path)
    if domain_text is None:
        return False, f"Cannot read domain file: {domain_path}"

    problem_text = read_file(workspace, problem_path)
    if problem_text is None:
        return False, f"Cannot read problem file: {problem_path}"

    # Parse plan
    plan_actions = parse_plan_actions(plan_text)
    if not plan_actions:
        return False, "Plan file is empty or has no valid actions"

    # Simulate and validate
    try:
        success, message, final_state = simulate_plan(domain_text, problem_text, plan_actions)
        return success, message
    except Exception as e:
        return False, f"Validation error: {str(e)}"


@evaluator("pddl_plan_step_count")
async def eval_pddl_plan_step_count(workspace: Path, op_args: Dict[str, Any],
                                     value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Check that PDDL plan has a step count within expected range.

    op_args:
        plan_path: Path to the plan file
        min_steps: Minimum expected steps (inclusive)
        max_steps: Maximum expected steps (inclusive)
    """
    plan_path = op_args.get("plan_path", "solution.plan")
    min_steps = op_args.get("min_steps", 1)
    max_steps = op_args.get("max_steps", 1000)

    plan_text = read_file(workspace, plan_path)
    if plan_text is None:
        return False, f"Cannot read plan file: {plan_path}"

    plan_actions = parse_plan_actions(plan_text)
    step_count = len(plan_actions)

    if step_count < min_steps:
        return False, f"Plan has {step_count} steps, minimum required is {min_steps}"
    if step_count > max_steps:
        return False, f"Plan has {step_count} steps, maximum allowed is {max_steps}"

    return True, f"Plan has {step_count} steps (valid range: {min_steps}-{max_steps})"


def parse_8puzzle_moves(plan_text: str) -> List[Tuple[int, str]]:
    """
    Parse 8-puzzle plan file into list of (tile, direction) moves.

    Supports formats:
    - "move 7 down" or "7 down"
    - "slide 3 left" or "3 left"
    - "up", "down", "left", "right" (move tile into blank)
    - "1", "2", ..., "8" (move that tile)
    """
    moves = []
    for line in plan_text.strip().split('\n'):
        line = line.strip().lower()
        if not line or line.startswith(';') or line.startswith('#'):
            continue

        # Remove common prefixes
        for prefix in ['move ', 'slide ', 'step ']:
            if line.startswith(prefix):
                line = line[len(prefix):]

        parts = line.split()
        if not parts:
            continue

        # Try to parse "tile direction" format
        if len(parts) >= 2:
            try:
                tile = int(parts[0])
                direction = parts[1]
                if direction in ('up', 'down', 'left', 'right', 'u', 'd', 'l', 'r'):
                    # Normalize direction
                    dir_map = {'u': 'up', 'd': 'down', 'l': 'left', 'r': 'right'}
                    direction = dir_map.get(direction, direction)
                    moves.append((tile, direction))
                    continue
            except ValueError:
                pass

        # Try direction only (tile is inferred from blank position)
        if len(parts) == 1:
            direction = parts[0]
            dir_map = {'u': 'up', 'd': 'down', 'l': 'left', 'r': 'right'}
            direction = dir_map.get(direction, direction)
            if direction in ('up', 'down', 'left', 'right'):
                moves.append((0, direction))  # 0 means "infer from blank"
                continue
            # Could be just a tile number
            try:
                tile = int(parts[0])
                moves.append((tile, 'infer'))  # direction to be inferred
                continue
            except ValueError:
                pass

    return moves


def simulate_8puzzle(initial_state: List[int], moves: List[Tuple[int, str]],
                     goal_state: List[int]) -> Tuple[bool, str, List[int]]:
    """
    Simulate 8-puzzle moves and check if goal is reached.

    State is a list of 9 integers (0-8), where 0 represents the blank.
    Position indices: 0 1 2 / 3 4 5 / 6 7 8

    Returns: (success, message, final_state)
    """
    state = list(initial_state)

    # Direction deltas (row, col)
    direction_delta = {
        'up': (-1, 0),    # tile moves up into blank (blank was above)
        'down': (1, 0),   # tile moves down into blank
        'left': (0, -1),  # tile moves left into blank
        'right': (0, 1),  # tile moves right into blank
    }

    for i, (tile, direction) in enumerate(moves):
        blank_pos = state.index(0)
        blank_row, blank_col = blank_pos // 3, blank_pos % 3

        if direction == 'infer':
            # Find the tile and determine direction
            if tile not in state or tile == 0:
                return False, f"Step {i+1}: Invalid tile {tile}", state
            tile_pos = state.index(tile)
            tile_row, tile_col = tile_pos // 3, tile_pos % 3

            # Check if tile is adjacent to blank
            row_diff = blank_row - tile_row
            col_diff = blank_col - tile_col

            if abs(row_diff) + abs(col_diff) != 1:
                return False, f"Step {i+1}: Tile {tile} is not adjacent to blank", state

            # Swap
            state[blank_pos], state[tile_pos] = state[tile_pos], state[blank_pos]

        elif tile == 0:
            # Direction only - move tile from opposite direction into blank
            # "up" means a tile below the blank moves up
            dr, dc = direction_delta[direction]
            # The tile to move is in the OPPOSITE direction from blank
            tile_row = blank_row - dr
            tile_col = blank_col - dc

            if not (0 <= tile_row < 3 and 0 <= tile_col < 3):
                return False, f"Step {i+1}: No tile to move {direction} into blank", state

            tile_pos = tile_row * 3 + tile_col
            state[blank_pos], state[tile_pos] = state[tile_pos], state[blank_pos]

        else:
            # Tile + direction: move specified tile in specified direction
            if tile not in state or tile == 0:
                return False, f"Step {i+1}: Invalid tile {tile}", state

            tile_pos = state.index(tile)
            tile_row, tile_col = tile_pos // 3, tile_pos % 3

            dr, dc = direction_delta[direction]
            new_row, new_col = tile_row + dr, tile_col + dc

            if not (0 <= new_row < 3 and 0 <= new_col < 3):
                return False, f"Step {i+1}: Tile {tile} cannot move {direction} (out of bounds)", state

            new_pos = new_row * 3 + new_col
            if state[new_pos] != 0:
                return False, f"Step {i+1}: Tile {tile} cannot move {direction} (position not blank)", state

            state[blank_pos], state[tile_pos] = state[tile_pos], state[blank_pos]

    # Check goal
    if state == goal_state:
        return True, f"Plan valid - goal reached in {len(moves)} moves", state
    else:
        return False, f"Goal not reached. Final: {state}, Expected: {goal_state}", state


@evaluator("puzzle_8_plan_validates")
async def eval_puzzle_8_plan_validates(workspace: Path, op_args: Dict[str, Any],
                                        value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Objectively validate an 8-puzzle plan.

    op_args:
        plan_path: Path to plan file (default: "puzzle_plan.txt")
        initial_state: Initial puzzle state as list of 9 integers (0=blank)
                      Default: [7,2,4,5,0,6,8,3,1] for "7 2 4 / 5 _ 6 / 8 3 1"
        goal_state: Goal puzzle state as list of 9 integers
                   Default: [1,2,3,4,5,6,7,8,0] for "1 2 3 / 4 5 6 / 7 8 _"
        min_moves: Minimum expected moves (default: 14, Manhattan distance)
        max_moves: Maximum allowed moves (default: 50)

    Validates:
        1. All moves are legal (tile adjacent to blank)
        2. Final state matches goal state
        3. Move count is within expected range
    """
    plan_path = op_args.get("plan_path", "puzzle_plan.txt")
    initial_state = op_args.get("initial_state", [7, 2, 4, 5, 0, 6, 8, 3, 1])
    goal_state = op_args.get("goal_state", [1, 2, 3, 4, 5, 6, 7, 8, 0])
    min_moves = op_args.get("min_moves", 14)
    max_moves = op_args.get("max_moves", 50)

    plan_text = read_file(workspace, plan_path)
    if plan_text is None:
        return False, f"Cannot read plan file: {plan_path}"

    moves = parse_8puzzle_moves(plan_text)
    if not moves:
        return False, "Plan file is empty or has no valid moves"

    if len(moves) < min_moves:
        return False, f"Plan has {len(moves)} moves, minimum required is {min_moves}"
    if len(moves) > max_moves:
        return False, f"Plan has {len(moves)} moves, maximum allowed is {max_moves}"

    try:
        success, message, final_state = simulate_8puzzle(initial_state, moves, goal_state)
        if success:
            return success, message

        # Direction-only plans are ambiguous: "down" could mean "blank moves
        # down" (solver convention) or "tile moves down" (evaluator convention).
        # If the first attempt failed and the plan uses direction-only moves,
        # retry with flipped directions.
        has_direction_only = any(tile == 0 and d != 'infer' for tile, d in moves)
        if has_direction_only:
            flip = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
            flipped_moves = [
                (tile, flip.get(d, d)) if tile == 0 and d != 'infer' else (tile, d)
                for tile, d in moves
            ]
            success2, message2, final_state2 = simulate_8puzzle(
                initial_state, flipped_moves, goal_state
            )
            if success2:
                return success2, message2

        # Both conventions failed — return the original error
        return success, message
    except Exception as e:
        return False, f"Validation error: {str(e)}"
