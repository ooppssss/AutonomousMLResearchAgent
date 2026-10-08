from .config import ModelConfig
from .exceptions import ModelNotFoundError, ProviderNotFoundError
from .providers.langchain_provider import LangChainProvider
from pydantic import SecretStr
import os
from dotenv import load_dotenv

load_dotenv()


class LLMRouter:

    def __init__(self, configs: dict[str, ModelConfig]):
        self.configs = configs
        self.providers = {}

    def get(self, name: str):

        if name not in self.configs:
            raise ModelNotFoundError(
                f"Model configuration '{name}' not found."
            )

        config = self.configs[name]

        if config.provider == "openai":
            return self._create_openai(config)

        if config.provider == "anthropic":
            return self._create_anthropic(config)

        if config.provider == "google":
            return self._create_google(config)

        if config.provider == "openrouter":
            return self._create_openrouter(config)

        raise ProviderNotFoundError(
            f"Provider '{config.provider}' is not supported."
        )

    def _create_openai(self, config):
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model=config.model,
            temperature=config.temperature,
            max_completion_tokens=config.max_tokens,
        )

        return LangChainProvider(config, llm)


    def _create_anthropic(self, config):
        from langchain_anthropic import ChatAnthropic

        llm = ChatAnthropic(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )

        return LangChainProvider(config, llm)


    def _create_google(self, config):
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model=config.model,
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
        )

        return LangChainProvider(config, llm)


    def _create_openrouter(self, config):
        from langchain_openai import ChatOpenAI

        api_key = os.getenv("OPENROUTER_API_KEY")

        llm = ChatOpenAI(
            model=config.model,
            temperature=config.temperature,
            max_completion_tokens=config.max_tokens,
            base_url="https://openrouter.ai/api/v1",
            api_key=SecretStr(api_key) if api_key else None,
        )

        return LangChainProvider(config, llm)