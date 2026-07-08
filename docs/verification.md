# Verification Layer

## Purpose

The verification layer acts as a **final quality gate** before deploying systems into the agentic ecosystem. It evaluates whether outputs advance the desired agentic future rather than sustaining legacy human-made structures.

## When to Verify

- **Before deployment** of any agent-designed system
- **End of funnel pipelines** as the final stage
- **Swarm consensus outputs** (convergent-swarm pattern)
- **Human review checkpoints** for high-stakes decisions

## Verification Rubric

Default criteria (override via `VerificationRequest.criteria`):

| Criterion | What It Checks |
|-----------|---------------|
| Exponential returns | Does the output enable compound growth, not linear incrementalism? |
| Zero-marginal-cost dynamics | Does it leverage near-zero replication cost for information goods? |
| Stigmergic coordination | Can agents leave signals that reduce coordination cost for others? |
| Abundance generation | Does it create composable, open value rather than artificial scarcity? |
| Agent-interoperable outputs | Are outputs structured for machine consumption without human translation? |
| Bottleneck reduction | Does it remove human coordination layers that limit throughput? |

## Scoring

Each criterion receives:
- **passed** (boolean): score >= 0.4
- **score** (0.0–1.0): based on alignment signal matching
- **evidence**: which signals were detected in the artifact

**Overall score** = average of criterion scores.

**Approval** requires:
- Overall score >= 0.6
- At least half of criteria passed

**Blocking issues** = criteria with score < 0.3 that failed.

## Usage

### Via Protocol (Agent-to-Agent)

```python
from models.requests import VerificationRequest

response = await ctx.send(
    economist_address,
    VerificationRequest(
        artifact={
            "pipeline": {...},
            "creation_sequence": {...},
            "architecture": {"pattern": "uAgent multi-protocol"},
        },
        artifact_type="EconomistResponse",
        original_intent="Build stigmergic coordination hub",
        mode="agentic",
    ),
)
```

### Standalone (Local)

```bash
python examples/verification_example.py
```

### Programmatic

```python
from utils.verification import VerificationEngine

engine = VerificationEngine()
result = engine.verify(verification_request)

if result.approved:
    proceed_to_deployment()
else:
    address_blocking_issues(result.blocking_issues)
```

## Response Structure

```python
VerificationResponse:
  approved: bool              # Can proceed to deployment?
  overall_score: float       # 0.0–1.0
  verdicts: [VerificationVerdict]  # Per-criterion evaluation
  agentic_future_alignment: str     # Summary assessment
  recommendations: [str]     # Actionable next steps
  blocking_issues: [str]      # Must-fix issues
  human_summary: str          # Rich text (human mode)
```

## Funnel Integration Pattern

```
Stage 1: Research Agent → findings
Stage 2: Economist Agent → creation_sequence
Stage 3: Builder Agent → implementation artifact
Stage 4: VERIFICATION → approved/rejected
Stage 5: Deploy (only if approved)
```

## Custom Criteria

Override defaults for domain-specific verification:

```python
VerificationRequest(
    artifact=my_output,
    original_intent="Design payment protocol",
    criteria=[
        "Supports agent-to-agent micropayments",
        "Zero-marginal-cost settlement",
        "Protocol-standard message models",
    ],
)
```

## Extending Verification

The current implementation uses heuristic signal matching. For production:

1. Add LLM-based evaluation in `utils/verification.py`
2. Integrate domain-specific rubrics per `artifact_type`
3. Store verification history in agent storage for trend analysis
4. Connect to CI/CD gates for automated pre-deployment checks

## Human Review

When `mode="human"`, the response includes a formatted `human_summary` with pass/fail per criterion, blocking issues, and recommendations suitable for direct presentation to decision-makers.