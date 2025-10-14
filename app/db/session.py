from sqlmodel import create_engine, Session, SQLModel
from app.core.config import DATABASE_URL

ssl_args = {'ssl': {'ca': 'ca.pem'}}
engine = create_engine(DATABASE_URL, connect_args=ssl_args)

#engine = create_engine(DATABASE_URL, echo=True) ## usar esto cuando no se vaya a usar ssl

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
