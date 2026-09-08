from fastapi import FastAPI, Depends, HTTPException
from database import sessionLocal
from sqlalchemy.orm import Session
from models import User
from pydantic import BaseModel
import bcrypt
from sqlalchemy import select
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

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

class UserSignUp(BaseModel):
    user_name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


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


@app.post("/user_signup/", response_model=UserOut, status_code=201)
def user_signup(user:UserSignUp, db:Session = Depends(get_db)):
    hp = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(name=user.user_name,hashed_password=hp)
    db.add(new_user)
    db.commit()
    return new_user

@app.post("/login/", response_model=Token)
def user_login(login:UserSignUp, db:Session = Depends(get_db)):
    user = db.execute(select(User).where(User.name == login.user_name)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.hashed_password is None:
        raise HTTPException(status_code=401, detail="Invalid credential")
    if not (bcrypt.checkpw(login.password.encode('utf-8'), user.hashed_password.encode('utf-8'))):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        payload = {"id":user.id,
                   "name":user.name}
        token = jwt.encode(payload,os.getenv("jwt_secret_key"), algorithm="HS256")
        return {"access_token":token, "token_type": "bearer"}
