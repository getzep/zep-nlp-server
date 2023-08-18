from datetime import datetime
from functools import lru_cache
from typing import Any, List, cast

import numpy as np
import torch
from sentence_transformers import SentenceTransformer  # type: ignore

from app.config import ComputeDevices, log, settings
from app.embedding_models import Collection, Document


class Embedder:
    """Embeds a Collection of Documents using a SentenceTransformer model."""

    def __init__(self):
        device = "cpu"
        if settings.embeddings_device == ComputeDevices.cuda:
            log.info("Configured for CUDA")
            if torch.cuda.is_available():
                device = "cuda"
            else:
                log.warning("Configured for CUDA but CUDA not available, using CPU")
        elif settings.embeddings_device == ComputeDevices.mps:
            log.info("Configured for MPS")
            if torch.backends.mps.is_available():
                device = "mps"
            else:
                log.warning("Configured for MPS but MPS not available, using CPU")

        required_models: List[str] = []
        if settings.embeddings_messages_enabled:
            required_models.append(settings.embeddings_messages_model)
        if settings.embeddings_documents_enabled:
            required_models.append(settings.embeddings_documents_model)

        models: dict[str, Any] = {}
        for model_name in required_models:
            if model_name not in models:
                log.info(
                    f"Downloading model {model_name} if not present. This may take a"
                    " while."
                )
                models[model_name] = SentenceTransformer(model_name, device=device)
                log.info(f"Loaded model {model_name} on device {device}.")

        self.models = models

    def _embed_collection(
        self, collection: Collection, model_name: str
    ) -> List[np.ndarray]:
        model = self.models.get(model_name)
        if model is None:
            raise ValueError(f"Model {model_name} not found")

        start_time = datetime.now()
        log.debug(f"Embedding {len(collection.documents)} documents")
        embeddings = cast(
            List[np.ndarray],
            model.encode(
                [doc.text for doc in collection.documents], convert_to_numpy=True
            ),
        )
        end_time = datetime.now()
        log.debug(
            f"Completed embedding of {len(collection.documents)} documents in"
            f" {end_time - start_time}s"
        )
        return embeddings

    def embed(self, collection: Collection, model_name: str) -> Collection:
        """Embed a Collection of Documents. model_name must be one of the
        configured models.
        """
        embeddings = self._embed_collection(collection, model_name)
        doc: Document
        emb: np.ndarray
        for doc, emb in zip(collection.documents, embeddings):
            doc.embedding = emb
        return collection


@lru_cache()
def get_embedder() -> Embedder:
    return Embedder()
