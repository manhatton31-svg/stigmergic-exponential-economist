"""
Request models for human and agent-to-agent communication.

Designed for interoperability with arbitrary agents via flexible context fields.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from uagents import Model


class OperationMode(str, Enum):
    """Dual-mode operation: human-readable vs machine-structured."""

    HUMAN = "human"
    AGENTIC = "agentic"


class EconomistRequest(Model):
    """
    Primary analysis request — works with any upstream agent or human proxy.

    Supports ForgeResonance, Arcly, and convergent-swarm patterns via
    integration_hooks and upstream_context.
    """

    query: str
    mode: str = OperationMode.AGENTIC.value
    domain: Optional[str] = None
    constraints: List[str] = []
    desired_outcomes: List[str] = []
    baseline_trajectory: Optional[str] = None
    upstream_context: Dict[str, Any] = {}
    integration_hooks: Dict[str, str] = {}
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None


class FunnelStageRequest(Model):
    """
    Funnel / pipeline stage input — one agent among many in a workflow.

    stage_name identifies the funnel position (e.g. 'strategic_analysis').
    prior_stages carries outputs from upstream agents in the pipeline.
    """

    stage_name: str
    stage_index: int = 0
    total_stages: int = 1
    query: str
    prior_stages: List[Dict[str, Any]] = []
    mode: str = OperationMode.AGENTIC.value
    pipeline_id: Optional[str] = None
    correlation_id: Optional[str] = None


class VerificationRequest(Model):
    """
    Final verification layer — evaluate whether outputs advance the agentic future.

    artifact is the output to verify (from any upstream agent).
    criteria optionally override default agentic-future verification rubric.
    """

    artifact: Dict[str, Any]
    artifact_type: str = "generic"
    original_intent: str
    criteria: List[str] = []
    mode: str = OperationMode.AGENTIC.value
    verification_id: Optional[str] = None
    correlation_id: Optional[str] = None


class FeedbackRequest(Model):
    """
    Learning loop input — structured feedback from humans or other agents.

    Used to improve reasoning quality, data grounding, and output usefulness.
    """

    target_request_id: str
    rating: int  # 1-5
    feedback_type: str = "general"  # general | reasoning | data | output | verification
    comments: str = ""
    suggested_improvements: List[str] = []
    source: str = "agent"  # human | agent
    correlation_id: Optional[str] = None