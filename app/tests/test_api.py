# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# Heavy modified by Zep

from starlette.testclient import TestClient

from app.api import app


def test_api_ner():
    client = TestClient(app)

    text = """But Google is starting from behind. The company made a late push
    into hardware, and Apple's Siri, available on iPhones, and Amazon's Alexa
    software, which runs on its Echo and Dot devices, have clear leads in
    consumer adoption."""

    request_data = {
        "values": [{"recordId": "a1", "data": {"text": text, "language": "en"}}]
    }

    response = client.post("/entities", json=request_data)
    assert response.status_code == 200

    first_record = response.json()["values"][0]
    assert first_record["recordId"] == "a1"
    assert first_record["errors"] is None
    assert first_record["warnings"] is None

    assert first_record["data"]["entities"] == [
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
