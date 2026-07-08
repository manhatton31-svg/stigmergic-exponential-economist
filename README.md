# Stigmergic Exponential Economist

Universal strategic foresight and verification agent for the Agentic Age on [Fetch.ai Agentverse](https://agentverse.ai).

Expert in exponential economics and zero-marginal-cost dynamics. Uses first principles + stigmergic autocatalysis to deconstruct, then convergence synthesis to generate novel frameworks for agentic economies.

## Capabilities

- **Mandatory 5-stage reasoning pipeline** on every input
- **Data-grounded analysis** with cited metrics and sources
- **Delta value analysis** comparing baseline vs agentic trajectories
- **Dual-mode operation**: rich human text + machine-structured JSON
- **Creation-sequence-ready outputs** for direct use in building
- **Universal agent collaboration** via structured protocols
- **Funnel workflow support** as a pipeline stage
- **Final verification layer** for agentic-future alignment
- **Built-in learning loop** with feedback and prompt evolution

## Quick Start

```bash
git clone https://github.com/manhatton31-svg/stigmergic-exponential-economist.git
cd stigmergic-exponential-economist
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env          # Add your API keys
python agent.py
```

## Run Examples

```bash
python examples/human_example.py
python examples/agent_funnel_example.py
python examples/verification_example.py
python examples/feedback_example.py
```

## Project Structure

```
stigmergic-exponential-economist/
├── agent.py                 # Main uAgent (mailbox=True)
├── requirements.txt
├── .env.example
├── models/                  # Structured request/response schemas
├── protocols/               # Economist, Funnel, Verification, Feedback
├── utils/                   # Reasoning, grounding, verification, learning
├── docs/                    # Architecture, principles, deployment guides
└── examples/                # Human, funnel, verification, feedback demos
```

## Protocols

| Protocol | Purpose |
|----------|---------|
| Chat | Human interaction via Agentverse / ASI:One |
| Economist | Structured agent-to-agent analysis |
| Funnel | Multi-agent pipeline stage participation |
| Verification | Final agentic-future alignment check |
| Feedback | Learning loop input |

## Documentation

- [Architecture](docs/architecture.md)
- [Principles](docs/principles.md)
- [Deployment](docs/deployment.md)
- [Integration](docs/integration.md)
- [Verification Layer](docs/verification.md)
- [Learning Loop](docs/learning-loop.md)

## Agentverse Registration (Manual Steps)

1. **Get API keys**
   - ASI:One API key from [asi1.ai/dashboard/api-keys](https://asi1.ai/dashboard/api-keys)
   - Add to `.env` as `ASI_ONE_API_KEY`

2. **Configure agent**
   - Set a unique `AGENT_SEED_PHRASE` in `.env`
   - Choose an available `AGENT_PORT` (default 8002)

3. **Run locally**
   ```bash
   python agent.py
   ```
   Note the agent address from startup logs.

4. **Connect mailbox**
   - Open the Inspector URL from startup logs
   - Or go to [agentverse.ai](https://agentverse.ai) → My Agents → Connect Local Agent
   - Paste the agent address and complete mailbox connection

5. **Verify protocols**
   - Confirm manifests published: Chat, Economist, Funnel, Verification, Feedback
   - Test via Agentverse chat UI with a strategic question

6. **Publish (optional)**
   - Register agent on Agentverse marketplace for discovery
   - Add description, avatar, and capability tags

## License

MIT