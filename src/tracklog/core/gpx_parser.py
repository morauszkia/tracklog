import gpxpy


def parse_gpx(file_path):
    with open(file_path, "r") as file:
        gpx = gpxpy.parse(file)

    print(f"Activity type: {gpx.tracks[0].type if gpx.tracks else 'N/A'}")
    print(f"Elevation: {round(gpx.get_uphill_downhill().uphill, 2)}")
