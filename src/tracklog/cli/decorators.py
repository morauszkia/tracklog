from functools import wraps
from sqlalchemy.exc import (
    OperationalError,
    IntegrityError,
    ProgrammingError,
)
from click import ClickException


def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            raise ClickException(
                "Could not connect to database. Check your database settings."
            ) from e
        except ProgrammingError as e:
            raise ClickException(
                "Could not connect to table. Run 'tracklog init-db' to ensure schema exists and is valid."
            ) from e
        except IntegrityError as e:
            raise ClickException(
                "Database constraint violated. Data may already exist or be invalid."
            ) from e

    return wrapper
