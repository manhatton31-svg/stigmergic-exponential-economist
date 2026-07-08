"""
Feedback flow example — learning loop demonstration.

Simulates feedback collection, storage, analysis, and prompt evolution proposals.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.requests import FeedbackRequest
from utils.learning import LearningLoop


class MockStorage:
    """In-memory storage simulating uAgent ctx.storage."""

    def __init__(self):
        self._data = {}

    def has(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str) -> str:
        return self._data[key]

    def set(self, key: str, value: str) -> None:
        self._data[key] = value


def main() -> None:
    print("=" * 60)
    print("FEEDBACK / LEARNING LOOP EXAMPLE")
    print("=" * 60)

    storage = MockStorage()
    loop = LearningLoop(storage=storage)

    # Simulate feedback from a human
    feedback1 = FeedbackRequest(
        target_request_id="req-001",
        rating=4,
        feedback_type="reasoning",
        comments="Strong first principles analysis, could use more citations",
        suggested_improvements=["Add live data API integration"],
        source="human",
    )

    result1 = loop.record_feedback(feedback1)
    print(f"\nFeedback 1 recorded: {result1.feedback_id}")
    print(f"Message: {result1.message}")
    print(f"Opportunities: {result1.improvement_opportunities}")

    # Simulate low rating from an agent
    feedback2 = FeedbackRequest(
        target_request_id="req-002",
        rating=2,
        feedback_type="data",
        comments="Data grounding citations felt stale",
        suggested_improvements=[
            "Refresh Gartner/McKinsey metrics quarterly",
            "Add Agentverse live agent count API",
        ],
        source="agent",
    )

    result2 = loop.record_feedback(feedback2)
    print(f"\nFeedback 2 recorded: {result2.feedback_id}")
    print(f"Prompt evolution proposed: {result2.prompt_evolution_proposed}")
    if result2.prompt_evolution_summary:
        print(f"Evolution: {result2.prompt_evolution_summary}")

    # Show accumulated stats
    stats = loop.get_stats()
    print(f"\n--- Feedback Statistics ---")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()