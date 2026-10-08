from abc import ABC, abstractmethod

from research_agent.llm.models import LLMResponse

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self , messages: list[dict]) -> LLMResponse:
        raise NotImplementedError
