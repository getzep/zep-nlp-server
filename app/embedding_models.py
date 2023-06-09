from typing import List, Optional

from pydantic.dataclasses import dataclass
from pydantic_numpy import NDArrayFp32  # type: ignore


@dataclass
class Document:
    text: str
    embedding: Optional[NDArrayFp32] = None
    language: str = "en"

    class Config:
        arbitrary_types_allowed = True


@dataclass
class Collection:
    documents: List[Document]
