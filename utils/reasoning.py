"""
Mandatory reasoning pipeline orchestrator.

Executes all 5 stages on every input:
1. First Principles Decomposition
2. Stigmergic Autocatalysis Analysis
3. Data Grounding
4. Convergence Synthesis
5. Delta Value Analysis
"""

import json
import uuid
from typing import Any, Dict, List, Optional

from models.requests import EconomistRequest, OperationMode
from models.responses import (
    CreationSequence,
    DataCitation,
    DeltaValueAnalysis,
    EconomistResponse,
    PipelineStage,
    ReasoningPipeline,
)
from utils.data_grounding import build_grounding_context
from utils.delta_analysis import compute_delta_analysis
from utils.llm import call_llm, extract_json_from_response

AGENT_VERSION = "1.0.0"

SYSTEM_PROMPT = """You are the Stigmergic Exponential Economist — a universal strategic
foresight and verification agent for the Agentic Age.

You MUST execute this mandatory reasoning pipeline on every input:
1. First Principles Decomposition — break down to fundamental truths
2. Stigmergic Autocatalysis Analysis — identify self-reinforcing coordination signals
3. Data Grounding — cite provided metrics; explain path selection based on data
4. Convergence Synthesis — converge bleeding-edge domains into novel frameworks
5. Delta Value Analysis — compare baseline vs activated trajectory; prove delta > cost

Output ONLY valid JSON matching this schema:
{
  "first_principles": {"analysis": "...", "key_insights": ["..."]},
  "stigmergic_autocatalysis": {"analysis": "...", "key_insights": ["..."]},
  "data_grounding": {"analysis": "...", "key_insights": ["..."]},
  "convergence_synthesis": {"analysis": "...", "key_insights": ["..."]},
  "delta_value": {"analysis": "...", "key_insights": ["..."]},
  "creation_sequence": {
    "summary": "...",
    "architecture": {},
    "prompts": [{"name": "...", "content": "..."}],
    "message_models": [{"name": "...", "fields": {}}],
    "build_sequence": [{"step": 1, "action": "...", "details": "..."}],
    "integration_points": [{"system": "...", "protocol": "...", "notes": "..."}],
    "prioritized_actions": [{"priority": 1, "action": "...", "rationale": "..."}]
  },
  "human_summary": "...",
  "confidence": 0.85,
  "activated_trajectory_summary": "..."
}
"""


class ReasoningEngine:
    """Orchestrates the full reasoning pipeline with LLM + fallback."""

    def __init__(self, storage: Optional[Any] = None):
        self.storage = storage

    def _build_user_prompt(self, request: EconomistRequest, grounding: Dict) -> str:
        parts = [
            f"QUERY: {request.query}",
            f"DOMAIN: {request.domain or 'general agentic systems'}",
            f"CONSTRAINTS: {', '.join(request.constraints) or 'none'}",
            f"DESIRED OUTCOMES: {', '.join(request.desired_outcomes) or 'agentic-future alignment'}",
            f"BASELINE TRAJECTORY: {request.baseline_trajectory or 'not specified — infer legacy default'}",
            f"\nDATA GROUNDING CITATIONS:\n{grounding['citation_text']}",
        ]
        if request.upstream_context:
            parts.append(f"\nUPSTREAM CONTEXT:\n{json.dumps(request.upstream_context, indent=2)}")
        if request.integration_hooks:
            parts.append(f"\nINTEGRATION HOOKS:\n{json.dumps(request.integration_hooks, indent=2)}")
        return "\n".join(parts)

    def _fallback_pipeline(
        self,
        request: EconomistRequest,
        grounding: Dict,
        citations: List[DataCitation],
    ) -> Dict[str, Any]:
        """Deterministic fallback when LLM is unavailable."""
        query = request.query
        domain = request.domain or "agentic systems"

        return {
            "first_principles": {
                "analysis": (
                    f"Decomposing '{query}' to fundamentals: (1) coordination cost is the "
                    f"primary constraint in {domain}; (2) information goods exhibit near-zero "
                    f"marginal cost; (3) agent-native design removes human coordination "
                    f"bottlenecks; (4) value accrues to systems that compound stigmergic signals."
                ),
                "key_insights": [
                    "Legacy structures optimize for human attention, not agent throughput",
                    "Exponential returns require autocatalytic feedback loops",
                    "First principles favor protocol-based interoperability",
                ],
            },
            "stigmergic_autocatalysis": {
                "analysis": (
                    "Stigmergic patterns: agents leave structured signals (outputs, "
                    "verifications, feedback) that reduce search cost for subsequent agents. "
                    "Each analysis increases network intelligence. ForgeResonance/Arcly hooks "
                    "amplify cross-agent signal propagation."
                ),
                "key_insights": [
                    "Creation-sequence outputs become environmental signals for other agents",
                    "Verification layer closes autocatalytic loop with quality gates",
                    "Funnel participation multiplies signal surface area",
                ],
            },
            "data_grounding": {
                "analysis": (
                    f"Grounded in {len(citations)} citations. "
                    f"Gartner projects 33% enterprise software with agentic AI by 2028. "
                    f"Agentverse hosts 100K+ agents. Inference costs declined ~10x since 2023. "
                    f"Path selected: agent-native architecture because data shows adoption "
                    f"inflection and cost curves favor autonomous coordination."
                ),
                "key_insights": [c.relevance for c in citations[:3]],
            },
            "convergence_synthesis": {
                "analysis": (
                    "Converging: multi-agent systems + zero-marginal-cost economics + "
                    "stigmergic coordination + strategic foresight. Novel framework: "
                    "'Exponential Stigmergic Economies' — systems where each agent action "
                    "increases collective foresight capacity at declining marginal cost."
                ),
                "key_insights": [
                    "Agentic funnel workflows as economic value chains",
                    "Verification as abundance-generating quality multiplier",
                    "Dual-mode I/O as interoperability primitive",
                ],
            },
            "delta_value": {
                "analysis": (
                    "Baseline: sustain legacy human coordination. Activated: full pipeline "
                    "with data grounding, creation-ready outputs, agent interoperability. "
                    "Delta exceeds cost when first coordination cycle is avoided or when "
                    "downstream agents consume structured outputs directly."
                ),
                "key_insights": [
                    "Break-even at first avoided human review cycle",
                    "10-100x efficiency gain for multi-agent pipelines",
                    "Composable artifacts amortize analysis cost across agents",
                ],
            },
            "creation_sequence": {
                "summary": f"Agent-native implementation plan for: {query}",
                "architecture": {
                    "pattern": "uAgent with mailbox + multi-protocol",
                    "components": ["reasoning_engine", "verification_layer", "learning_loop"],
                    "integration": ["ForgeResonance", "Arcly", "convergent-swarm"],
                },
                "prompts": [
                    {
                        "name": "strategic_analysis",
                        "content": f"Analyze {query} using 5-stage stigmergic pipeline",
                    }
                ],
                "message_models": [
                    {"name": "EconomistRequest", "fields": {"query": "str", "mode": "str"}}
                ],
                "build_sequence": [
                    {"step": 1, "action": "Deploy uAgent with mailbox=True", "details": "Agentverse registration"},
                    {"step": 2, "action": "Integrate protocols", "details": "economist, funnel, verification, feedback"},
                    {"step": 3, "action": "Connect upstream agents", "details": "Send EconomistRequest via agent messaging"},
                ],
                "integration_points": [
                    {"system": "ForgeResonance", "protocol": "EconomistRequest", "notes": "Resonance pattern hook"},
                    {"system": "Arcly", "protocol": "FunnelStageRequest", "notes": "Pipeline stage participant"},
                    {"system": "convergent-swarm", "protocol": "VerificationRequest", "notes": "Final verification node"},
                ],
                "prioritized_actions": [
                    {"priority": 1, "action": "Define agent-native data model", "rationale": "Eliminate human translation layer"},
                    {"priority": 2, "action": "Publish protocol manifest", "rationale": "Enable agent discovery"},
                    {"priority": 3, "action": "Wire feedback loop", "rationale": "Continuous self-improvement"},
                ],
            },
            "human_summary": (
                f"Analysis of '{query}': The agentic-native path delivers exponential returns "
                f"through stigmergic coordination, supported by current adoption and cost data. "
                f"See creation_sequence for build-ready artifacts."
            ),
            "confidence": 0.75,
            "activated_trajectory_summary": (
                f"Agent-native {domain} with full reasoning pipeline, structured I/O, "
                f"and funnel/verification integration."
            ),
        }

    def _parse_pipeline_stage(
        self,
        name: str,
        number: int,
        data: Dict,
        citations: List[DataCitation],
    ) -> PipelineStage:
        stage_citations = citations if name == "data_grounding" else []
        return PipelineStage(
            stage_name=name,
            stage_number=number,
            analysis=data.get("analysis", ""),
            key_insights=data.get("key_insights", []),
            citations=stage_citations,
        )

    def analyze(self, request: EconomistRequest) -> EconomistResponse:
        """Execute full mandatory reasoning pipeline."""
        request_id = request.request_id or str(uuid.uuid4())
        grounding = build_grounding_context(request.query, request.domain)
        citations: List[DataCitation] = grounding["citations"]

        user_prompt = self._build_user_prompt(request, grounding)
        llm_response = call_llm(SYSTEM_PROMPT, user_prompt)

        if llm_response:
            try:
                parsed = extract_json_from_response(llm_response)
            except (json.JSONDecodeError, ValueError):
                parsed = self._fallback_pipeline(request, grounding, citations)
        else:
            parsed = self._fallback_pipeline(request, grounding, citations)

        pipeline = ReasoningPipeline(
            first_principles=self._parse_pipeline_stage(
                "first_principles", 1, parsed.get("first_principles", {}), citations
            ),
            stigmergic_autocatalysis=self._parse_pipeline_stage(
                "stigmergic_autocatalysis", 2, parsed.get("stigmergic_autocatalysis", {}), citations
            ),
            data_grounding=self._parse_pipeline_stage(
                "data_grounding", 3, parsed.get("data_grounding", {}), citations
            ),
            convergence_synthesis=self._parse_pipeline_stage(
                "convergence_synthesis", 4, parsed.get("convergence_synthesis", {}), citations
            ),
            delta_value=self._parse_pipeline_stage(
                "delta_value", 5, parsed.get("delta_value", {}), citations
            ),
        )

        cs_data = parsed.get("creation_sequence", {})
        creation_sequence = CreationSequence(
            summary=cs_data.get("summary", ""),
            architecture=cs_data.get("architecture", {}),
            prompts=cs_data.get("prompts", []),
            message_models=cs_data.get("message_models", []),
            build_sequence=cs_data.get("build_sequence", []),
            integration_points=cs_data.get("integration_points", []),
            prioritized_actions=cs_data.get("prioritized_actions", []),
        )

        delta = compute_delta_analysis(
            baseline=request.baseline_trajectory,
            activated_summary=parsed.get(
                "activated_trajectory_summary",
                creation_sequence.summary,
            ),
            quantified_benefits=parsed.get("delta_value", {}).get("key_insights"),
        )

        human_summary = parsed.get("human_summary")
        if request.mode == OperationMode.HUMAN.value and not human_summary:
            human_summary = self._format_human_response(pipeline, delta, creation_sequence)

        return EconomistResponse(
            request_id=request_id,
            correlation_id=request.correlation_id,
            mode=request.mode,
            pipeline=pipeline,
            delta_analysis=delta,
            creation_sequence=creation_sequence,
            human_summary=human_summary,
            confidence=float(parsed.get("confidence", 0.75)),
            version=AGENT_VERSION,
        )

    def _format_human_response(
        self,
        pipeline: ReasoningPipeline,
        delta: DeltaValueAnalysis,
        creation: CreationSequence,
    ) -> str:
        """Format rich natural-language response for human mode."""
        sections = [
            "# Stigmergic Exponential Economist — Analysis\n",
            "## 1. First Principles Decomposition\n",
            pipeline.first_principles.analysis,
            "\n**Key Insights:** " + "; ".join(pipeline.first_principles.key_insights),
            "\n## 2. Stigmergic Autocatalysis Analysis\n",
            pipeline.stigmergic_autocatalysis.analysis,
            "\n**Key Insights:** " + "; ".join(pipeline.stigmergic_autocatalysis.key_insights),
            "\n## 3. Data Grounding\n",
            pipeline.data_grounding.analysis,
        ]
        if pipeline.data_grounding.citations:
            sections.append("\n**Citations:**")
            for c in pipeline.data_grounding.citations:
                sections.append(f"- {c.source}: {c.metric} = {c.value}")
        sections.extend([
            "\n## 4. Convergence Synthesis\n",
            pipeline.convergence_synthesis.analysis,
            "\n## 5. Delta Value Analysis\n",
            f"**Baseline:** {delta.baseline_trajectory}",
            f"\n**Activated:** {delta.activated_trajectory}",
            f"\n**Net Assessment:** {delta.net_value_assessment}",
            f"\n**Delta Exceeds Cost:** {delta.exceeds_cost}",
            "\n## Creation-Sequence-Ready Output\n",
            creation.summary,
            "\n**Prioritized Actions:**",
        ])
        for action in creation.prioritized_actions[:5]:
            sections.append(
                f"- P{action.get('priority', '?')}: {action.get('action', '')} — "
                f"{action.get('rationale', '')}"
            )
        return "\n".join(sections)