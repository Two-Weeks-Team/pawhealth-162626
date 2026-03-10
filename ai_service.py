import os
import json
import re
import httpx
from typing import Any, Dict, List

_INFERENCE_URL = "https://inference.do-ai.run/v1/chat/completions"
_DEFAULT_MODEL = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")
_API_KEY = os.getenv("DIGITALOCEAN_INFERENCE_KEY")


def _extract_json(text: str) -> str:
    """Extract JSON from LLM markdown or raw string."""
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


def _coerce_unstructured_payload(raw_text: str) -> Dict[str, Any]:
    compact = raw_text.strip()
    tags = [part.strip(" -•\t") for part in re.split(r",|\\n", compact) if part.strip(" -•\t")]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": compact,
        "tags": tags[:6],
    }


async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {_API_KEY}" if _API_KEY else "",
        "Content-Type": "application/json",
    }
    payload = {
        "model": _DEFAULT_MODEL,
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "stream": False,
    }
    timeout = httpx.Timeout(90.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.post(_INFERENCE_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # The LLM response is typically under 'choices[0].message.content'
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            extracted = _extract_json(content)
            return json.loads(extracted) if extracted else {"note": "AI returned empty response"}
        except Exception as e:
            # Any error – return a graceful fallback dict
            return {"note": f"AI service unavailable: {str(e)}"}


async def call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    """Public wrapper used by route handlers."""
    return await _call_inference(messages, max_tokens)
