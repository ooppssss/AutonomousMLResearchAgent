from pathlib import Path
from dataclasses import dataclass
import yaml

@dataclass
class ModelConfig:
    name: str
    provider: str
    model: str

    temperature: float = 0.0
    max_tokens : int | None = None


def load_model_config(path: str | Path) -> dict[str, ModelConfig]:
    path = Path(path)

    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    configs = {}

    for name, config in data.get("models", {}).items():
        configs[name] = ModelConfig(
            name = name, 
            provider=config["provider"],
            model = config["model"],
            temperature= config.get("temperature", 0.0),
            max_tokens= config.get("max_tokens", 0)
        )

    return config