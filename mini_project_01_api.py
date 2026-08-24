from database import sessionLocal
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from models import User, Post
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

"""
1. Could add the User, and Post
2. Could get the User, and Posts of the user
3. Could create a post
4. Could get a post
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

class PostCreate(BaseModel):
    """Creation schema of the Post"""
    title: str
    user_id: int

class PostOut(BaseModel):
    """Return schema of the post"""
    id: int
    title: str
    user_id: int









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

@app.post("/users/create_post")
def create_post(post:PostCreate, db: Session = Depends(get_db)):
    new_post = Post(
        title = post.title,
        user_id = post.user_id
    )
    db.add(new_post)
    db.commit()
    return {
        'status': "Post is added successfully"
    }

@app.get("/users/get_post/{post_id}", response_model=PostOut)
def get_post(post_id:int, db:Session = Depends(get_db)):
    result_post = db.get(Post,post_id)
    return result_post





