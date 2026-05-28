# Multi-Armed Bandit & Exploration

This guide covers exploration strategies for recommendation systems using multi-armed bandits.

## Thompson Sampling

```python
# src/recommendation/bandit.py
from typing import Dict, Tuple, List
import numpy as np
from dataclasses import dataclass

@dataclass
class BanditArm:
    """Represents a recommendation strategy."""
    name: str
    successes: int = 0
    failures: int = 0

    @property
    def total_pulls(self) -> int:
        return self.successes + self.failures

    @property
    def success_rate(self) -> float:
        if self.total_pulls == 0:
            return 0.0
        return self.successes / self.total_pulls

class ThompsonSamplingBandit:
    """Thompson Sampling for recommendation strategy selection."""

    def __init__(self, strategies: List[str]):
        self.arms = {name: BanditArm(name) for name in strategies}

    def select_strategy(self) -> str:
        """Select strategy using Thompson Sampling."""
        samples = {}
        for name, arm in self.arms.items():
            # Beta distribution sampling
            alpha = arm.successes + 1
            beta = arm.failures + 1
            samples[name] = np.random.beta(alpha, beta)

        # Select arm with highest sample
        return max(samples.items(), key=lambda x: x[1])[0]

    def update(self, strategy: str, success: bool):
        """Update arm statistics."""
        if success:
            self.arms[strategy].successes += 1
        else:
            self.arms[strategy].failures += 1

    def get_statistics(self) -> Dict[str, Dict]:
        """Get current bandit statistics."""
        return {
            name: {
                'pulls': arm.total_pulls,
                'success_rate': arm.success_rate,
                'confidence': self._calculate_confidence(arm)
            }
            for name, arm in self.arms.items()
        }

    def _calculate_confidence(self, arm: BanditArm) -> Tuple[float, float]:
        """Calculate 95% confidence interval using Wilson score."""
        if arm.total_pulls == 0:
            return (0.0, 1.0)

        p = arm.success_rate
        n = arm.total_pulls
        z = 1.96  # 95% confidence

        denominator = 1 + z**2/n
        centre_adjusted = p + z**2 / (2*n)
        adjusted_std = np.sqrt((p*(1 - p) + z**2/(4*n)) / n)

        lower = (centre_adjusted - z*adjusted_std) / denominator
        upper = (centre_adjusted + z*adjusted_std) / denominator

        return (max(0, lower), min(1, upper))
```

## Epsilon-Greedy Strategy

```python
# src/recommendation/epsilon_greedy.py
import random
from typing import List, Dict

class EpsilonGreedy:
    """Epsilon-Greedy exploration strategy."""

    def __init__(self, epsilon: float = 0.1):
        """
        Args:
            epsilon: Probability of exploration (vs exploitation)
        """
        self.epsilon = epsilon
        self.strategy_rewards = {}
        self.strategy_counts = {}

    def select_strategy(self, strategies: List[str]) -> str:
        """Select strategy using epsilon-greedy."""

        if random.random() < self.epsilon:
            # Explore: random strategy
            return random.choice(strategies)
        else:
            # Exploit: best known strategy
            if not self.strategy_rewards:
                return random.choice(strategies)

            avg_rewards = {
                strategy: self.strategy_rewards[strategy] / self.strategy_counts[strategy]
                for strategy in self.strategy_rewards.keys()
            }
            return max(avg_rewards, key=avg_rewards.get)

    def update(self, strategy: str, reward: float):
        """Update strategy statistics."""
        self.strategy_rewards[strategy] = \
            self.strategy_rewards.get(strategy, 0.0) + reward
        self.strategy_counts[strategy] = \
            self.strategy_counts.get(strategy, 0) + 1

    def decay_epsilon(self, decay_rate: float = 0.99):
        """Decay epsilon over time (explore less as we learn more)."""
        self.epsilon *= decay_rate
```

## UCB (Upper Confidence Bound)

```python
# src/recommendation/ucb.py
import math
from typing import List, Dict

class UCB:
    """Upper Confidence Bound algorithm."""

    def __init__(self, c: float = 2.0):
        """
        Args:
            c: Exploration parameter (higher = more exploration)
        """
        self.c = c
        self.strategy_rewards = {}
        self.strategy_counts = {}
        self.total_pulls = 0

    def select_strategy(self, strategies: List[str]) -> str:
        """Select strategy using UCB."""

        # Ensure all strategies are tried at least once
        for strategy in strategies:
            if strategy not in self.strategy_counts:
                return strategy

        # Calculate UCB scores
        ucb_scores = {}
        for strategy in strategies:
            avg_reward = self.strategy_rewards[strategy] / self.strategy_counts[strategy]
            exploration_bonus = self.c * math.sqrt(
                math.log(self.total_pulls) / self.strategy_counts[strategy]
            )
            ucb_scores[strategy] = avg_reward + exploration_bonus

        return max(ucb_scores, key=ucb_scores.get)

    def update(self, strategy: str, reward: float):
        """Update strategy statistics."""
        self.strategy_rewards[strategy] = \
            self.strategy_rewards.get(strategy, 0.0) + reward
        self.strategy_counts[strategy] = \
            self.strategy_counts.get(strategy, 0) + 1
        self.total_pulls += 1
```

## Contextual Bandits

```python
# src/recommendation/contextual_bandit.py
import numpy as np
from sklearn.linear_model import LogisticRegression
from typing import Dict, List

class ContextualBandit:
    """Contextual bandit using logistic regression."""

    def __init__(self, strategies: List[str]):
        self.strategies = strategies
        self.models = {
            strategy: LogisticRegression()
            for strategy in strategies
        }
        self.training_data = {
            strategy: {'X': [], 'y': []}
            for strategy in strategies
        }

    def select_strategy(self, context: Dict[str, float]) -> str:
        """Select strategy based on context features."""

        context_vector = self._context_to_vector(context)

        # Predict reward probability for each strategy
        predictions = {}
        for strategy, model in self.models.items():
            if len(self.training_data[strategy]['X']) < 10:
                # Not enough data, random exploration
                predictions[strategy] = np.random.random()
            else:
                # Predict reward probability
                X = np.array([context_vector])
                predictions[strategy] = model.predict_proba(X)[0][1]

        # Select best strategy
        return max(predictions, key=predictions.get)

    def update(self, strategy: str, context: Dict[str, float], reward: float):
        """Update model with new observation."""

        context_vector = self._context_to_vector(context)
        self.training_data[strategy]['X'].append(context_vector)
        self.training_data[strategy]['y'].append(1 if reward > 0 else 0)

        # Retrain model if enough data
        if len(self.training_data[strategy]['X']) >= 10:
            X = np.array(self.training_data[strategy]['X'])
            y = np.array(self.training_data[strategy]['y'])
            self.models[strategy].fit(X, y)

    def _context_to_vector(self, context: Dict[str, float]) -> List[float]:
        """Convert context dict to feature vector."""
        # Ensure consistent ordering
        return [context.get(key, 0.0) for key in sorted(context.keys())]
```

## Exploration vs Exploitation Trade-off

```python
# src/recommendation/exploration.py
from typing import List, Dict
import random

def calculate_exploration_rate(
    total_users: int,
    exploration_budget: float = 0.1
) -> float:
    """
    Calculate appropriate exploration rate based on traffic.

    Args:
        total_users: Total number of users
        exploration_budget: Percentage of traffic for exploration

    Returns:
        Exploration probability
    """
    return exploration_budget

def hybrid_explore_exploit(
    user_id: str,
    recommendations: List[Dict],
    exploration_rate: float = 0.1,
    diversification_factor: float = 0.3
) -> List[Dict]:
    """
    Combine exploration and exploitation in recommendations.

    Args:
        user_id: User identifier
        recommendations: Ranked recommendations
        exploration_rate: Probability of exploring
        diversification_factor: How much to diversify exploited items

    Returns:
        Final recommendation list
    """
    n_items = len(recommendations)
    n_explore = int(n_items * exploration_rate)
    n_exploit = n_items - n_explore

    # Exploit: Top recommendations with some diversification
    exploit_items = recommendations[:int(n_exploit / diversification_factor)]
    exploit_sample = random.sample(exploit_items, n_exploit)

    # Explore: Random items from lower ranks
    explore_pool = recommendations[n_exploit:]
    explore_sample = random.sample(explore_pool, min(n_explore, len(explore_pool)))

    # Combine and shuffle
    final_recs = exploit_sample + explore_sample
    random.shuffle(final_recs)

    return final_recs[:n_items]
```

## A/B Testing with Bandits

```python
# src/recommendation/ab_testing_bandit.py
from typing import Dict
import hashlib

class ABTestBandit:
    """Combine A/B testing with bandit algorithms."""

    def __init__(self, variants: Dict[str, float]):
        """
        Args:
            variants: Dict of variant_name -> initial_allocation (0-1)
        """
        self.variants = variants
        self.variant_results = {v: {'successes': 0, 'trials': 0} for v in variants}

    def assign_variant(self, user_id: str) -> str:
        """Assign user to variant using Thompson Sampling."""

        # Sample from Beta distribution for each variant
        samples = {}
        for variant in self.variants:
            alpha = self.variant_results[variant]['successes'] + 1
            beta = self.variant_results[variant]['trials'] - \
                   self.variant_results[variant]['successes'] + 1
            samples[variant] = np.random.beta(alpha, beta)

        return max(samples, key=samples.get)

    def record_outcome(self, variant: str, success: bool):
        """Record experiment outcome."""
        self.variant_results[variant]['trials'] += 1
        if success:
            self.variant_results[variant]['successes'] += 1

    def get_winning_variant(self, confidence_threshold: float = 0.95) -> str:
        """Get winning variant if confidence threshold met."""

        best_variant = max(
            self.variant_results.keys(),
            key=lambda v: self.variant_results[v]['successes'] /
                         max(self.variant_results[v]['trials'], 1)
        )

        # Check if we have enough confidence
        # Simple implementation - production should use proper statistical tests
        return best_variant
```

## Best Practices

- Use Thompson Sampling for most cases (good exploration/exploitation balance)
- Start with ε=0.1 for epsilon-greedy, decay over time
- UCB works well when you have many strategies to choose from
- Use contextual bandits when user features are available
- Reserve 10-20% of traffic for exploration
- A/B test bandit performance against static algorithms
- Monitor regret (difference from optimal strategy)
- Use separate bandits for different user segments
- Track both immediate rewards (clicks) and delayed rewards (purchases)
- Regularly audit exploration strategies for effectiveness
