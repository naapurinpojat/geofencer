"""
Generic utils needed to run snowdog
"""

# pylint: disable=no-self-argument

import json
from time import sleep
from time import clock_gettime_ns
from math import radians, sin, cos, sqrt, atan2

class Utils:
    """Utils to calculate time and distances"""
    # pylint: disable=no-method-argument

    def millis_to_nanos(millis: int) -> int:
        """convert milliseconds to nanoseconds"""
        return millis * 1000

    def sleep_ms(time_ms: int) -> None:
        """sleep using milliseconds"""
        sleep(Utils.millis_to_seconds(time_ms))

    def get_time() -> int:
        """get system time in nanoseconds (epoch)"""
        return clock_gettime_ns(0)

    def millis_to_seconds(millis: int) -> float:
        """convert milliseconds to seconds"""
        return float(millis) / 1000

    # this conversion losts nanosecond accuracy
    def nanos_to_millis(nanos: int) -> int:
        """convert nanoseconds to milliseconds (int)"""
        return int(nanos / 1000000)

    def nanos_to_seconds(nanos: int) -> float:
        """convert nanoseconds to seconds"""
        return Utils.millis_to_seconds(Utils.nanos_to_millis(nanos))

    def timedelta_seconds(nanos_1: int, nanos_2: int = None) -> int:
        """Calculate timedelta between startpoint and current time (or timestamp 2 if given)"""
        if not nanos_2:
            nanos_2 = Utils.get_time()
        nanos = nanos_2 - nanos_1
        return Utils.nanos_to_seconds(nanos)

    def haversine_distance_meters(point1, point2):
        """
        Calculate the haversine distance between two points in meters.

        Parameters:
        - point1, point2: Tuple of (latitude, longitude) for each point.

        Returns:
        Distance in meters.
        """
        # pylint: disable=invalid-name
        # Radius of the Earth in meters
        earth_radius = 6371000.0

        # Convert latitude and longitude from degrees to radians
        lat1, lon1 = map(radians, point1)
        lat2, lon2 = map(radians, point2)

        # Calculate the differences in coordinates
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Haversine formula
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Distance in meters
        distance = earth_radius * c

        return distance

class Fences:
    """Class to handle geofencing"""
    # pylint: disable=too-few-public-methods
    def __init__(self, filepath):
        fences = None
        self.areas = {}
        with open(filepath, "r", encoding="utf-8") as geojson:
            fences = json.load(geojson)
        for i in fences.get("features"):
            self.areas[i.get("properties").get("name")] = i.get("geometry").get('coordinates')[0]


    def in_area(self, point):
        """
        Check if point (x,y) is in provided area (geojson containing multiple polygons)
        """
        def point_in_polygon(point_x, point_y, polygon):
            """
            Check if a point (x, y) is inside a polygon.

            Parameters:
            - point_x, point_y: Coordinates of the point.
            - polygon: List of tuples representing the vertices of the polygon.

            Returns:
            True if the point is inside the polygon, False otherwise.
            """
            polygon_len = len(polygon)
            inside = False

            # Ray casting algorithm
            for i in range(polygon_len):
                x_1, y_1 = polygon[i]
                x_2, y_2 = polygon[(i + 1) % polygon_len]

                if ((y_1 <= point_y < y_2) or (y_2 <= point_y < y_1)) and \
                (point_x > (x_2 - x_1) * (point_y - y_1) / (y_2 - y_1) + x_1):
                    inside = not inside

            return inside
        for area_key, area_value in self.areas.items():
            if point_in_polygon(point.get('lon'), point.get('lat'), area_value):
                return area_key

        return None
