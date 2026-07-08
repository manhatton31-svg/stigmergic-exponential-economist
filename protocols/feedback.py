"""
Feedback protocol — learning loop input from humans and other agents.
"""

from uagents import Context, Protocol

from models.requests import FeedbackRequest
from models.responses import FeedbackResponse
from utils.learning import LearningLoop

feedback_proto = Protocol(name="StigmergicFeedbackProtocol", version="1.0.0")


@feedback_proto.on_message(model=FeedbackRequest, replies=FeedbackResponse)
async def handle_feedback(
    ctx: Context,
    sender: str,
    msg: FeedbackRequest,
) -> None:
    """Record feedback and trigger learning loop analysis."""
    ctx.logger.info(
        f"Feedback from {sender}: rating={msg.rating}, type={msg.feedback_type}"
    )

    loop = LearningLoop(storage=ctx.storage)
    response = loop.record_feedback(msg)
    await ctx.send(sender, response)