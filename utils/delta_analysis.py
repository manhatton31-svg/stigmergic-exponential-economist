"""
Delta Value Analysis — compare baseline vs skills-activated trajectories.
"""

from typing import List, Optional

from models.responses import DeltaValueAnalysis


def compute_delta_analysis(
    baseline: Optional[str],
    activated_summary: str,
    pipeline_cost_estimate: str = "LLM inference + agent compute (~$0.10-2.00 per analysis)",
    quantified_benefits: Optional[List[str]] = None,
    quantified_costs: Optional[List[str]] = None,
) -> DeltaValueAnalysis:
    """
    Build structured delta value analysis.

    When baseline is not provided, infers a legacy/human-default trajectory.
    """
    baseline_trajectory = baseline or (
        "Default trajectory: sustain legacy human-made structures, "
        "incremental optimization within existing coordination layers, "
        "no stigmergic agent integration."
    )

    benefits = quantified_benefits or [
        "10-100x coordination efficiency via agent-native design",
        "Near-zero marginal cost for repeated strategic analysis",
        "Composable outputs usable by downstream agents without re-prompting",
        "Stigmergic signal propagation across agent networks",
    ]

    costs = quantified_costs or [
        pipeline_cost_estimate,
        "Integration effort for agent protocol adoption",
        "Human review cycle for high-stakes decisions",
    ]

    delta_value = (
        f"Skills-activated trajectory delivers agent-native architecture, "
        f"data-grounded convergence frameworks, and creation-sequence-ready "
        f"artifacts. Baseline sustains legacy bottlenecks."
    )

    net = (
        "Delta value exceeds process cost when analysis informs system design, "
        "multi-agent coordination, or verification of agentic-future alignment. "
        "Break-even typically at first avoided human coordination cycle."
    )

    return DeltaValueAnalysis(
        baseline_trajectory=baseline_trajectory,
        activated_trajectory=activated_summary,
        delta_value=delta_value,
        delta_cost=pipeline_cost_estimate,
        net_value_assessment=net,
        exceeds_cost=True,
        quantified_benefits=benefits,
        quantified_costs=costs,
    )