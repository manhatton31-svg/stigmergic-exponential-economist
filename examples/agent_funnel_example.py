"""
Agent-to-agent funnel workflow example.

Demonstrates multi-stage pipeline where the Economist participates as one stage
among many agents, consuming prior stage outputs and producing handoff artifacts.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.requests import EconomistRequest, FunnelStageRequest, OperationMode
from utils.reasoning import ReasoningEngine


def simulate_funnel_pipeline() -> None:
    """Simulate a 3-stage funnel with Economist as stage 2."""
    print("=" * 60)
    print("FUNNEL WORKFLOW EXAMPLE")
    print("=" * 60)

    pipeline_id = "funnel-demo-001"

    # Stage 1 output (simulated upstream agent — e.g., research agent)
    stage1_output = {
        "stage_name": "research",
        "findings": [
            "Agent-to-agent commerce growing 300% YoY",
            "100K+ agents on Agentverse",
            "Inference costs declined 10x since 2023",
        ],
        "recommendation": "Build agent-native marketplace",
    }

    print(f"\nPipeline ID: {pipeline_id}")
    print(f"Stage 1 (Research Agent) output:")
    print(json.dumps(stage1_output, indent=2))

    # Stage 2: Economist analyzes with prior context
    funnel_request = FunnelStageRequest(
        stage_name="strategic_analysis",
        stage_index=1,
        total_stages=3,
        query="Design an agent-native marketplace architecture",
        prior_stages=[stage1_output],
        mode=OperationMode.AGENTIC.value,
        pipeline_id=pipeline_id,
        correlation_id="corr-funnel-001",
    )

    print(f"\n--- Stage 2: Stigmergic Exponential Economist ---")

    engine = ReasoningEngine()
    economist_request = EconomistRequest(
        query=funnel_request.query,
        mode=funnel_request.mode,
        upstream_context={
            "pipeline_id": funnel_request.pipeline_id,
            "stage_name": funnel_request.stage_name,
            "prior_stages": funnel_request.prior_stages,
        },
        correlation_id=funnel_request.correlation_id,
    )

    economist_response = engine.analyze(economist_request)

    print(f"Confidence: {economist_response.confidence:.0%}")
    print(f"Creation Sequence Summary: {economist_response.creation_sequence.summary}")
    print(f"\nPrioritized Actions:")
    for action in economist_response.creation_sequence.prioritized_actions:
        print(f"  P{action.get('priority')}: {action.get('action')}")

    # Stage 3 would receive economist_response.creation_sequence
    stage2_handoff = {
        "stage_name": "strategic_analysis",
        "economist_response": economist_response.model_dump(),
        "handoff_notes": "Pass creation_sequence to deployment stage",
    }

    print(f"\n--- Handoff to Stage 3 (Deployment Agent) ---")
    print(f"Build sequence steps: {len(economist_response.creation_sequence.build_sequence)}")
    print(f"Integration points: {len(economist_response.creation_sequence.integration_points)}")
    print("\nFunnel stage complete. Ready for downstream agent consumption.")


if __name__ == "__main__":
    simulate_funnel_pipeline()