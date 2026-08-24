from database import sessionLocal
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from models import User, Post
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

"""
1. Could add the User, and Post
2. Could get the User, and Posts of the user
"""

app = FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# returning schema of the user (only)
class UserOut(BaseModel):
    """Returning schema of the user"""
    id: int
    name: str

class UserCreate(BaseModel):
    """Creation schema of the user"""
    name: str






@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id:int, db: Session= Depends(get_db)):
    user = db.get(User,user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not exists")
    else:
        return user

@app.post("/users/create")
def create_user(user:UserCreate, db:Session= Depends(get_db)):
    new_user = User(
        name = user.name
    )
    db.add(new_user)
    db.commit()
    return{
        'statur': "User is entered successfully"
    }






