"""
Verification layer example — final check before deployment.

Demonstrates evaluating an artifact against agentic-future criteria.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.requests import EconomistRequest, OperationMode, VerificationRequest
from utils.reasoning import ReasoningEngine
from utils.verification import VerificationEngine


def main() -> None:
    print("=" * 60)
    print("VERIFICATION LAYER EXAMPLE")
    print("=" * 60)

    # Step 1: Generate an artifact via reasoning pipeline
    engine = ReasoningEngine()
    request = EconomistRequest(
        query="Build a stigmergic agent coordination hub",
        mode=OperationMode.AGENTIC.value,
        domain="multi-agent systems",
    )
    artifact = engine.analyze(request)

    print(f"\nArtifact generated (request_id: {artifact.request_id})")
    print(f"Confidence: {artifact.confidence:.0%}")

    # Step 2: Verify the artifact
    verifier = VerificationEngine()
    verification_request = VerificationRequest(
        artifact=artifact.model_dump(),
        artifact_type="EconomistResponse",
        original_intent="Build a stigmergic agent coordination hub",
        mode=OperationMode.HUMAN.value,
        verification_id="verify-demo-001",
    )

    result = verifier.verify(verification_request)

    print(f"\n--- Verification Result ---")
    print(f"Approved: {result.approved}")
    print(f"Overall Score: {result.overall_score:.0%}")
    print(f"Alignment: {result.agentic_future_alignment}")

    print(f"\n--- Criterion Verdicts ---")
    for v in result.verdicts:
        status = "PASS" if v.passed else "FAIL"
        print(f"  [{status}] {v.criterion} (score: {v.score:.0%})")

    if result.blocking_issues:
        print(f"\n--- Blocking Issues ---")
        for issue in result.blocking_issues:
            print(f"  - {issue}")

    print(f"\n--- Recommendations ---")
    for rec in result.recommendations:
        print(f"  - {rec}")

    if result.human_summary:
        print(f"\n{result.human_summary}")


if __name__ == "__main__":
    main()