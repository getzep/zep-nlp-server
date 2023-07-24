# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep
from functools import lru_cache
from typing import Dict, List

import spacy.tokens.doc
from spacy.language import Language

from app.config import settings
from app.entity_models import (
    Entity,
    EntityMatch,
    EntityRequestRecord,
    EntityResponse,
    EntityResponseRecord,
)

from app.config import log


class SpacyExtractor:
    """class SpacyExtractor encapsulates logic to pipe Records with an id and text body
    through a spacy model and return entities separated by Entity Type
    """

    def __init__(
        self,
        nlp: Language,
    ):
        """Initialize the SpacyExtractor pipeline.

        nlp (spacy.language.Language): pre-loaded spacy language model

        RETURNS (EntityRecognizer): The newly constructed object.
        """
        self.nlp = nlp

    def _name_to_id(self, text: str):
        """Utility function to do a messy normalization of an entity name

        text (str): text to create "id" from
        """
        return "-".join([s.lower() for s in text.split()])

    def extract_entities(self, records: List[EntityRequestRecord]) -> EntityResponse:
        """Apply the pre-trained model to a batch of records

        records (list[RequestRecord]): The list of RequestRecord each with an
            `uuid` and `text` property

        RETURNS (Response): `Response` containing the uuid of
            the correlating document and a list of entities.
        """
        ids = (r.uuid for r in records)
        texts = (r.text for r in records)

        res: List[EntityResponseRecord] = []

        spacy_doc: spacy.tokens.doc.Doc
        for doc_id, spacy_doc in zip(ids, self.nlp.pipe(texts)):
            entities: Dict[int, Entity] = {}
            for ent in spacy_doc.ents:
                ent_id = ent.kb_id
                if not ent_id:
                    ent_id = ent.ent_id
                if not ent_id:
                    ent_id = self._name_to_id(ent.text)

                if ent_id not in entities:
                    if ent.text.lower() == ent.text:
                        ent_name = ent.text.capitalize()
                    else:
                        ent_name = ent.text
                    entities[ent_id] = Entity(
                        name=ent_name, label=ent.label_, matches=[]
                    )
                entities[ent_id].matches.append(
                    EntityMatch(start=ent.start_char, end=ent.end_char, text=ent.text)
                )

            res.append(
                EntityResponseRecord(uuid=doc_id, entities=list(entities.values()))
            )
        return EntityResponse(texts=res)


@lru_cache()
def get_extractor() -> SpacyExtractor:
    log.info(
        f"Loading spacy model {settings.nlp_spacy_model}. If the model is not already"
        " downloaded, this may take a while."
    )
    nlp = spacy.load(settings.nlp_spacy_model)
    log.info(f"Loaded spacy model {settings.nlp_spacy_model}.")

    return SpacyExtractor(nlp)
