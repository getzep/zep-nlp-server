from typing import List, cast

import numpy as np
from sentence_transformers import SentenceTransformer  # type: ignore

from app.embedding_models import Collection, Document

EMBEDDING_MODELS = "multi-qa-mpnet-base-dot-v1"


class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODELS)

    def _embed_collection(self, collection: Collection) -> List[np.ndarray]:
        embeddings = cast(
            List[np.ndarray],
            self.model.encode(
                [doc.text for doc in collection.documents], convert_to_numpy=True
            ),
        )
        return embeddings

    def embed(self, collection: Collection) -> Collection:
        embeddings = self._embed_collection(collection)
        doc: Document
        emb: np.ndarray
        for doc, emb in zip(collection.documents, embeddings):
            doc.embedding = emb
        return collection
