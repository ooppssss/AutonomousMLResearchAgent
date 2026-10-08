class LLMError(Exception):
    """Base exception for LLM-related errors."""


class ModelNotFoundError(LLMError):
    """Requested model configuration does not exist."""


class ProviderNotFoundError(LLMError):
    """Requested provider is not supported."""