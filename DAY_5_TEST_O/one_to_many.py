from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase):
    """Models ORM"""
    pass

class Author(Base):
    """Models the Author Table"""
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] 
    books: Mapped[list["Book"]] = relationship(back_populates='author')

class Book(Base):
    """Models the Books Table"""
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    author_id : Mapped[int] = mapped_column(ForeignKey('authors.id'))
    author : Mapped["Author"] = relationship(back_populates='books')

    def __repr__(self):
        return f"Book({self.id},{self.name})"
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    auth = Author(name= 'Ali')
    book = Book(name="What's you'r dream")
    book2 = Book(name = 'Reality of Frinedship')
    book.author = auth
    book2.author = auth
    session.add(auth)
    print(auth.books)
    print(book.author_id)
    session.commit()
    print(auth.books)
    print(book.author_id)
