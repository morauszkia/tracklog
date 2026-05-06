from click import ClickException
from pathlib import Path
from rich.console import Console
from gpxpy.gpx import GPXException
from tracklog.core.gpx_parser import (
    process_path,
    InvalidPathError,
    EmptyGPXError,
)
from tracklog.services.db import record_workouts


def log_workout_from_path(path: str):
    """Log workouts from a GPX file or directory.

    Args:
        path (str): path to file or directory

    Raises:
        ClickException: for user-facing errors (nonexistent of invalid path, parsing error, etc.)
    """
    path = Path(path).resolve()
    if not path.exists():
        raise ClickException(f"File not found: {path}")

    try:
        workouts = process_path(path)
        record_workouts(workouts)

        Console().print(
            f"[green]{len(workouts)} workouts logged successfully[/]"
        )
    except InvalidPathError as e:
        raise ClickException(str(e))
    except GPXException as e:
        raise ClickException(f"GPX parsing error: {str(e)}")
    except EmptyGPXError as e:
        raise ClickException(f"GPX parsing error: {str(e)}")
    except Exception as e:
        raise ClickException(f"Unexpected error: {str(e)}")
