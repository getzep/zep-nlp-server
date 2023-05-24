# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep

import spacy
import srsly  # type: ignore
from fastapi import Body, FastAPI, status
from starlette.responses import PlainTextResponse, RedirectResponse

from app.entity_models import Request, Response
from app.spacy_extractor import SpacyExtractor

app = FastAPI(
    title="zep-nlp-server",
    version="0.1",
    description="Zep NLP Server",
)

example_request = srsly.read_json("app/data/example_request.json")

nlp = spacy.load("en_core_web_sm")
extractor = SpacyExtractor(nlp)


@app.get("/healthz", response_model=str, status_code=status.HTTP_200_OK)
def health():
    return PlainTextResponse(".")


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("/docs")


@app.post("/entities", response_model=Response, tags=["NER"])
async def extract_entities(body: Request = Body(..., example=example_request)):
    """Extract Named Entities from a batch of Records."""

    return extractor.extract_entities(body.texts)
