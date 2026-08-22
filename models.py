from database import engine
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """Models ORM"""
    pass

# ---------- User -> Post = One-to-many Relationship

class User(Base):
    """Models the users table"""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    posts: Mapped[list["Post"]] = relationship(back_populates='user')

    def __repr__(self):
        return f"User({self.id}, {self.name})"

# ---------- User -> Post = One-to-many Relationship
# ---------- Post -> Tag = Many-to-Many Relationship

class Post(Base):
    """Models posts table"""
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates='posts')
    tags: Mapped[list["Tag"]] = relationship(secondary="post_tag", back_populates="posts")

    def __repr__(self):
        return f"Post({self.id},{self.title})"


# ---------- Post -> Tag = Many-to-Many Relationship

class Tag(Base):
    """Models the Tags table"""
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    posts: Mapped[list["Post"]] = relationship(secondary="post_tag", back_populates="tags")

    def __repr__(self):
        return f"Tag({self.id}, {self.name})"
    
# ----------- Junction table of Tag - Post

post_tag = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tags_id", ForeignKey("tags.id"), primary_key=True)
)

# ---- Now creating tables from the above defined struture
Base.metadata.create_all(engine)
