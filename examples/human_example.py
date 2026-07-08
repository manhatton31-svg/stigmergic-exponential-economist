"""
Human interaction example — tests the reasoning pipeline in human mode.

Run without starting the full agent:
    python examples/human_example.py

This simulates what happens when a human sends a chat message.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.requests import EconomistRequest, OperationMode
from utils.reasoning import ReasoningEngine


def main() -> None:
    query = (
        "How should we design a multi-agent marketplace for zero-marginal-cost "
        "digital goods that uses stigmergic coordination instead of centralized "
        "matching?"
    )

    print("=" * 60)
    print("HUMAN MODE EXAMPLE")
    print("=" * 60)
    print(f"\nQuery: {query}\n")

    engine = ReasoningEngine()
    request = EconomistRequest(
        query=query,
        mode=OperationMode.HUMAN.value,
        domain="agentic marketplaces",
        desired_outcomes=[
            "exponential returns",
            "stigmergic coordination",
            "zero-marginal-cost dynamics",
        ],
        baseline_trajectory="Centralized marketplace with human moderators",
    )

    response = engine.analyze(request)

    print(response.human_summary)
    print("\n" + "=" * 60)
    print(f"Confidence: {response.confidence:.0%}")
    print(f"Request ID: {response.request_id}")
    print("=" * 60)

    # Also show structured output snippet
    print("\n--- Structured Output (Agentic Mode Preview) ---")
    print(json.dumps(response.creation_sequence.model_dump(), indent=2)[:1500] + "...")


if __name__ == "__main__":
    main()