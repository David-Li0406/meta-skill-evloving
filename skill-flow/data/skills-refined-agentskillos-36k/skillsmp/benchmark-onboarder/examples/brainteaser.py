"""
HELM Scenario: BRAINTEASER

Paper: https://arxiv.org/abs/2310.05057 (EMNLP 2023)
Code: https://github.com/1171-jpg/BrainTeaser

Prompt format:
  Question: {question}
  A. {choice_0}
  B. {choice_1}
  C. {choice_2}
  D. {choice_3}

Prompt source: Standard MC format (paper Section 3.2 uses similar structure)
Fields used: question, answer, distractor1, distractor2, distractor(unsure), label, choice_order
Fields skipped: id, choice_list

Note: Uses tasksource/brainteasers which has SP (Sentence Puzzle) and WP (Word Puzzle) configs.
      This example uses SP; create separate scenario or add subset param for WP.
"""

from datasets import load_dataset
from helm.benchmark.scenarios.scenario import (
    Scenario, Instance, Input, Output, Reference,
    CORRECT_TAG, TEST_SPLIT
)

class BrainteaserScenario(Scenario):
    name = "brainteaser"
    description = "tasksource/brainteasers"
    tags = ["creativity", "lateral_thinking", "multiple_choice"]

    def get_instances(self, output_path):
        # SP = Sentence Puzzle, WP = Word Puzzle
        dataset = load_dataset("tasksource/brainteasers", "SP", split="train")

        instances = []
        for item in dataset:
            # Original choices before shuffling
            original_choices = [
                item['answer'],
                item['distractor1'],
                item['distractor2'],
                item['distractor(unsure)']
            ]

            # Use choice_order to get shuffled order, label indicates correct position
            choice_order = item['choice_order']
            shuffled_choices = [original_choices[i] for i in choice_order]
            correct_idx = item['label']

            # Format prompt
            prompt = f"Question: {item['question']}\n"
            for i, choice in enumerate(shuffled_choices):
                prompt += f"\n{chr(65+i)}. {choice}"

            # HELM MC pattern: all choices are References
            references = []
            for i in range(4):
                letter = chr(65 + i)
                is_correct = (i == correct_idx)
                tags = [CORRECT_TAG] if is_correct else []
                references.append(Reference(Output(text=letter), tags=tags))

            instances.append(Instance(
                input=Input(text=prompt),
                references=references,
                split=TEST_SPLIT
            ))

        return instances
