"""
Funnel protocol — pipeline stage participation for multi-agent workflows.
"""

from uagents import Context, Protocol

from models.requests import EconomistRequest, FunnelStageRequest
from models.responses import FunnelStageResponse
from utils.reasoning import ReasoningEngine

funnel_proto = Protocol(name="StigmergicFunnelProtocol", version="1.0.0")


@funnel_proto.on_message(model=FunnelStageRequest, replies=FunnelStageResponse)
async def handle_funnel_stage(
    ctx: Context,
    sender: str,
    msg: FunnelStageRequest,
) -> None:
    """
    Process a funnel stage — enrich query with prior stage context,
    run reasoning pipeline, return handoff-ready response.
    """
    ctx.logger.info(
        f"Funnel stage '{msg.stage_name}' ({msg.stage_index + 1}/{msg.total_stages}) "
        f"from {sender}"
    )

    # Merge prior stage outputs into upstream context
    upstream_context = {
        "pipeline_id": msg.pipeline_id,
        "stage_name": msg.stage_name,
        "prior_stages": msg.prior_stages,
    }

    economist_request = EconomistRequest(
        query=msg.query,
        mode=msg.mode,
        upstream_context=upstream_context,
        correlation_id=msg.correlation_id,
    )

    engine = ReasoningEngine(storage=ctx.storage)
    economist_response = engine.analyze(economist_request)

    handoff_notes = (
        f"Stage '{msg.stage_name}' complete. "
        f"Prior stages consumed: {len(msg.prior_stages)}. "
        f"Confidence: {economist_response.confidence:.0%}."
    )

    next_recs = []
    if msg.stage_index + 1 < msg.total_stages:
        next_recs = [
            "Pass economist_response.creation_sequence to next stage",
            "Include correlation_id for traceability",
            "Run verification if this is the final stage",
        ]

    response = FunnelStageResponse(
        pipeline_id=msg.pipeline_id,
        stage_name=msg.stage_name,
        stage_index=msg.stage_index,
        stage_complete=True,
        economist_response=economist_response,
        handoff_notes=handoff_notes,
        next_stage_recommendations=next_recs,
    )

    ctx.storage.set(
        f"funnel_{msg.pipeline_id}_{msg.stage_name}",
        response.model_dump_json(),
    )
    await ctx.send(sender, response)