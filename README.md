# TrackLog - Run Logger

TrackLog is a command-line tool written in Python to log outdoor sport activities, primarily runs, rides and hikes from GPX files. Built with modern Python practices, clean architecture, and designed to be easily scaled from CLI to web API.

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
