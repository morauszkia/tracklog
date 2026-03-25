import pytest
from sqlalchemy import create_engine
from tracklog.db.models import Base
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def session_factory(db_engine):
    return sessionmaker(bind=db_engine)
