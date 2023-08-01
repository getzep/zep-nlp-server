from fastapi import Depends, FastAPI, status
from fastapi.responses import ORJSONResponse
from starlette.responses import PlainTextResponse, RedirectResponse

from app.config import settings
from app.embedder import Embedder, get_embedder
from app.embedding_models import Collection
from app.entity_extractor import SpacyExtractor, get_extractor
from app.entity_models import EntityRequest, EntityResponse

app = FastAPI(
    title="zep-nlp-server",
    version="0.3",
    description="Zep NLP Server",
)


@app.on_event("startup")
def startup_event():
    get_embedder()
    get_extractor()


@app.get("/healthz", response_model=str, status_code=status.HTTP_200_OK)
def health():
    return PlainTextResponse(".")


@app.get("/config")
def config():
    """Get the current configuration."""
    return settings.dict()


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("/docs")


@app.post("/entities", response_model=EntityResponse)
def extract_entities(
    entity_request: EntityRequest,
    extractor: SpacyExtractor = Depends(get_extractor),
):
    """Extract Named Entities from a batch of Records."""
    return extractor.extract_entities(entity_request.texts)


@app.post(
    "/embeddings/message",
    description="Retained for legacy v0.8.1 and prior support. Will deprecate soon.",
    response_class=ORJSONResponse,
)
def embed_message_collection_legacy(
    collection: Collection, embedder: Embedder = Depends(get_embedder)
):
    """Embed a Collection of Documents."""
    return ORJSONResponse(
        embedder.embed(collection, settings.embeddings_messages_model)
    )


@app.post("/embeddings/message", response_class=ORJSONResponse)
def embed_message_collection(
    collection: Collection, embedder: Embedder = Depends(get_embedder)
):
    """Embed a Collection of Documents."""
    return ORJSONResponse(
        embedder.embed(collection, settings.embeddings_messages_model)
    )


@app.post("/embeddings/document", response_class=ORJSONResponse)
def embed_document_collection(
    collection: Collection, embedder: Embedder = Depends(get_embedder)
):
    """Embed a Collection of Documents."""
    return ORJSONResponse(
        embedder.embed(collection, settings.embeddings_documents_model)
    )
