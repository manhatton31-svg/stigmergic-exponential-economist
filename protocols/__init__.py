"""Custom protocols for agent-to-agent communication."""

from protocols.economist import economist_proto
from protocols.feedback import feedback_proto
from protocols.funnel import funnel_proto
from protocols.verification import verification_proto

__all__ = [
    "economist_proto",
    "feedback_proto",
    "funnel_proto",
    "verification_proto",
]