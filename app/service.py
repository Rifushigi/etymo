from typing import Dict

from openai import OpenAI

from app.errors import A2AErrorCode, A2AException


_CACHE: Dict[str, str] = {}
client = OpenAI()


async def get_etymology(word: str) -> str:
    if not word:
        return "No word provided."
    
    key = word.lower().strip().split()[0]
    if key in _CACHE:
        return _CACHE[key]
    
    system_prompt = f"""
    You are an expert in etymology and word origins.

    Provide a concise etymology (2–5 sentences) for the word provided to you.

    Rules:
    - Pick the first word if more than one word or a sentence is provided.
    - If it's a historical word: include origin language(s), meaning of components, and approximate entry into English.
    - If the word is a modern coined term, product name, brand, or company (e.g., "Facebook", "GitHub"):
        - Explain it as a coined / compound / invented term, not ancient etymology.
    - If it is an acronym (e.g., "NASA", "FIFA"):
        - Expand the acronym and give founding context instead of linguistic etymology.
    - If it's a portmanteau (e.g., "brunch", "motel"):
        - Explain the blended roots.
    - If the origin is unknown: say it's uncertain or debated — do NOT fabricate details.

    Keep the answer factual, concise, and clear. Avoid speculation.
    """

    try:
        response = client.responses.create(
            model='chatgpt-4o-latest',
            instructions=system_prompt,
            temperature=0.2,
            input=word
        )

        etymology = response.output_text.strip()

        if not etymology:
            raise A2AException(
                code=A2AErrorCode.INTERNAL_ERROR,
                message="Model returned empty response."
            )
        
        _CACHE[key] = etymology
        return etymology
        
    except A2AException:
        raise

    except Exception as e:
        raise A2AException(
            code=A2AErrorCode.INTERNAL_ERROR,
            message="Failed to fetch etymology.",
            data = {"error": str(e)}
        )