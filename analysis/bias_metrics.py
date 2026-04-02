"""
RAR - Bias Metrics Module

Quantitative metrics for measuring aesthetic convergence
and representational bias in generative AI outputs.
"""

import numpy as np
from collections import Counter


def aesthetic_convergence_score(features: list) -> float:
    """
    Measure how much outputs converge toward dominant patterns.
    Higher score = more convergence (less diversity).
    """
    if not features:
        return 0.0
    counts = Counter(features)
    total = len(features)
    proportions = [c / total for c in counts.values()]
    max_proportion = max(proportions)
    return max_proportion


def diversity_index(categories: list) -> float:
    """
    Shannon diversity index for output categories.
    Higher value = more diverse outputs.
    """
    counts = Counter(categories)
    total = sum(counts.values())
    proportions = [c / total for c in counts.values()]
    return -sum(p * np.log(p) for p in proportions if p > 0)


def reinforcement_loop_strength(
    initial_distribution: dict,
    final_distribution: dict
) -> float:
    """
    Measure the strength of aesthetic reinforcement loops
    by comparing initial vs final output distributions.
    """
    all_keys = set(initial_distribution) | set(final_distribution)
    divergence = 0
    for key in all_keys:
        p = initial_distribution.get(key, 0.001)
        q = final_distribution.get(key, 0.001)
        divergence += p * np.log(p / q)
    return divergence
