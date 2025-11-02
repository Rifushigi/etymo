from typing import Any, Dict, Optional
import uuid


def make_rpc_result_message(text: str) -> Dict[str, Any]:
    return {
        "role": "agent",
        "kind": "message",
        "messageId": str(uuid.uuid4()),
        "parts": [
            {
                "kind": "text",
                "text": text
            }
        ]
    }

def extract_first_text_from_message_parts(message: Dict[str, Any]) -> Optional[str]:
    parts = message.get("parts") or []
    for p in parts:
        if p.get("kind") == "text" and p.get("text"):
            return p.get("text")
    return None