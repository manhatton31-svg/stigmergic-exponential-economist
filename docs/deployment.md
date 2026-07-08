# Deployment

## Prerequisites

- Python 3.10+
- ASI:One API key (recommended) or OpenAI API key
- Fetch.ai testnet tokens for Almanac registration (optional for local dev)

## Local Setup

```bash
# Clone repository
git clone https://github.com/manhatton31-svg/stigmergic-exponential-economist.git
cd stigmergic-exponential-economist

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys and seed phrase
```

## Run Locally

```bash
python agent.py
```

Expected output:
```
INFO: [stigmergic-exponential-economist]: Stigmergic Exponential Economist v1.0.0
INFO: [stigmergic-exponential-economist]: Agent address: agent1q...
INFO: [stigmergic-exponential-economist]: Starting mailbox client for https://agentverse.ai
INFO: [stigmergic-exponential-economist]: Manifest published successfully
```

## Run Examples (Without Agent)

```bash
python examples/human_example.py
python examples/agent_funnel_example.py
python examples/verification_example.py
python examples/feedback_example.py
```

## Agentverse Registration (Manual Steps)

See README.md for step-by-step Agentverse registration instructions.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `AGENT_SEED_PHRASE` | Yes (prod) | Unique seed for stable agent address |
| `ASI_ONE_API_KEY` | Recommended | ASI:One LLM API key |
| `OPENAI_API_KEY` | Alternative | OpenAI API key (if not using ASI:One) |
| `AGENT_PORT` | No | Default 8002 |
| `LLM_MODEL` | No | Default `asi1` |
| `LLM_BASE_URL` | No | Default `https://api.asi1.ai/v1` |

## Production Considerations

- Use a unique `AGENT_SEED_PHRASE` and store securely
- Configure live data grounding API for fresh metrics
- Monitor feedback stats via agent storage
- Review prompt evolution proposals regularly
- Set up process manager (systemd, pm2) for persistent running