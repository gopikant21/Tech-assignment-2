import math
from ..models.entities import Location


class DistanceCalculator:
    """
    Utility class for calculating distances between geographical locations.
    Uses Haversine formula to calculate the great-circle distance.
    """

    @staticmethod
    def calculate_distance(location1: Location, location2: Location) -> float:
        """
        Calculate distance between two locations using Haversine formula.

        Args:
            location1: First location with lat/lng
            location2: Second location with lat/lng

        Returns:
            Distance in kilometers
        """
        # Convert latitude and longitude from degrees to radians
        lat1, lon1 = math.radians(location1.lat), math.radians(location1.lng)
        lat2, lon2 = math.radians(location2.lat), math.radians(location2.lng)

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.asin(math.sqrt(a))

        # Radius of Earth in kilometers
        r = 6371

        return c * r
