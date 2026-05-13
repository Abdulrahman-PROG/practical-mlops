from locust import HttpUser, task, between


class AppUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def index(self):
        self.client.get("/")

    @task(1)
    def add(self):
        self.client.get("/add/3/5")
