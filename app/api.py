# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep

import os

import spacy
import srsly  # type: ignore
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.responses import ORJSONResponse
from starlette.responses import PlainTextResponse, RedirectResponse

from app.embedder import Embedder
from app.embedding_models import Collection
from app.entity_extractor import SpacyExtractor
from app.entity_models import Request, Response

ENABLE_EMBEDDINGS = os.getenv("ENABLE_EMBEDDINGS", "false").lower() == "true"

app = FastAPI(
    title="zep-nlp-server",
    version="0.2",
    description="Zep NLP Server",
)

example_request = srsly.read_json("app/data/example_request.json")

nlp = spacy.load("en_core_web_sm")
extractor = SpacyExtractor(nlp)

if ENABLE_EMBEDDINGS:
    embedder = Embedder()


@app.get("/healthz", response_model=str, status_code=status.HTTP_200_OK)
def health():
    return PlainTextResponse(".")


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("/docs")


@app.post("/entities", response_model=Response)
async def extract_entities(body: Request = Body(..., example=example_request)):
    """Extract Named Entities from a batch of Records."""

    return extractor.extract_entities(body.texts)


@app.post("/embeddings", response_class=ORJSONResponse)
async def embed_collection(collection: Collection):
    """Embed a Collection of Documents."""
    if ENABLE_EMBEDDINGS:
        return ORJSONResponse(embedder.embed(collection))
    else:
        raise HTTPException(status_code=400, detail="Embeddings not enabled.")
