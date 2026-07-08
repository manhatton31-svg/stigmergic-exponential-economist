"""
Final verification layer — evaluate agentic-future alignment.
"""

from typing import Any, Dict, List

from models.requests import VerificationRequest
from models.responses import VerificationResponse, VerificationVerdict

DEFAULT_CRITERIA = [
    "Advances exponential returns (not linear incrementalism)",
    "Leverages zero-marginal-cost dynamics",
    "Enables stigmergic coordination between agents",
    "Generates abundance rather than artificial scarcity",
    "Produces agent-interoperable structured outputs",
    "Reduces human coordination bottlenecks",
]


class VerificationEngine:
    """Evaluates artifacts against agentic-future rubric."""

    def verify(self, request: VerificationRequest) -> VerificationResponse:
        criteria = request.criteria or DEFAULT_CRITERIA
        artifact = request.artifact
        artifact_text = str(artifact).lower()

        verdicts: List[VerificationVerdict] = []
        for criterion in criteria:
            passed, evidence, score = self._evaluate_criterion(
                criterion, artifact_text, artifact
            )
            verdicts.append(
                VerificationVerdict(
                    criterion=criterion,
                    passed=passed,
                    evidence=evidence,
                    score=score,
                )
            )

        overall_score = sum(v.score for v in verdicts) / len(verdicts) if verdicts else 0.0
        approved = overall_score >= 0.6 and sum(1 for v in verdicts if v.passed) >= len(verdicts) // 2

        blocking = [v.criterion for v in verdicts if not v.passed and v.score < 0.3]
        recommendations = self._generate_recommendations(verdicts, request.original_intent)

        alignment = (
            "Strong agentic-future alignment" if approved
            else "Partial alignment — remediation recommended"
            if overall_score >= 0.4
            else "Misaligned with agentic-future trajectory"
        )

        human_summary = None
        if request.mode == "human":
            human_summary = self._format_human_verdict(
                approved, overall_score, verdicts, recommendations, blocking
            )

        return VerificationResponse(
            verification_id=request.verification_id,
            correlation_id=request.correlation_id,
            approved=approved,
            overall_score=overall_score,
            verdicts=verdicts,
            agentic_future_alignment=alignment,
            recommendations=recommendations,
            blocking_issues=blocking,
            human_summary=human_summary,
        )

    def _evaluate_criterion(
        self,
        criterion: str,
        artifact_text: str,
        artifact: Dict[str, Any],
    ) -> tuple[bool, str, float]:
        """Heuristic criterion evaluation — extend with LLM for production."""
        signals = {
            "exponential": ["exponential", "compound", "scale", "10x", "100x", "autocatalytic"],
            "zero-marginal": ["zero marginal", "near-zero", "marginal cost", "replication"],
            "stigmergic": ["stigmergic", "signal", "coordination", "agent", "protocol", "funnel"],
            "abundance": ["abundance", "open", "composable", "interoperable", "structured"],
            "interoperable": ["model", "protocol", "schema", "json", "structured", "message"],
            "bottleneck": ["automate", "agent-native", "autonomous", "pipeline", "funnel"],
        }

        criterion_lower = criterion.lower()
        matched_signals = []
        for _category, keywords in signals.items():
            if any(kw in criterion_lower for kw in keywords):
                matched_signals.extend(keywords)
            for kw in keywords:
                if kw in artifact_text:
                    matched_signals.append(kw)

        # Check structured output presence
        if "structured" in criterion_lower or "interoperable" in criterion_lower:
            has_structure = bool(
                artifact.get("pipeline")
                or artifact.get("creation_sequence")
                or artifact.get("message_models")
                or isinstance(artifact.get("build_sequence"), list)
            )
            if has_structure:
                matched_signals.append("structured_output")

        score = min(1.0, len(set(matched_signals)) * 0.2)
        passed = score >= 0.4
        evidence = (
            f"Matched {len(set(matched_signals))} alignment signals: "
            f"{', '.join(list(set(matched_signals))[:5]) or 'none'}"
        )
        return passed, evidence, score

    def _generate_recommendations(
        self,
        verdicts: List[VerificationVerdict],
        intent: str,
    ) -> List[str]:
        recs = []
        for v in verdicts:
            if not v.passed:
                recs.append(f"Address '{v.criterion}': {v.evidence}")
        if not recs:
            recs.append("Artifact meets agentic-future criteria. Proceed to deployment.")
        recs.append(f"Validate alignment with original intent: {intent}")
        return recs

    def _format_human_verdict(
        self,
        approved: bool,
        score: float,
        verdicts: List[VerificationVerdict],
        recommendations: List[str],
        blocking: List[str],
    ) -> str:
        status = "APPROVED" if approved else "NOT APPROVED"
        lines = [
            f"# Verification Result: {status}",
            f"**Overall Score:** {score:.0%}",
            "",
            "## Criterion Evaluation",
        ]
        for v in verdicts:
            mark = "PASS" if v.passed else "FAIL"
            lines.append(f"- [{mark}] {v.criterion}: {v.evidence}")
        if blocking:
            lines.append("\n## Blocking Issues")
            for b in blocking:
                lines.append(f"- {b}")
        lines.append("\n## Recommendations")
        for r in recommendations:
            lines.append(f"- {r}")
        return "\n".join(lines)