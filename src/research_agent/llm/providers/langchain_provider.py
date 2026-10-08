from langchain_core.messages import HumanMessage, SystemMessage

from .base import BaseLLMProvider
from ..models import LLMResponse


class LangChainProvider(BaseLLMProvider):

    def __init__(self, config, llm):
        self.config = config
        self.llm = llm

    async def generate(
        self,
        messages: list[dict],
    ) -> LLMResponse:

        lc_messages = []

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "system":
                lc_messages.append(SystemMessage(content=content))

            elif role == "user":
                lc_messages.append(HumanMessage(content=content))

        response = await self.llm.ainvoke(lc_messages)

        usage = getattr(response, "usage_metadata", {}) or {}

        return LLMResponse(
            content=response.content,
            model=self.config.model,
            provider=self.config.provider,
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            raw_response=response,
        )