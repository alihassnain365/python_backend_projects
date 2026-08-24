from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine("sqlite:///blog.db")
sessionLocal = sessionmaker(bind=engine)
