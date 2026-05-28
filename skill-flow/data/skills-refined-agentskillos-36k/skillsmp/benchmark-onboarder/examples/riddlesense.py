"""
HELM Scenario: RIDDLESENSE

Paper: https://aclanthology.org/2021.findings-acl.131/ (ACL-IJCNLP 2021)
Code: https://github.com/INK-USC/RiddleSense

Prompt format:
  Question: {question}
  A. {choice_0}
  B. {choice_1}
  ...

Prompt source: Standard CommonsenseQA-style MC format (paper uses same approach)
Fields used: question, choices (label + text), answerKey
Fields skipped: none

Note: Test split has no labels; using validation split instead.
"""

from datasets import load_dataset
from helm.benchmark.scenarios.scenario import (
    Scenario, Instance, Input, Output, Reference,
    CORRECT_TAG, TEST_SPLIT
)

class RiddlesenseScenario(Scenario):
    name = "riddlesense"
    description = "INK-USC/riddle_sense"
    tags = ["creativity", "commonsense_reasoning", "riddles", "multiple_choice"]

    def get_instances(self, output_path):
        # Note: test split has no labels; using validation for HELM evaluation
        dataset = load_dataset(
            "INK-USC/riddle_sense",
            split="validation",
            trust_remote_code=True
        )

        instances = []
        for item in dataset:
            # Format prompt (standard MC format)
            prompt = f"Question: {item['question']}\n"

            # Add answer choices
            labels = item['choices']['label']
            texts = item['choices']['text']
            for label, text in zip(labels, texts):
                prompt += f"\n{label}. {text}"

            # HELM MC pattern: all choices become References
            references = []
            for label in labels:
                is_correct = (label == item['answerKey'])
                tags = [CORRECT_TAG] if is_correct else []
                references.append(Reference(Output(text=label), tags=tags))

            instances.append(Instance(
                input=Input(text=prompt),
                references=references,
                split=TEST_SPLIT
            ))

        return instances
