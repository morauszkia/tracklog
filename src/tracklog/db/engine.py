import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from tracklog.db.models import Base

load_dotenv()
db_path = os.environ.get("DB_PATH")

if not db_path:
    raise ValueError("DB_PATH environment variable is required")

engine = create_engine(db_path, echo=True)


def create_tables():
    Base.metadata.create_all(engine)
