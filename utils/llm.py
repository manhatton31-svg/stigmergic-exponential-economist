"""
LLM client wrapper — supports ASI:One and OpenAI-compatible endpoints.
"""

import json
import os
import re
from typing import Any, Dict, Optional

# Optional dependency — graceful fallback when not configured.
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore


def get_llm_client() -> Optional[Any]:
    """Create OpenAI-compatible client from environment."""
    if OpenAI is None:
        return None

    api_key = os.getenv("ASI_ONE_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("LLM_BASE_URL", "https://api.asi1.ai/v1")
    return OpenAI(base_url=base_url, api_key=api_key)


def get_model_name() -> str:
    """Resolve model name from environment."""
    return os.getenv("LLM_MODEL", "asi1")


def extract_json_from_response(text: str) -> Dict[str, Any]:
    """Extract JSON object from LLM response, handling markdown fences."""
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence_match:
        text = fence_match.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Attempt to find first JSON object in text
        brace_match = re.search(r"\{[\s\S]*\}", text)
        if brace_match:
            return json.loads(brace_match.group())
        raise


def call_llm(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> Optional[str]:
    """Call LLM and return response text. Returns None if unavailable."""
    client = get_llm_client()
    if client is None:
        return None

    try:
        response = client.chat.completions.create(
            model=get_model_name(),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return str(response.choices[0].message.content)
    except Exception:
        return None