# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep

from typing import List

from pydantic import BaseModel


class RequestRecord(BaseModel):
    uuid: str
    text: str
    language: str = "en"


class Request(BaseModel):
    texts: List[RequestRecord]


class Match(BaseModel):
    end: int
    start: int
    text: str


class Entity(BaseModel):
    label: str
    matches: List[Match]
    name: str


class ResponseRecord(BaseModel):
    uuid: str
    entities: List[Entity]


class Response(BaseModel):
    texts: List[ResponseRecord]
