from typing import List, Optional

from pydantic.dataclasses import dataclass
from pydantic_numpy import NDArrayFp32


@dataclass
class Document:
    uuid: str
    text: str
    embedding: Optional[List[NDArrayFp32]] = None
    language: str = "en"

    class Config:
        arbitrary_types_allowed = True

@dataclass
class Collection:
    uuid: str
    documents: List[Document]
