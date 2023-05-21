# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep

import spacy
import srsly  # type: ignore
from fastapi import Body, FastAPI
from starlette.responses import RedirectResponse

from app.models import (
    RecordsRequest,
    RecordsResponse,
)
from app.spacy_extractor import SpacyExtractor

app = FastAPI(
    title="zep-nlp-server",
    version="0.1",
    description="Zep NLP Server",
)

example_request = srsly.read_json("app/data/example_request.json")

nlp = spacy.load("en_core_web_sm")
extractor = SpacyExtractor(nlp)


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("/docs")


@app.post("/entities", response_model=RecordsResponse, tags=["NER"])
async def extract_entities(body: RecordsRequest = Body(..., example=example_request)):
    """Extract Named Entities from a batch of Records."""

    documents = []

    for val in body.values:
        documents.append({"id": val.recordId, "text": val.data.text})

    entities_res = extractor.extract_entities(documents)

    res = [
        {"recordId": er["id"], "data": {"entities": er["entities"]}}
        for er in entities_res
    ]

    return {"values": res}
