from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str = "Applied"

class ApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    status: str

    class Config:
        from_attributes = True
