# Learning Loop

## Purpose

The built-in learning loop enables the Stigmergic Exponential Economist to **continuously improve** based on structured feedback from humans and other agents. It implements human-in-the-loop prompt evolution — the agent proposes improvements but requires review before applying them.

## Architecture

```
Feedback (human/agent)
        │
        ▼
┌───────────────────┐
│ Feedback Protocol  │ ← FeedbackRequest
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  LearningLoop     │
│  - Store feedback │
│  - Update stats   │
│  - Identify gaps  │
│  - Propose evolution │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Agent Storage    │
│  - feedback_log   │
│  - feedback_stats │
│  - prompt_evolution │
└───────────────────┘
```

## Feedback Types

| Type | What It Measures |
|------|-----------------|
| `general` | Overall usefulness |
| `reasoning` | Pipeline quality (stages 1-2, 4-5) |
| `data` | Data grounding quality (stage 3) |
| `output` | Creation-sequence usefulness |
| `verification` | Verification accuracy |

## Feedback Request Schema

```python
FeedbackRequest(
    target_request_id="req-abc-123",  # Links to EconomistResponse.request_id
    rating=4,                          # 1-5 scale
    feedback_type="data",
    comments="Citations were relevant but could be fresher",
    suggested_improvements=[
        "Add live Agentverse agent count API",
        "Refresh quarterly metrics",
    ],
    source="human",  # or "agent"
)
```

## Improvement Detection

The learning loop monitors:

1. **Average ratings per feedback type** against thresholds:
   - `reasoning`: 3.0
   - `data`: 3.5
   - `output`: 3.5
   - `verification`: 3.0
   - `general`: 3.5

2. **Low individual ratings** (<= 2) trigger immediate opportunity flags

3. **Suggested improvements** from feedback are aggregated

## Prompt Evolution (Human-in-the-Loop)

When improvement opportunities are detected, the loop proposes prompt evolution:

```json
{
  "proposed_at": "2026-07-08T12:00:00Z",
  "trigger": "feedback rating 2 on data",
  "opportunities": ["Improve data: avg rating 2.5 below threshold 3.5"],
  "suggested_changes": [
    "Strengthen data grounding citation requirements in Stage 3",
    "Add explicit delta cost quantification templates in Stage 5",
    "Expand creation_sequence schema with deployment artifacts"
  ],
  "status": "pending_review"
}
```

**Important**: Proposals are stored with `status: pending_review`. They are NOT auto-applied. A human or supervising agent must review and approve before updating the core reasoning prompt.

## Storage Keys

| Key | Content |
|-----|---------|
| `see_feedback_log` | JSON array of feedback entries (last 500) |
| `see_feedback_stats` | Aggregated ratings by feedback type |
| `see_prompt_evolution` | Prompt evolution proposals (last 20) |
| `see_core_prompt` | Active core prompt (for future versioning) |

## Usage

### Via Protocol

```python
await ctx.send(
    economist_address,
    FeedbackRequest(
        target_request_id=response.request_id,
        rating=5,
        feedback_type="output",
        comments="Creation sequence was directly usable",
        source="agent",
    ),
)
```

### Local Example

```bash
python examples/feedback_example.py
```

## Reviewing Prompt Evolution

1. Run agent and collect feedback over time
2. Inspect `see_prompt_evolution` in agent storage (via Inspector or custom endpoint)
3. Review proposed changes
4. If approved, update `SYSTEM_PROMPT` in `utils/reasoning.py`
5. Increment `AGENT_VERSION`
6. Mark proposal status as `approved` in storage

## Metrics to Monitor

- Average rating by feedback type (trending up = improving)
- Feedback volume (more feedback = more learning signal)
- Prompt evolution proposal frequency (high = needs attention)
- Correlation between low `data` ratings and citation freshness

## Future Enhancements

- Automated A/B testing of prompt variants
- Vector storage for feedback similarity clustering
- Cross-agent feedback aggregation in multi-agent deployments
- Dashboard for feedback stats visualization
- Auto-refresh of data grounding knowledge base based on `data` feedback patterns