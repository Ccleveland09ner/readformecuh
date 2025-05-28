from openai import OpenAI, APIConnectionError
from fastapi import HTTPException
from backend.app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)

async def get_summary(text: str, words: int = 200) -> str:
    """
    Return a ~N-word plain-language summary of `text`.
    """
    prompt = (
        f"Summarise the following document in about {words} words, "
        "using plain language and write in the perspective the document was written(eg. first person, etc):\n\n" + text
    )
    try:
        resp = client.chat.completions.create(
            model=settings.summary_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=words * 3,
        )
        return resp.choices[0].message.content.strip()

    except APIConnectionError as e:
        # Upstream unreachable (DNS, proxy, offline, etc.)
        raise HTTPException(
            status_code=502,
            detail="Could not reach OpenAI servers. "
                   "Check your internet connection or proxy settings.",
        ) from e
