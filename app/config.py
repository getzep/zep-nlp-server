import logging
from collections.abc import MutableMapping
from enum import Enum
from functools import lru_cache
from typing import Any

import yaml
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


class ComputeDevices(Enum):
    cpu = "cpu"
    cuda = "cuda"
    mps = "mps"


class Settings(BaseSettings):
    log_level: str
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_app_name: str = "zep-nlp"
    server_port: int
    embeddings_device: ComputeDevices
    embeddings_messages_enabled: bool
    embeddings_documents_enabled: bool
    embeddings_messages_model: str
    embeddings_documents_model: str
    nlp_spacy_model: str

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings

        case_sensitive = False
        env_prefix = "zep_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    def load(cls, config_file: str = "config.yaml"):
        config = load_config(config_file)
        return cls.parse_obj(config)


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
def get_logger(log_level: str | None = None) -> logging.Logger:
    if log_level is None:
        log_level = settings.log_level

    logger = logging.getLogger(settings.log_app_name)
    logger.setLevel(log_level.upper())

    ch = logging.StreamHandler()
    ch.setLevel(log_level.upper())

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(settings.log_format)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(ch)

    return logger


settings = Settings.load()
log = get_logger()
