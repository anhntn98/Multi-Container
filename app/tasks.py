import os
import time
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)


# NEW: Task 1 - Send welcome email after registration
@celery_app.task
def send_welcome_email(email: str, username: str):
    """Simulates sending an onboarding/welcome email asynchronously."""
    time.sleep(4)  # Simulate email provider latency
    print(f"==================================================")
    print(f"📧 [CELERY] Welcome email sent to {username} ({email})!")
    print(f"==================================================")
    return f"Welcome email sent to {email}"

# NEW: Task 2 - Log security audit after login
@celery_app.task
def log_security_event(username: str, action: str):
    """Simulates writing a security audit event in background."""
    time.sleep(1)
    print(f"🔒 [CELERY AUDIT] User '{username}' performed action: {action}")
    return f"Logged audit for {username}"
