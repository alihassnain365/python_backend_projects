from database import engine
from models import User, Post, Table,Tag, post_tag
from sqlalchemy.orm import Session

with Session(engine) as session:
    u_ali = User(name = 'Ali')
    session.add(u_ali)
    session.commit()
    p1 = Post(title = 'First post',user_id = u_ali.id)
    p2 = Post(user_id=u_ali.id, title = 'Second post')
    session.add(p1)
    session.add(p2)
    tag1 = Tag(name = 'FYP')
    p1.tags.append(tag1)
    tag2 = Tag(name='Bawag')
    p2.tags.append(tag2)
    session.commit()
    
    for post in u_ali.posts:
        print(post.title, post.tags)