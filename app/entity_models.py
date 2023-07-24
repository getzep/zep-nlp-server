# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep

from typing import List

from pydantic import BaseModel


class EntityRequestRecord(BaseModel):
    uuid: str
    text: str
    language: str = "en"


class EntityRequest(BaseModel):
    texts: List[EntityRequestRecord]


class EntityMatch(BaseModel):
    end: int
    start: int
    text: str


class Entity(BaseModel):
    label: str
    matches: List[EntityMatch]
    name: str


class EntityResponseRecord(BaseModel):
    uuid: str
    entities: List[Entity]


class EntityResponse(BaseModel):
    texts: List[EntityResponseRecord]
