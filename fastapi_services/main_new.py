from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from auth.auth_utils import create_access_token
from auth.schemas import UserCreate

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {}  # Use a real DB for production

@app.post("/signup")
def signup(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = pwd_context.hash(user.password)
    fake_users_db[user.email] = {"password": hashed_pw}
    return {"msg": "Verification email sent 🚀 (mocked)"}
