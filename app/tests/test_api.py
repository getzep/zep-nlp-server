# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep

from starlette.testclient import TestClient

from app.api import app
from app.entity_models import Entity, Match, Response


def test_api_ner():
    client = TestClient(app)

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
        {
            "label": "ORG",
            "matches": [{"end": 10, "start": 4, "text": "Google"}],
            "name": "Google",
        },
        {
            "label": "ORG",
            "matches": [{"end": 93, "start": 88, "text": "Apple"}],
            "name": "Apple",
        },
        {
            "label": "PERSON",
            "matches": [{"end": 100, "start": 96, "text": "Siri"}],
            "name": "Siri",
        },
        {
            "label": "ORG",
            "matches": [{"end": 122, "start": 115, "text": "iPhones"}],
            "name": "iPhones",
        },
        {
            "label": "ORG",
            "matches": [{"end": 134, "start": 128, "text": "Amazon"}],
            "name": "Amazon",
        },
        {
            "label": "ORG",
            "matches": [{"end": 142, "start": 137, "text": "Alexa"}],
            "name": "Alexa",
        },
        {
            "label": "LOC",
            "matches": [{"end": 179, "start": 175, "text": "Echo"}],
            "name": "Echo",
        },
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
            label="DATE", matches=[Match(end=75, start=70, text="daily")], name="Daily"
        ),
        Entity(
            label="ORG",
            matches=[Match(end=108, start=85, text="Samsung Electronics Co.")],
            name="Samsung Electronics Co.",
        ),
        Entity(
            label="ORG",
            matches=[Match(end=126, start=113, text="SK Hynix Inc.")],
            name="SK Hynix Inc.",
        ),
        Entity(
            label="GPE",
            matches=[
                Match(end=196, start=191, text="China"),
                Match(end=377, start=372, text="China"),
            ],
            name="China",
        ),
        Entity(
            label="GPE",
            matches=[
                Match(end=210, start=208, text="US"),
                Match(end=367, start=365, text="US"),
            ],
            name="US",
        ),
        Entity(
            label="ORG",
            matches=[Match(end=244, start=217, text="Micron Technology \n    Inc.")],
            name="Micron Technology \n    Inc.",
        ),
        Entity(
            label="PERSON",
            matches=[Match(end=384, start=379, text="Biden")],
            name="Biden",
        ),
        Entity(
            label="DATE",
            matches=[Match(end=399, start=393, text="Sunday")],
            name="Sunday",
        ),
        Entity(
            label="CARDINAL",
            matches=[Match(end=427, start=422, text="Seven")],
            name="Seven",
        ),
        Entity(
            label="GPE", matches=[Match(end=443, start=438, text="Japan")], name="Japan"
        ),
        Entity(
            label="NORP",
            matches=[Match(end=535, start=528, text="Chinese")],
            name="Chinese",
        ),
        Entity(
            label="PERSON",
            matches=[Match(end=563, start=553, text="Li Shangfu")],
            name="Li Shangfu",
        ),
    ]
