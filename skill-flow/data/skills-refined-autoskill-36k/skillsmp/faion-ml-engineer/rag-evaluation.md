---
id: rag-evaluation
name: "RAG Evaluation"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# RAG Evaluation

## Overview

RAG evaluation measures the quality of retrieval and generation components separately and together. This methodology covers metrics, evaluation frameworks, and techniques for building reliable RAG systems.

## When to Use

- Validating RAG pipeline before production
- Comparing different retrieval strategies
- Tuning chunk sizes and overlap
- Selecting embedding models
- Measuring generation quality
- Continuous monitoring in production

## Key Concepts

### Evaluation Dimensions

| Dimension | Measures | Key Metrics |
|-----------|----------|-------------|
| Retrieval | Finding relevant docs | Precision, Recall, MRR, NDCG |
| Generation | Response quality | Faithfulness, Relevance, Coherence |
| End-to-End | Full pipeline | Answer accuracy, User satisfaction |

### RAG Triad (RAGAS Framework)

```
┌─────────────────────────────────────────┐
│           CONTEXT RELEVANCE             │
│   (Is retrieved context relevant?)       │
└────────────────────┬────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   FAITHFULNESS  │    │ ANSWER RELEVANCE│
│ (Is answer true │    │ (Does answer    │
│  to context?)   │    │  address query?)│
└─────────────────┘    └─────────────────┘
```

## Implementation

### Retrieval Metrics

```python
from typing import List, Set, Dict
import numpy as np

def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Precision@K: How many retrieved docs are relevant?

    Args:
        retrieved: List of retrieved document IDs (ordered by rank)
        relevant: Set of relevant document IDs
        k: Number of top results to consider
    """
    retrieved_at_k = set(retrieved[:k])
    relevant_retrieved = retrieved_at_k.intersection(relevant)
    return len(relevant_retrieved) / k

def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Recall@K: How many relevant docs were retrieved?
    """
    retrieved_at_k = set(retrieved[:k])
    relevant_retrieved = retrieved_at_k.intersection(relevant)
    return len(relevant_retrieved) / len(relevant) if relevant else 0

def mean_reciprocal_rank(retrieved: List[str], relevant: Set[str]) -> float:
    """
    MRR: How highly is the first relevant doc ranked?
    """
    for i, doc_id in enumerate(retrieved):
        if doc_id in relevant:
            return 1.0 / (i + 1)
    return 0.0

def ndcg_at_k(retrieved: List[str], relevance_scores: Dict[str, float], k: int) -> float:
    """
    NDCG@K: Normalized Discounted Cumulative Gain.
    Considers graded relevance (not just binary).
    """
    def dcg(scores: List[float]) -> float:
        return sum(
            (2**score - 1) / np.log2(i + 2)
            for i, score in enumerate(scores)
        )

    # Actual DCG
    actual_scores = [relevance_scores.get(doc_id, 0) for doc_id in retrieved[:k]]
    actual_dcg = dcg(actual_scores)

    # Ideal DCG (best possible ranking)
    ideal_scores = sorted(relevance_scores.values(), reverse=True)[:k]
    ideal_dcg = dcg(ideal_scores)

    return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0

def hit_rate(retrieved: List[str], relevant: Set[str]) -> float:
    """
    Hit Rate: Was at least one relevant doc retrieved?
    """
    return 1.0 if any(doc_id in relevant for doc_id in retrieved) else 0.0
```

### Generation Quality Metrics

```python
from openai import OpenAI

client = OpenAI()

def evaluate_faithfulness(
    answer: str,
    context: str,
    model: str = "gpt-4o"
) -> Dict[str, any]:
    """
    Faithfulness: Is the answer supported by the context?
    """
    prompt = f"""Evaluate if the answer is faithful to the given context.

Context:
{context}

Answer:
{answer}

Analyze the answer and determine:
1. What claims does the answer make?
2. Is each claim supported by the context?
3. Are there any hallucinations (claims not in context)?

Provide a score from 0 to 1 where:
- 1.0: Completely faithful, all claims supported
- 0.5: Partially faithful, some unsupported claims
- 0.0: Unfaithful, major hallucinations

Return JSON with: score, supported_claims, unsupported_claims, explanation"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    import json
    return json.loads(response.choices[0].message.content)

def evaluate_relevance(
    answer: str,
    question: str,
    model: str = "gpt-4o"
) -> Dict[str, any]:
    """
    Answer Relevance: Does the answer address the question?
    """
    prompt = f"""Evaluate if the answer addresses the question.

Question:
{question}

Answer:
{answer}

Analyze:
1. Does the answer directly address the question?
2. Is the answer complete or partial?
3. Is there irrelevant information?

Score from 0 to 1 where:
- 1.0: Completely answers the question
- 0.5: Partially answers or includes irrelevant info
- 0.0: Does not answer the question

Return JSON with: score, addresses_question, completeness, explanation"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    import json
    return json.loads(response.choices[0].message.content)

def evaluate_context_relevance(
    context: str,
    question: str,
    model: str = "gpt-4o"
) -> Dict[str, any]:
    """
    Context Relevance: Is the retrieved context relevant to the question?
    """
    prompt = f"""Evaluate if the context is relevant to answering the question.

Question:
{question}

Context:
{context}

Analyze:
1. Does the context contain information to answer the question?
2. How much of the context is relevant?
3. What relevant information is missing?

Score from 0 to 1 where:
- 1.0: Context fully relevant and sufficient
- 0.5: Partially relevant or incomplete
- 0.0: Irrelevant context

Return JSON with: score, relevant_sentences, irrelevant_sentences, missing_info"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    import json
    return json.loads(response.choices[0].message.content)
```

### RAGAS Integration

```python
# pip install ragas

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    context_entity_recall,
    answer_similarity,
    answer_correctness
)
from datasets import Dataset

def evaluate_with_ragas(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str]
) -> Dict[str, float]:
    """
    Comprehensive RAG evaluation using RAGAS framework.
    """
    # Prepare dataset
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    dataset = Dataset.from_dict(data)

    # Run evaluation
    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
            answer_correctness
        ]
    )

    return result

# Example usage
questions = ["What is machine learning?"]
answers = ["Machine learning is a subset of AI that enables systems to learn from data."]
contexts = [["Machine learning is a branch of artificial intelligence focused on building systems that learn from data."]]
ground_truths = ["Machine learning is a type of AI where computers learn from data without being explicitly programmed."]

scores = evaluate_with_ragas(questions, answers, contexts, ground_truths)
print(scores)
```

### Test Set Generation

```python
from typing import List, Tuple
import random

def generate_test_questions(
    documents: List[str],
    num_questions: int = 10,
    model: str = "gpt-4o"
) -> List[Dict[str, str]]:
    """
    Generate test questions from documents.
    """
    test_set = []

    for doc in random.sample(documents, min(num_questions, len(documents))):
        prompt = f"""Based on this document, generate a question and its answer.

Document:
{doc[:2000]}

Generate a factual question that can be answered from this document.
Return JSON with: question, answer, source_quote"""

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        import json
        qa = json.loads(response.choices[0].message.content)
        qa["document"] = doc
        test_set.append(qa)

    return test_set

def generate_diverse_questions(
    documents: List[str],
    question_types: List[str] = ["factual", "comparative", "reasoning", "summarization"]
) -> List[Dict[str, str]]:
    """
    Generate diverse question types for comprehensive testing.
    """
    test_set = []

    for q_type in question_types:
        prompt = f"""Generate a {q_type} question based on the documents.

Documents:
{chr(10).join(documents[:3])}

Question type: {q_type}
- factual: Simple fact lookup
- comparative: Compare two things
- reasoning: Requires inference
- summarization: Summarize information

Return JSON with: question, expected_answer, type, difficulty"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        import json
        test_set.append(json.loads(response.choices[0].message.content))

    return test_set
```

### Evaluation Pipeline

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

@dataclass
class EvaluationResult:
    question: str
    answer: str
    context: List[str]
    ground_truth: Optional[str]
    retrieval_metrics: Dict[str, float]
    generation_metrics: Dict[str, float]
    timestamp: str

class RAGEvaluator:
    """Complete RAG evaluation pipeline."""

    def __init__(self, rag_pipeline, model: str = "gpt-4o"):
        self.rag = rag_pipeline
        self.model = model
        self.results: List[EvaluationResult] = []

    def evaluate_single(
        self,
        question: str,
        ground_truth: Optional[str] = None,
        relevant_doc_ids: Optional[Set[str]] = None
    ) -> EvaluationResult:
        """Evaluate single question."""
        # Get RAG response
        response = self.rag.query(question)

        # Extract components
        answer = response["answer"]
        contexts = [s["content"] for s in response["sources"]]
        retrieved_ids = [s["metadata"].get("id") for s in response["sources"]]

        # Retrieval metrics
        retrieval_metrics = {}
        if relevant_doc_ids:
            retrieval_metrics["precision@5"] = precision_at_k(retrieved_ids, relevant_doc_ids, 5)
            retrieval_metrics["recall@5"] = recall_at_k(retrieved_ids, relevant_doc_ids, 5)
            retrieval_metrics["mrr"] = mean_reciprocal_rank(retrieved_ids, relevant_doc_ids)
            retrieval_metrics["hit_rate"] = hit_rate(retrieved_ids, relevant_doc_ids)

        # Generation metrics
        context_combined = "\n\n".join(contexts)

        faithfulness_result = evaluate_faithfulness(answer, context_combined, self.model)
        relevance_result = evaluate_relevance(answer, question, self.model)
        context_result = evaluate_context_relevance(context_combined, question, self.model)

        generation_metrics = {
            "faithfulness": faithfulness_result.get("score", 0),
            "answer_relevance": relevance_result.get("score", 0),
            "context_relevance": context_result.get("score", 0)
        }

        result = EvaluationResult(
            question=question,
            answer=answer,
            context=contexts,
            ground_truth=ground_truth,
            retrieval_metrics=retrieval_metrics,
            generation_metrics=generation_metrics,
            timestamp=datetime.now().isoformat()
        )

        self.results.append(result)
        return result

    def evaluate_batch(
        self,
        test_set: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Evaluate batch of questions and compute aggregate metrics."""
        for item in test_set:
            self.evaluate_single(
                question=item["question"],
                ground_truth=item.get("answer"),
                relevant_doc_ids=item.get("relevant_docs")
            )

        return self.aggregate_metrics()

    def aggregate_metrics(self) -> Dict[str, float]:
        """Compute aggregate metrics across all evaluations."""
        if not self.results:
            return {}

        metrics = {
            "avg_faithfulness": 0,
            "avg_answer_relevance": 0,
            "avg_context_relevance": 0,
            "avg_precision@5": 0,
            "avg_recall@5": 0,
            "avg_mrr": 0,
            "total_evaluated": len(self.results)
        }

        for result in self.results:
            metrics["avg_faithfulness"] += result.generation_metrics.get("faithfulness", 0)
            metrics["avg_answer_relevance"] += result.generation_metrics.get("answer_relevance", 0)
            metrics["avg_context_relevance"] += result.generation_metrics.get("context_relevance", 0)
            metrics["avg_precision@5"] += result.retrieval_metrics.get("precision@5", 0)
            metrics["avg_recall@5"] += result.retrieval_metrics.get("recall@5", 0)
            metrics["avg_mrr"] += result.retrieval_metrics.get("mrr", 0)

        n = len(self.results)
        for key in metrics:
            if key.startswith("avg_"):
                metrics[key] /= n

        return metrics

    def export_results(self, filepath: str):
        """Export results to JSON."""
        data = [
            {
                "question": r.question,
                "answer": r.answer,
                "ground_truth": r.ground_truth,
                "retrieval_metrics": r.retrieval_metrics,
                "generation_metrics": r.generation_metrics,
                "timestamp": r.timestamp
            }
            for r in self.results
        ]

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
```

### A/B Testing Framework

```python
class RAGABTest:
    """A/B testing for RAG configurations."""

    def __init__(self, config_a: dict, config_b: dict):
        self.config_a = config_a
        self.config_b = config_b
        self.results_a = []
        self.results_b = []

    def run_test(
        self,
        test_questions: List[str],
        rag_a,  # RAG pipeline with config A
        rag_b   # RAG pipeline with config B
    ):
        """Run A/B test on both configurations."""
        for question in test_questions:
            # Test config A
            response_a = rag_a.query(question)
            eval_a = self._evaluate(question, response_a)
            self.results_a.append(eval_a)

            # Test config B
            response_b = rag_b.query(question)
            eval_b = self._evaluate(question, response_b)
            self.results_b.append(eval_b)

    def _evaluate(self, question: str, response: dict) -> dict:
        """Quick evaluation of single response."""
        return {
            "question": question,
            "answer": response["answer"],
            "latency": response.get("latency", 0),
            "num_sources": len(response.get("sources", []))
        }

    def compare_results(self) -> dict:
        """Compare results between configurations."""
        def avg_metric(results: List[dict], key: str) -> float:
            values = [r.get(key, 0) for r in results]
            return sum(values) / len(values) if values else 0

        return {
            "config_a": {
                "name": self.config_a.get("name", "Config A"),
                "avg_latency": avg_metric(self.results_a, "latency"),
                "total_questions": len(self.results_a)
            },
            "config_b": {
                "name": self.config_b.get("name", "Config B"),
                "avg_latency": avg_metric(self.results_b, "latency"),
                "total_questions": len(self.results_b)
            }
        }
```

## Best Practices

1. **Ground Truth Creation**
   - Manually verify ground truth answers
   - Include diverse question types
   - Cover edge cases

2. **Metric Selection**
   - Use retrieval metrics when you have relevance labels
   - Use LLM-based metrics for generation quality
   - Combine multiple metrics for holistic view

3. **Evaluation Frequency**
   - Run full evaluation before major changes
   - Use lightweight metrics for continuous monitoring
   - Track trends over time

4. **Human Evaluation**
   - Sample and manually review outputs
   - Create annotation guidelines
   - Calculate inter-annotator agreement

5. **Cost Management**
   - Use cheaper models for high-volume evaluation
   - Cache evaluation results
   - Batch similar evaluations

## Common Pitfalls

1. **No Ground Truth** - Evaluating without knowing correct answers
2. **Single Metric** - Over-relying on one metric
3. **Non-representative Test Set** - Test questions don't match production
4. **Evaluator Bias** - LLM evaluator may have biases
5. **Ignoring Latency** - Only measuring quality, not speed
6. **Static Evaluation** - Not re-evaluating after changes

## References

- [RAGAS Paper](https://arxiv.org/abs/2309.15217)
- [RAGAS Documentation](https://docs.ragas.io/)
- [Evaluating RAG (LlamaIndex)](https://docs.llamaindex.ai/en/stable/module_guides/evaluating/)
- [RAG Evaluation Best Practices](https://www.pinecone.io/learn/rag-evaluation/)
