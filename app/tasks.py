import os
import time
from celery import Celery

# Read the Redis URL from environment variables
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
def process_heavy_job(job_name: str):
    """Simulates a long background task like video processing or sending emails."""
    time.sleep(5)  # Simulate 5 seconds of work
    return f"Job '{job_name}' completed successfully!"