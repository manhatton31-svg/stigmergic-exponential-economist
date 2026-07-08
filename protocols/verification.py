"""
Verification protocol — final verification layer for agentic-future alignment.
"""

from uagents import Context, Protocol

from models.requests import VerificationRequest
from models.responses import VerificationResponse
from utils.verification import VerificationEngine

verification_proto = Protocol(name="StigmergicVerificationProtocol", version="1.0.0")


@verification_proto.on_message(model=VerificationRequest, replies=VerificationResponse)
async def handle_verification(
    ctx: Context,
    sender: str,
    msg: VerificationRequest,
) -> None:
    """Evaluate artifact against agentic-future verification rubric."""
    ctx.logger.info(
        f"Verification request from {sender} for artifact type: {msg.artifact_type}"
    )

    engine = VerificationEngine()
    response = engine.verify(msg)

    ctx.storage.set(
        f"verification_{msg.verification_id or 'latest'}",
        response.model_dump_json(),
    )
    await ctx.send(sender, response)