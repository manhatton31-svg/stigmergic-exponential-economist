"""
Built-in learning loop — feedback collection, storage, analysis, prompt evolution.

Phase 3 implementation with extensible storage via uAgent ctx.storage.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from models.requests import FeedbackRequest
from models.responses import FeedbackResponse

FEEDBACK_STORAGE_KEY = "see_feedback_log"
FEEDBACK_STATS_KEY = "see_feedback_stats"
PROMPT_EVOLUTION_KEY = "see_prompt_evolution"
CORE_PROMPT_KEY = "see_core_prompt"

IMPROVEMENT_THRESHOLDS = {
    "reasoning": 3.0,
    "data": 3.5,
    "output": 3.5,
    "verification": 3.0,
    "general": 3.5,
}


class LearningLoop:
    """Manages feedback collection and prompt evolution proposals."""

    def __init__(self, storage: Any):
        self.storage = storage

    def _get_feedback_log(self) -> List[Dict]:
        if self.storage.has(FEEDBACK_STORAGE_KEY):
            return json.loads(self.storage.get(FEEDBACK_STORAGE_KEY))
        return []

    def _save_feedback_log(self, log: List[Dict]) -> None:
        self.storage.set(FEEDBACK_STORAGE_KEY, json.dumps(log))

    def _update_stats(self, feedback: FeedbackRequest) -> Dict:
        stats = {}
        if self.storage.has(FEEDBACK_STATS_KEY):
            stats = json.loads(self.storage.get(FEEDBACK_STATS_KEY))

        ftype = feedback.feedback_type
        if ftype not in stats:
            stats[ftype] = {"count": 0, "total_rating": 0, "avg_rating": 0.0}
        stats[ftype]["count"] += 1
        stats[ftype]["total_rating"] += feedback.rating
        stats[ftype]["avg_rating"] = (
            stats[ftype]["total_rating"] / stats[ftype]["count"]
        )

        self.storage.set(FEEDBACK_STATS_KEY, json.dumps(stats))
        return stats

    def record_feedback(self, feedback: FeedbackRequest) -> FeedbackResponse:
        """Store feedback and analyze improvement opportunities."""
        feedback_id = str(uuid.uuid4())
        entry = {
            "id": feedback_id,
            "target_request_id": feedback.target_request_id,
            "rating": feedback.rating,
            "feedback_type": feedback.feedback_type,
            "comments": feedback.comments,
            "suggested_improvements": feedback.suggested_improvements,
            "source": feedback.source,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        log = self._get_feedback_log()
        log.append(entry)
        # Retain last 500 entries
        if len(log) > 500:
            log = log[-500:]
        self._save_feedback_log(log)

        stats = self._update_stats(feedback)
        opportunities = self._identify_opportunities(stats, feedback)
        evolution = self._propose_prompt_evolution(opportunities, feedback)

        return FeedbackResponse(
            feedback_id=feedback_id,
            accepted=True,
            message="Feedback recorded. Learning loop updated.",
            improvement_opportunities=opportunities,
            prompt_evolution_proposed=evolution is not None,
            prompt_evolution_summary=evolution,
        )

    def _identify_opportunities(
        self,
        stats: Dict,
        feedback: FeedbackRequest,
    ) -> List[str]:
        """Identify improvement areas from stats and current feedback."""
        opportunities = []

        for ftype, data in stats.items():
            threshold = IMPROVEMENT_THRESHOLDS.get(ftype, 3.5)
            if data["avg_rating"] < threshold:
                opportunities.append(
                    f"Improve {ftype}: avg rating {data['avg_rating']:.1f} "
                    f"below threshold {threshold}"
                )

        if feedback.rating <= 2:
            opportunities.append(
                f"Low rating ({feedback.rating}/5) on request "
                f"{feedback.target_request_id}: {feedback.comments or 'no comments'}"
            )

        opportunities.extend(feedback.suggested_improvements)
        return list(dict.fromkeys(opportunities))  # dedupe preserving order

    def _propose_prompt_evolution(
        self,
        opportunities: List[str],
        feedback: FeedbackRequest,
    ) -> Optional[str]:
        """Propose core prompt updates for human/agent review."""
        if not opportunities and feedback.rating >= 4:
            return None

        stats = {}
        if self.storage.has(FEEDBACK_STATS_KEY):
            stats = json.loads(self.storage.get(FEEDBACK_STATS_KEY))

        proposal = {
            "proposed_at": datetime.now(timezone.utc).isoformat(),
            "trigger": f"feedback rating {feedback.rating} on {feedback.feedback_type}",
            "opportunities": opportunities,
            "suggested_changes": [
                "Strengthen data grounding citation requirements in Stage 3",
                "Add explicit delta cost quantification templates in Stage 5",
                "Expand creation_sequence schema with deployment artifacts",
            ],
            "status": "pending_review",
        }

        evolutions = []
        if self.storage.has(PROMPT_EVOLUTION_KEY):
            evolutions = json.loads(self.storage.get(PROMPT_EVOLUTION_KEY))
        evolutions.append(proposal)
        self.storage.set(PROMPT_EVOLUTION_KEY, json.dumps(evolutions[-20:]))

        return (
            f"Prompt evolution proposed based on {len(opportunities)} improvement "
            f"opportunities. Pending human/agent review. ID: {proposal['proposed_at']}"
        )

    def get_stats(self) -> Dict:
        """Return feedback statistics for monitoring."""
        if self.storage.has(FEEDBACK_STATS_KEY):
            return json.loads(self.storage.get(FEEDBACK_STATS_KEY))
        return {}