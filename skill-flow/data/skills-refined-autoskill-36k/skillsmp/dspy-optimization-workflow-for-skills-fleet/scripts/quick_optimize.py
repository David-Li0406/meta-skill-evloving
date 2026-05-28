#!/usr/bin/env python3
"""Quick optimization script with sensible defaults.

Simplified wrapper around DSPy optimization for common use cases.

Usage:
    # GEPA optimization (fast)
    ./scripts/quick_optimize.py --trainset config/training/trainset_v4.json --optimizer gepa
    
    # MIPROv2 optimization (better quality)
    ./scripts/quick_optimize.py --trainset config/training/trainset_v4.json --optimizer miprov2 --auto medium
    
    # With custom output path
    ./scripts/quick_optimize.py --trainset config/training/trainset_v4.json --output config/optimized/my_program.pkl
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import dspy

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from skill_fleet.core.dspy.metrics.enhanced_metrics import comprehensive_metric
from skill_fleet.core.optimization.optimizer import get_lm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_trainset(path: str) -> list[dspy.Example]:
    """Load training set from JSON file."""
    logger.info(f"Loading trainset from {path}")
    
    with open(path, "r") as f:
        data = json.load(f)
    
    examples = []
    for item in data:
        example = dspy.Example(
            task_description=item["task_description"],
            expected_taxonomy_path=item.get("expected_taxonomy_path", ""),
            expected_name=item.get("expected_name", ""),
            expected_skill_style=item.get("expected_skill_style", "comprehensive"),
        ).with_inputs("task_description")
        examples.append(example)
    
    logger.info(f"Loaded {len(examples)} training examples")
    return examples


def create_simple_program():
    """Create simple test program."""
    from skill_fleet.core.dspy.signatures.phase1_understanding import GatherRequirements
    
    class SimpleProgram(dspy.Module):
        def __init__(self):
            super().__init__()
            self.gather = dspy.ChainOfThought(GatherRequirements)
        
        def forward(self, task_description: str):
            return self.gather(task_description=task_description)
    
    return SimpleProgram()


def main():
    parser = argparse.ArgumentParser(description="Quick DSPy optimization")
    parser.add_argument(
        "--trainset",
        default="config/training/trainset_v4.json",
        help="Path to training set JSON",
    )
    parser.add_argument(
        "--optimizer",
        choices=["gepa", "miprov2"],
        default="gepa",
        help="Optimizer to use (default: gepa for speed)",
    )
    parser.add_argument(
        "--auto",
        choices=["light", "medium", "heavy"],
        default="medium",
        help="MIPROv2 auto level (default: medium)",
    )
    parser.add_argument(
        "--output",
        default="config/optimized/quick_optimized.pkl",
        help="Output path for optimized program",
    )
    parser.add_argument(
        "--test-split",
        type=float,
        default=0.2,
        help="Test set split ratio (default: 0.2)",
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Quick DSPy Optimization")
    print("=" * 60)
    print(f"Trainset: {args.trainset}")
    print(f"Optimizer: {args.optimizer}")
    if args.optimizer == "miprov2":
        print(f"Auto level: {args.auto}")
    print(f"Output: {args.output}")
    print("=" * 60)
    
    # Configure DSPy
    logger.info("Configuring DSPy with Gemini 3 Flash...")
    lm = get_lm("gemini-3-flash-preview", temperature=1.0)
    dspy.configure(lm=lm)
    
    # Load data
    examples = load_trainset(args.trainset)
    
    # Split train/test
    split_idx = int(len(examples) * (1 - args.test_split))
    trainset = examples[:split_idx]
    testset = examples[split_idx:]
    
    logger.info(f"Split: {len(trainset)} train, {len(testset)} test")
    
    # Create program
    program = create_simple_program()
    
    # Baseline evaluation
    logger.info("Running baseline evaluation...")
    
    from dspy.evaluate import Evaluate
    evaluator = Evaluate(devset=testset, metric=comprehensive_metric)
    baseline_score = evaluator(program)
    
    logger.info(f"Baseline score: {baseline_score:.3f}")
    
    # Run optimization
    logger.info(f"\nRunning {args.optimizer} optimization...")
    
    if args.optimizer == "gepa":
        optimizer = dspy.GEPA(
            metric=comprehensive_metric,
            num_candidates=5,
            num_iters=2,
        )
        optimized = optimizer.compile(program, trainset=trainset)
    
    else:  # miprov2
        optimizer = dspy.MIPROv2(
            metric=comprehensive_metric,
            auto=args.auto,
            num_threads=8,
        )
        optimized = optimizer.compile(
            program,
            trainset=trainset,
            max_bootstrapped_demos=2,
            max_labeled_demos=2,
            num_candidate_programs=8,
        )
    
    # Evaluate optimized
    logger.info("Evaluating optimized program...")
    optimized_score = evaluator(optimized)
    
    # Results
    improvement = optimized_score - baseline_score
    
    print("\n" + "=" * 60)
    print("Results")
    print("=" * 60)
    print(f"Baseline:  {baseline_score:.3f}")
    print(f"Optimized: {optimized_score:.3f}")
    print(f"Improvement: {improvement:+.3f} ({improvement/baseline_score*100:+.1f}%)")
    print("=" * 60)
    
    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    import pickle
    with open(output_path, "wb") as f:
        pickle.dump(optimized, f)
    
    logger.info(f"\n✅ Saved optimized program to {output_path}")
    
    # Save results
    results_path = output_path.with_suffix(".json")
    results = {
        "optimizer": args.optimizer,
        "auto": args.auto if args.optimizer == "miprov2" else None,
        "trainset_size": len(trainset),
        "testset_size": len(testset),
        "baseline_score": baseline_score,
        "optimized_score": optimized_score,
        "improvement": improvement,
        "improvement_pct": improvement / baseline_score * 100 if baseline_score > 0 else 0,
    }
    
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"✅ Saved results to {results_path}")


if __name__ == "__main__":
    main()
