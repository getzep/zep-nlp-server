# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep

from typing import List, Optional

from pydantic import BaseModel


class RecordDataRequest(BaseModel):
    text: str
    language: str = "en"


class RecordRequest(BaseModel):
    recordId: str
    data: RecordDataRequest


class RecordsRequest(BaseModel):
    values: List[RecordRequest]


class RecordDataResponse(BaseModel):
    entities: List


class Message(BaseModel):
    message: str


class RecordResponse(BaseModel):
    recordId: str
    data: RecordDataResponse
    errors: Optional[List[Message]]
    warnings: Optional[List[Message]]


class RecordsResponse(BaseModel):
    values: List[RecordResponse]
