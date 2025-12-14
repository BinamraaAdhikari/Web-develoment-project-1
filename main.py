from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schema, authorize
from models import User, Application

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------- AUTH --------

@app.post("/register")
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed = authorize.hash_password(user.password)
    new_user = User(email=user.email, password_hash=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login")
def login(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not authorize.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = authorize.create_token(db_user.id)
    return {"access_token": token}

# -------- APPLICATIONS --------

@app.post("/applications")
def create_application(app_data: schema.ApplicationCreate, user_id: int, db: Session = Depends(get_db)):
    application = Application(**app_data.dict(), user_id=user_id)
    db.add(application)
    db.commit()
    return {"message": "Application added"}

@app.get("/applications", response_model=list[schema.ApplicationOut])
def list_applications(user_id: int, db: Session = Depends(get_db)):
    return db.query(Application).filter(Application.user_id == user_id).all()
