# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep

from starlette.testclient import TestClient

from app.api import app
from app.embedding_models import Collection, Document
from app.entity_models import Entity, Match, Response

text1 = """But Google is starting from behind. The company made a late push
into hardware, and Apple's Siri, available on iPhones, and Amazon's Alexa
software, which runs on its Echo and Dot devices, have clear leads in
consumer adoption."""
text2 = """South Korea’s Kospi gained as much as 1%, on track for its sixth 
daily advance. Samsung Electronics Co. and SK Hynix Inc. were among the biggest 
contributors to the benchmark after China said their US rival Micron Technology 
Inc. had failed to pass a cybersecurity review. "I think you’re gonna see that 
begin to thaw very shortly,” between the US and China, Biden said on Sunday 
after a Group-of-Seven summit in Japan. He added that his administration was 
considering whether to lift sanctions on Chinese Defense Minister Li Shangfu."""


def test_api_ner():
    client = TestClient(app)

    request_data = {
        "texts": [
            {
                "uuid": "87c397dc-aabd-483f-8811-0ad9ef01248e",
                "text": text1,
                "language": "en",
            },
            {
                "uuid": "52x23423-sdfd-2344-adfs-234sdvsdfsds",
                "text": text2,
                "language": "en",
            },
        ]
    }

    response = client.post("/entities", json=request_data)
    assert response.status_code == 200

    r = Response.parse_obj(response.json())
    assert len(r.texts) == 2

    assert r.texts[0].uuid == request_data["texts"][0]["uuid"]
    assert r.texts[1].uuid == request_data["texts"][1]["uuid"]

    assert r.texts[0].entities == [
        Entity(
            label="ORG",
            matches=[Match(end=10, start=4, text="Google")],
            name="Google",
        ),
        Entity(
            label="ORG",
            matches=[Match(end=89, start=84, text="Apple")],
            name="Apple",
        ),
        Entity(
            label="PERSON",
            matches=[Match(end=96, start=92, text="Siri")],
            name="Siri",
        ),
        Entity(
            label="ORG",
            matches=[Match(end=118, start=111, text="iPhones")],
            name="iPhones",
        ),
        Entity(
            label="ORG",
            matches=[Match(end=130, start=124, text="Amazon")],
            name="Amazon",
        ),
        Entity(
            label="ORG",
            matches=[Match(end=138, start=133, text="Alexa")],
            name="Alexa",
        ),
        Entity(
            label="LOC",
            matches=[Match(end=171, start=167, text="Echo")],
            name="Echo",
        ),
    ]

    assert r.texts[1].entities == [
        Entity(
            label="GPE",
            matches=[Match(end=13, start=0, text="South Korea’s")],
            name="South Korea’s",
        ),
        Entity(
            label="PERCENT",
            matches=[Match(end=40, start=27, text="as much as 1%")],
            name="As much as 1%",
        ),
        Entity(
            label="ORDINAL",
            matches=[Match(end=64, start=59, text="sixth")],
            name="Sixth",
        ),
        Entity(
            label="DATE", matches=[Match(end=71, start=66, text="daily")], name="Daily"
        ),
        Entity(
            label="ORG",
            matches=[Match(end=104, start=81, text="Samsung Electronics Co.")],
            name="Samsung Electronics Co.",
        ),
        Entity(
            label="ORG",
            matches=[Match(end=122, start=109, text="SK Hynix Inc.")],
            name="SK Hynix Inc.",
        ),
        Entity(
            label="GPE",
            matches=[
                Match(end=188, start=183, text="China"),
                Match(end=361, start=356, text="China"),
            ],
            name="China",
        ),
        Entity(
            label="GPE",
            matches=[
                Match(end=202, start=200, text="US"),
                Match(end=351, start=349, text="US"),
            ],
            name="US",
        ),
        Entity(
            label="ORG",
            matches=[Match(end=232, start=209, text="Micron Technology \nInc.")],
            name="Micron Technology \nInc.",
        ),
        Entity(
            label="PERSON",
            matches=[Match(end=368, start=363, text="Biden")],
            name="Biden",
        ),
        Entity(
            label="DATE",
            matches=[Match(end=383, start=377, text="Sunday")],
            name="Sunday",
        ),
        Entity(
            label="CARDINAL",
            matches=[Match(end=407, start=402, text="Seven")],
            name="Seven",
        ),
        Entity(
            label="GPE", matches=[Match(end=423, start=418, text="Japan")], name="Japan"
        ),
        Entity(
            label="NORP",
            matches=[Match(end=511, start=504, text="Chinese")],
            name="Chinese",
        ),
        Entity(
            label="PERSON",
            matches=[Match(end=539, start=529, text="Li Shangfu")],
            name="Li Shangfu",
        ),
    ]


def test_embedding():
    client = TestClient(app)

    request_data = {
        "uuid": "87c397dc-aabd-483f-8811-0ad9ef01248e",
        "documents": [
            {
                "uuid": "87c397dc-aabd-483f-8811-0ad9ef01248e",
                "text": text1,
                "language": "en",
            },
            {
                "uuid": "52x23423-sdfd-2344-adfs-234sdvsdfsds",
                "text": text2,
                "language": "en",
            },
        ],
    }

    response = client.post("/embeddings", json=request_data)
    assert response.status_code == 200

    r = Collection(**response.json())
    assert len(r.documents) == 2
    d: Document
    for d in r.documents:
        assert d.embedding is not None
        assert d.embedding.shape[0] == 768
        assert d.text is not None
