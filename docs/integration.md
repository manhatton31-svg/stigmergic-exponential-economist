# Integration Guide

## Universal Agent Collaboration

Any agent can interact with the Economist by sending structured messages.

### Economist Protocol

```python
from uagents import Agent, Context
from models.requests import EconomistRequest
from models.responses import EconomistResponse

@my_agent.on_event("startup")
async def query_economist(ctx: Context):
    economist_address = "agent1q..."  # Economist agent address

    await ctx.send(
        economist_address,
        EconomistRequest(
            query="Design a stigmergic coordination layer for my agent swarm",
            mode="agentic",
            domain="multi-agent coordination",
            integration_hooks={"ForgeResonance": "resonance-v2"},
        ),
    )

@my_agent.on_message(model=EconomistResponse)
async def handle_response(ctx: Context, sender: str, msg: EconomistResponse):
    build_sequence = msg.creation_sequence.build_sequence
    # Use creation_sequence directly in your build process
```

### Protocol Manifest Names

| Protocol | Name | Version |
|----------|------|---------|
| Economist | `StigmergicEconomistProtocol` | 1.0.0 |
| Funnel | `StigmergicFunnelProtocol` | 1.0.0 |
| Verification | `StigmergicVerificationProtocol` | 1.0.0 |
| Feedback | `StigmergicFeedbackProtocol` | 1.0.0 |
| Chat | `AgentChatProtocol` | (standard) |

## Funnel Workflow Integration

```python
from models.requests import FunnelStageRequest

await ctx.send(
    economist_address,
    FunnelStageRequest(
        stage_name="strategic_analysis",
        stage_index=1,
        total_stages=3,
        query="Analyze marketplace architecture",
        prior_stages=[stage1_output_dict],
        pipeline_id="pipeline-abc-123",
    ),
)
```

The Economist enriches the query with prior stage context and returns a `FunnelStageResponse` with handoff notes.

## Verification Integration

```python
from models.requests import VerificationRequest

await ctx.send(
    economist_address,
    VerificationRequest(
        artifact=my_agent_output.model_dump(),
        artifact_type="MarketplaceDesign",
        original_intent="Build agent-native marketplace",
    ),
)
```

## ForgeResonance Integration

Pass resonance context via `integration_hooks`:

```python
EconomistRequest(
    query="...",
    integration_hooks={
        "ForgeResonance": "pattern-resonance-v2",
        "resonance_context": "swarm-coordination",
    },
)
```

## Arcly Integration

Use funnel protocol with Arcly pipeline IDs:

```python
FunnelStageRequest(
    pipeline_id="arcly-pipeline-id",
    stage_name="economist_analysis",
    ...
)
```

## Convergent-Swarm Integration

Use as final verification node in swarm patterns:

```python
VerificationRequest(
    artifact=swarm_consensus_output,
    original_intent="Swarm design goal",
    criteria=["stigmergic coordination", "exponential returns"],
)
```

## Human Interaction

Humans interact via:
- **Agentverse Chat UI** — standard chat protocol
- **ASI:One** — discoverable via published manifest

No code required; send natural language queries.