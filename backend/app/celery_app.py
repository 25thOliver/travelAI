from celery import Celery
import os

celery_app = Celery(
    "travel_tasks",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "travel_queue"}
}