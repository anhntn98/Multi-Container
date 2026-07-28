import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
import psycopg2
from tasks import send_welcome_email, log_security_event

app = FastAPI(title="Enterprise Microservice Auth API")

# Password Hashing Setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database Connection Helper
def get_db_connection():
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:mysecretpassword@db:5432/enterprisedb")
    return psycopg2.connect(db_url)

# Automatically create 'users' table on startup
@app.on_event("startup")
def setup_database():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database table 'users' initialized successfully.")
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        raise e

# Request Schemas
class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

#Default route for health check
@app.get("/")
def read_root():
    return {"message": "health check OK", "status": "running"}

# 1. REGISTER ENDPOINT
@app.post("/signup", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterSchema):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if user exists
    cur.execute("SELECT id FROM users WHERE username = %s OR email = %s;", (user.username, user.email))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already exists")

    # Hash the password
    hashed_pwd = pwd_context.hash(user.password)

    # Save to PostgreSQL
    cur.execute(
        "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s) RETURNING id;",
        (user.username, user.email, hashed_pwd)
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    # Trigger Celery Task (Async Email)
    send_welcome_email.delay(user.email, user.username)

    return {
        "message": "User registered successfully!",
        "user_id": user_id,
        "notice": "Welcome email is being sent in the background by Celery!"
    }

# 2. LOGIN ENDPOINT
@app.post("/login")
def login_user(credentials: LoginSchema):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT hashed_password FROM users WHERE username = %s;", (credentials.username,))
    record = cur.fetchone()
    cur.close()
    conn.close()

    if not record or not pwd_context.verify(credentials.password, record[0]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Trigger Celery Task (Async Security Audit Log)
    log_security_event.delay(credentials.username, "USER_LOGIN_SUCCESS")

    return {
        "message": f"Welcome back, {credentials.username}!",
        "status": "authenticated"
    }