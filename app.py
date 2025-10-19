from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "defaultsecret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_MINUTES = 15

app = FastAPI(title="Marketplace API")

# Dummy user (in-memory)
user_db = {
    "email": "demo@example.com",
    "password": "12345",
    "name": "Demo User"
}

# Dummy items
items = [
    {"id": 1, "name": "Laptop", "price": 12000000},
    {"id": 2, "name": "Headset", "price": 250000}
]

# Security scheme
security = HTTPBearer()

# ---------------- JWT Utility Functions ----------------
def create_jwt_token(email: str):
    payload = {
        "sub": email,
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRY_MINUTES)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ---------------- Routes ----------------

@app.post("/auth/login")
def login(payload: dict):
    email = payload.get("email")
    password = payload.get("password")

    if email == user_db["email"] and password == user_db["password"]:
        token = create_jwt_token(email)
        return {"access_token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/items")
def get_items():
    return {"items": items}

@app.put("/profile")
def update_profile(payload: dict, user=Depends(verify_jwt_token)):
    name = payload.get("name")
    email = payload.get("email")

    # Simulasi update profil
    if user_db["email"] != user["email"]:
        raise HTTPException(status_code=404, detail="User not found")

    if name:
        user_db["name"] = name
    if email:
        user_db["email"] = email

    return {
        "message": "Profile updated",
        "profile": {"name": user_db["name"], "email": user_db["email"]}
    }

# (Opsional) Refresh Token
@app.post("/auth/refresh")
def refresh_token(user=Depends(verify_jwt_token)):
    new_token = create_jwt_token(user["email"])
    return {"access_token": new_token}
