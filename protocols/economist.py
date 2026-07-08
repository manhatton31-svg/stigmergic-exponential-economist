"""
Economist protocol — primary agent-to-agent analysis interface.
"""

from uagents import Context, Protocol

from models.requests import EconomistRequest
from models.responses import EconomistResponse
from utils.reasoning import ReasoningEngine

economist_proto = Protocol(name="StigmergicEconomistProtocol", version="1.0.0")


@economist_proto.on_message(model=EconomistRequest, replies=EconomistResponse)
async def handle_economist_request(
    ctx: Context,
    sender: str,
    msg: EconomistRequest,
) -> None:
    """Execute mandatory reasoning pipeline and return structured response."""
    ctx.logger.info(f"Economist request from {sender}: {msg.query[:80]}...")

    engine = ReasoningEngine(storage=ctx.storage)
    response = engine.analyze(msg)

    ctx.storage.set(f"last_analysis_{response.request_id}", response.model_dump_json())
    await ctx.send(sender, response)