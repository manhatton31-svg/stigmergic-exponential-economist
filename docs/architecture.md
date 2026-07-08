# Architecture

## Overview

The Stigmergic Exponential Economist is a uAgent designed for Fetch.ai Agentverse with `mailbox=True`. It serves as a universal strategic foresight and verification node in the agentic ecosystem.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        agent.py                              │
│  uAgent (mailbox=True) + Chat Protocol + 4 Custom Protocols │
└──────────┬──────────┬──────────┬──────────┬────────────────┘
           │          │          │          │
    ┌──────▼──┐ ┌─────▼────┐ ┌──▼──────┐ ┌─▼────────┐
    │  Chat   │ │ Economist│ │ Funnel  │ │Verification│
    │ (Human) │ │ Protocol │ │ Protocol│ │ Protocol  │
    └────┬────┘ └─────┬────┘ └──┬──────┘ └─────┬────┘
         │            │         │               │
         └────────────┴────┬────┴───────────────┘
                           │
                  ┌────────▼────────┐
                  │ ReasoningEngine   │
                  │ (5-stage pipeline)│
                  └────────┬──────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼─────┐ ┌───▼────┐ ┌────▼──────┐
       │Data        │ │Delta   │ │Learning   │
       │Grounding   │ │Analysis│ │Loop       │
       └────────────┘ └────────┘ └───────────┘
```

## Phased Implementation

### Phase 1 (Core MVP) — Implemented

- Full 5-stage mandatory reasoning pipeline
- Data grounding with curated citations
- Delta value analysis
- Dual-mode operation (human chat + agentic structured)
- Creation-sequence-ready outputs

### Phase 2 — Implemented (Protocol Layer)

- Economist protocol for universal agent collaboration
- Funnel protocol for pipeline stage participation
- Verification protocol as final verification layer
- Integration hooks for ForgeResonance, Arcly, convergent-swarm

### Phase 3 — Implemented (Learning Loop)

- Feedback protocol for structured feedback collection
- Agent storage for feedback logs and statistics
- Improvement opportunity identification
- Prompt evolution proposals (human-in-the-loop)

## Module Responsibilities

| Module | Responsibility |
|--------|---------------|
| `agent.py` | uAgent setup, protocol registration, chat handler |
| `models/` | Structured request/response schemas |
| `protocols/` | Message handlers for each protocol |
| `utils/reasoning.py` | Pipeline orchestration |
| `utils/data_grounding.py` | Citation selection and grounding |
| `utils/delta_analysis.py` | Baseline vs activated comparison |
| `utils/verification.py` | Agentic-future rubric evaluation |
| `utils/learning.py` | Feedback storage and prompt evolution |
| `utils/llm.py` | ASI:One / OpenAI client wrapper |

## Data Flow

1. **Input** arrives via Chat (human) or custom protocol (agent)
2. **ReasoningEngine** executes 5-stage pipeline with data grounding
3. **Output** returned as `EconomistResponse` (agentic) or formatted text (human)
4. **Optional**: downstream verification via `VerificationRequest`
5. **Optional**: feedback via `FeedbackRequest` triggers learning loop

## Extensibility

- Add live data APIs in `data_grounding.py` without changing protocols
- Swap LLM provider via environment variables
- Add new protocols by creating handler + `agent.include()`
- Learning loop prompt evolution stored in agent storage for review