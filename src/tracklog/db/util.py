from sqlalchemy import Engine, inspect


def is_db_initialized(engine: Engine):
    return inspect(engine).has_table("workouts")
