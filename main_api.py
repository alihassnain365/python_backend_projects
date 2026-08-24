from fastapi import FastAPI, Depends, HTTPException
from database import sessionLocal
from sqlalchemy.orm import Session
from models import User
from pydantic import BaseModel


app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserCreate(BaseModel):
    name: str

class UserOut(BaseModel):
    id: int
    name: str

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id:int, db: Session = Depends(get_db) )->dict:
    user = db.get(User,user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User Not found')
    else:
        return user

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name = user.name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        'status': "User is successfully created"
    }
