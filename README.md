# TrackLog - Run Logger

TrackLog is a command-line tool written in Python that can be used to log outdoor sport activities, primarily running, cycling and hiking. It is currently under construction. It is designed to scale from CLI to web API.

## MVP Features

- GPX import: single files or directories
- Statistics: weekly/monthly/YTD totals, averages
- SQLite: Local-first, will migrate to PostgreSQL
- Extensible: activity types, multi-user, REST API ready

## Built With

- uv - Lightning-fast package & project management
- Click - Robust CLI framework
- SQLAlchemy - ORM with PostgreSQL migration path
- gpxpy - GPX parsing & analysis
- Rich - Beautiful terminal output
- Pydantic - Data validation & serialization
