from sqlmodel import Session, create_engine

from config import config

# engine = create_engine(f"sqlite:///./{config.db_name}", echo=config.db_echo)
engine = create_engine(f"sqlite:///./{config.db_name}", echo=False)


# Currently SQLite does not have an async driver, so unfortunately we can not use SqlAlchemy's async extension
def get_db() -> Generator:
    """create a db session"""
    with Session(engine) as session:
        yield session
