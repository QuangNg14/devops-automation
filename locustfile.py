import random
import time
from uuid import uuid4
from locust import HttpUser, task, between


question_ids = [ str(uuid4()) for _ in range(100) ]

user_ids = []


class QuickstartUser(HttpUser):
    wait_time = between(0.5, 1.0)

    @task(2)
    def answer_question(self):
        self.client.post("/answers", json={
            "user_id": self.user_id,
            "question_id": question_ids[self.question_idx],
            "score": random.choice(range(1, 8))
        })
    
    @task
    def create_compatibility(self):
        self.client.post("/users/compatibility", json={
            "from_id": self.user_id,
            "to_id": random.choice([ uid for uid in user_ids if uid != self.user_id ])
        })

    def on_start(self):
        global user_ids
        self.user_id = str(uuid4())
        self.question_idx = 0

        user_ids.append(self.user_id)
