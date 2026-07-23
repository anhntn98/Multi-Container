import os
from fastapi import FastAPI
from tasks import celery_app, process_heavy_job

app = FastAPI(title="Enterprise Microservice API")

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "FastAPI Web Service",
        "container_id": os.uname().nodename
    }

@app.post("/trigger-job")
def trigger_job(name: str):
    # Sends the job to Redis/Celery queue without blocking the API response
    task = process_heavy_job.delay(name)
    return {
        "message": "Task submitted to background queue!",
        "task_id": task.id
    }