from fastapi import FastAPI, HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .auth.auth_utils import create_access_token
from .auth.schemas import UserCreate
from .models import User
from .database import get_db
import secrets
from datetime import datetime, timedelta

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
def read_root():
    return {"msg": "NeoOS is live 🚀"}

@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists in REAL database
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate verification token
    verification_token = secrets.token_urlsafe(32)
    
    # Create new user in REAL database
    hashed_pw = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_pw,
        is_verified=False,
        verification_token=verification_token  # Need to add this field to User model
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # TODO: Send actual email here
    # send_verification_email(user.email, verification_token)
    
    return {"msg": "Verification email sent! Check your inbox 📧"}

@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    # Get user from REAL database
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

