from locust import HttpUser, task, between
import random


class MathUser(HttpUser):
    wait_time = between(0.01, 0.1)

    @task
    def factorial(self):
        n = random.randint(-1, 25)
        self.client.get(f"/factorial?n={n}")

    @task
    def fibonacci(self):
        n = random.randint(-1, 25)
        self.client.get(f"/fibonacci/{n}")

    @task
    def mean(self):
        arr = [random.uniform(-10, 10) for i in range(random.randint(0, 1000))]
        self.client.get("/mean", json=arr, headers={"Content-Type": "application/json"})
