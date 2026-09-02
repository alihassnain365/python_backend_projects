from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
engine = create_engine("sqlite:///blog.db")
sessionLocal = sessionmaker(bind=engine)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
