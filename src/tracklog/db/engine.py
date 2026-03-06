import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()
db_path = os.environ.get("DB_PATH")

if not db_path:
    raise ValueError("DB_PATH environment variable is required")

engine = create_engine(db_path, echo=True)


class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
