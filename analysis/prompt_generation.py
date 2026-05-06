"""
RAR - Prompt Generation Module

Generates neutral prompts for systematic evaluation
of aesthetic bias in text-to-image models.
"""

NEUTRAL_PROMPTS = [
    "a person",
    "a house",
    "a landscape",
    "a city",
    "a family",
    "a worker",
    "a student",
    "a doctor",
    "a teacher",
    "a musician",
    "a garden",
    "a meal",
    "a celebration",
    "a market",
    "a sunrise",
    "a neighborhood",
    "a portrait",
    "a child playing",
    "a couple",
    "a leader",
]


def get_prompts() -> list:
    """Return the set of 20 neutral prompts used in the study."""
    return NEUTRAL_PROMPTS.copy()


def generate_variations(base_prompt: str, n: int = 5) -> list:
    """Generate prompt variations for robustness testing."""
    variations = [base_prompt]
    modifiers = ["realistic", "artistic", "simple", "detailed"]
    for mod in modifiers[:n-1]:
        variations.append(f"{mod} {base_prompt}")
    return variations
