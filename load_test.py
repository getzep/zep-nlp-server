import json
import uuid

from locust import HttpUser, between, task

text = (
    """
    South Korea’s Kospi gained as much as 1%, on track for its sixth 
    daily advance. Samsung Electronics Co. and SK Hynix Inc. were among the biggest 
    contributors to the benchmark after China said their US rival Micron Technology 
    Inc. had failed to pass a cybersecurity review. "I think you’re gonna see that 
    begin to thaw very shortly,” between the US and China, Biden said on Sunday 
    after a Group-of-Seven summit in Japan. He added that his administration was 
    considering whether to lift sanctions on Chinese Defense Minister Li Shangfu.""",
)


class ApiUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def post_entities(self):
        headers = {"Content-Type": "application/json"}
        data = {"texts": [{"uuid": str(uuid.uuid4()), "text": text}]}
        self.client.post("/entities", data=json.dumps(data), headers=headers)

    @task
    def post_embeddings(self):
        headers = {"Content-Type": "application/json"}
        data = {"documents": [{"text": text}]}
        self.client.post("/embeddings", data=json.dumps(data), headers=headers)
