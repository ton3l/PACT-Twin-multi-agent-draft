import os
from typing import cast

from langchain_groq import ChatGroq
from pydantic import SecretStr


def gpt_oss_120b():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
        api_key=cast(SecretStr, os.getenv("GROQ_API_KEY")),
        # other params...
    )