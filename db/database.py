from sqlmodel import create_engine, Session, SQLModel, select

engine = create_engine("sqlite:///sqlite.db")

session = Session(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
