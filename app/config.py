import logging
from collections.abc import MutableMapping
from functools import lru_cache
from typing import Any
from enum import Enum
import yaml
from pydantic import BaseSettings


class ComputeDevices(Enum):
    cpu = "cpu"
    cuda = "cuda"


class Settings(BaseSettings):
    log_level: str
    server_port: int
    embeddings_device: ComputeDevices
    embeddings_messages_model: str
    embeddings_documents_model: str
    nlp_spacy_model: str

    @classmethod
    def load(cls, config_file: str = "config.yaml"):
        config = load_config(config_file)
        return cls.parse_obj(config)

    class Config:
        env_file = ".env"


@lru_cache()
def load_config(config_file: str = "config.yaml"):
    with open(config_file) as f:
        config = yaml.safe_load(f)

    if config is None:
        config = {}

    config_flattened = flatten_dict(config)
    return config_flattened


def flatten_dict(
    d: MutableMapping, parent_key: str = "", sep: str = "_"
) -> MutableMapping:
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


@lru_cache()
def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn.*")
    logger.setLevel(settings.log_level.upper())
    return logger


settings = Settings.load()
log = get_logger()
