"""
Response models — creation-sequence-ready, machine-parseable outputs.
"""

from typing import Any, Dict, List, Optional

from uagents import Model


class DataCitation(Model):
    """Grounding citation with metric and source."""

    source: str
    metric: str
    value: str
    relevance: str
    retrieved_at: Optional[str] = None


class PipelineStage(Model):
    """Single stage of the mandatory reasoning pipeline."""

    stage_name: str
    stage_number: int
    analysis: str
    key_insights: List[str] = []
    citations: List[DataCitation] = []


class ReasoningPipeline(Model):
    """Complete 5-stage mandatory reasoning pipeline output."""

    first_principles: PipelineStage
    stigmergic_autocatalysis: PipelineStage
    data_grounding: PipelineStage
    convergence_synthesis: PipelineStage
    delta_value: PipelineStage


class DeltaValueAnalysis(Model):
    """Explicit comparison: baseline trajectory vs skills-activated trajectory."""

    baseline_trajectory: str
    activated_trajectory: str
    delta_value: str
    delta_cost: str
    net_value_assessment: str
    exceeds_cost: bool
    quantified_benefits: List[str] = []
    quantified_costs: List[str] = []


class CreationSequence(Model):
    """
    Creation-sequence-ready artifact — directly usable in active building.

    Includes architectures, prompts, message models, build sequences,
    integration points, and prioritized actions.
    """

    summary: str
    architecture: Dict[str, Any] = {}
    prompts: List[Dict[str, str]] = []
    message_models: List[Dict[str, Any]] = []
    build_sequence: List[Dict[str, Any]] = []
    integration_points: List[Dict[str, str]] = []
    prioritized_actions: List[Dict[str, Any]] = []


class EconomistResponse(Model):
    """Primary structured response for agentic mode."""

    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    mode: str = "agentic"
    pipeline: ReasoningPipeline
    delta_analysis: DeltaValueAnalysis
    creation_sequence: CreationSequence
    human_summary: Optional[str] = None
    confidence: float = 0.0
    version: str = "1.0.0"


class FunnelStageResponse(Model):
    """Response for funnel / pipeline stage participation."""

    pipeline_id: Optional[str] = None
    stage_name: str
    stage_index: int
    stage_complete: bool = True
    economist_response: EconomistResponse
    handoff_notes: str = ""
    next_stage_recommendations: List[str] = []


class VerificationVerdict(Model):
    """Single criterion evaluation in verification."""

    criterion: str
    passed: bool
    evidence: str
    score: float = 0.0


class VerificationResponse(Model):
    """Final verification layer output."""

    verification_id: Optional[str] = None
    correlation_id: Optional[str] = None
    approved: bool
    overall_score: float
    verdicts: List[VerificationVerdict] = []
    agentic_future_alignment: str
    recommendations: List[str] = []
    blocking_issues: List[str] = []
    human_summary: Optional[str] = None


class FeedbackResponse(Model):
    """Learning loop acknowledgment and improvement signal."""

    feedback_id: str
    accepted: bool
    message: str
    improvement_opportunities: List[str] = []
    prompt_evolution_proposed: bool = False
    prompt_evolution_summary: Optional[str] = None