"""
HELM Scenario: ANALOBENCH

Paper: https://arxiv.org/abs/2402.12370 (EMNLP 2024)
Code: https://github.com/jhu-clsp/AnaloBench

Prompt format:
  Which of the following is the most analogous story to the target story?

  Target story: {Sentence}

  {Options}

Prompt source: Paper Section 3
Fields used: Sentence, Options, Label
Fields skipped: Index
"""

from datasets import load_dataset
from helm.benchmark.scenarios.scenario import (
    Scenario, Instance, Input, Output, Reference,
    CORRECT_TAG, TEST_SPLIT
)

class AnalobenchScenario(Scenario):
    name = "analobench"
    description = "jhu-clsp/AnaloBench"
    tags = ["creativity", "analogical_reasoning", "multiple_choice"]

    def get_instances(self, output_path):
        dataset = load_dataset("jhu-clsp/AnaloBench", "T1S1-Subset", split="train")

        instances = []
        for item in dataset:
            # Format prompt (from paper Section 3)
            prompt = f"Which of the following is the most analogous story to the target story?\n\n"
            prompt += f"Target story: {item['Sentence']}\n\n"
            prompt += item['Options']

            # HELM MC pattern: all choices become References
            references = []
            for letter in ['A', 'B', 'C', 'D']:
                is_correct = (letter == item['Label'])
                tags = [CORRECT_TAG] if is_correct else []
                references.append(Reference(Output(text=letter), tags=tags))

            instances.append(Instance(
                input=Input(text=prompt),
                references=references,
                split=TEST_SPLIT
            ))

        return instances
