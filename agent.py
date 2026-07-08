"""
Stigmergic Exponential Economist — uAgent for Fetch.ai Agentverse.

Universal strategic foresight and verification agent for the Agentic Age.
Executes mandatory 5-stage reasoning pipeline on every input.

Protocols:
  - Chat Protocol (human interaction via Agentverse / ASI:One)
  - Economist Protocol (structured agent-to-agent analysis)
  - Funnel Protocol (pipeline stage participation)
  - Verification Protocol (final verification layer)
  - Feedback Protocol (learning loop)
"""

import asyncio
import os
from datetime import datetime, timezone

# Python 3.10+ requires explicit event loop before uAgent init
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
from uuid import uuid4

from dotenv import load_dotenv
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

from models.requests import EconomistRequest, OperationMode
from protocols.economist import economist_proto
from protocols.feedback import feedback_proto
from protocols.funnel import funnel_proto
from protocols.verification import verification_proto
from utils.reasoning import AGENT_VERSION, ReasoningEngine

load_dotenv()

# --- Agent Configuration ---

AGENT_NAME = os.getenv("AGENT_NAME", "stigmergic-exponential-economist")
AGENT_SEED = os.getenv("AGENT_SEED_PHRASE", "stigmergic_exponential_economist_seed_v1")
AGENT_PORT = int(os.getenv("AGENT_PORT", "8002"))

agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    port=AGENT_PORT,
    mailbox=True,
    publish_agent_details=True,
)

# --- Chat Protocol (Human Mode) ---

chat_proto = Protocol(spec=chat_protocol_spec)
reasoning_engine = ReasoningEngine()


@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage) -> None:
    """Handle human chat messages — full reasoning pipeline in human mode."""
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(timezone.utc), acknowledged_msg_id=msg.msg_id),
    )

    text = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text

    if not text.strip():
        text = "Provide a strategic question about agentic systems or exponential economics."

    ctx.logger.info(f"Human query from {sender}: {text[:100]}...")

    request = EconomistRequest(
        query=text,
        mode=OperationMode.HUMAN.value,
        request_id=str(uuid4()),
    )

    try:
        response = reasoning_engine.analyze(request)
        reply = response.human_summary or "Analysis complete. See structured output for details."
    except Exception:
        ctx.logger.exception("Error in reasoning pipeline")
        reply = (
            "I encountered an error processing your request. "
            "Please try again or send an EconomistRequest via agent protocol."
        )

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=reply),
                EndSessionContent(type="end-session"),
            ],
        ),
    )


@chat_proto.on_message(ChatAcknowledgement)
async def handle_chat_ack(ctx: Context, sender: str, msg: ChatAcknowledgement) -> None:
    """Acknowledge chat acknowledgements (read receipts)."""
    pass


# --- Agent Startup ---

@agent.on_event("startup")
async def on_startup(ctx: Context) -> None:
    """Log agent identity and capabilities on startup."""
    ctx.logger.info(f"Stigmergic Exponential Economist v{AGENT_VERSION}")
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info("Protocols: Chat, Economist, Funnel, Verification, Feedback")
    ctx.logger.info(
        "Pipeline: First Principles → Stigmergic → Data Grounding → "
        "Convergence → Delta Value"
    )


# --- Register Protocols ---

agent.include(chat_proto, publish_manifest=True)
agent.include(economist_proto, publish_manifest=True)
agent.include(funnel_proto, publish_manifest=True)
agent.include(verification_proto, publish_manifest=True)
agent.include(feedback_proto, publish_manifest=True)


if __name__ == "__main__":
    agent.run()