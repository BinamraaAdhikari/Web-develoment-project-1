from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hash):
    return pwd_context.verify(password, hash)

def create_token(user_id: int):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
