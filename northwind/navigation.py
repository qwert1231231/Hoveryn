"""
Navigation module for Northwind drone library.
Handles destination setting, route calculation, and position updates.
"""

class Navigation:
    def __init__(self):
        self.destination = None
        self.current_position = (0.0, 0.0)  # (lat, lon)
        self.route = []

    def set_destination(self, lat, lon):
        """
        Set the destination coordinates for the drone.

        Args:
            lat (float): Latitude of destination
            lon (float): Longitude of destination
        """
        self.destination = (lat, lon)
        print(f"Destination set to: {lat}, {lon}")

    def calculate_route(self, start, end):
        """
        Calculate a route from start to end coordinates.

        Args:
            start (tuple): (lat, lon) starting position
            end (tuple): (lat, lon) ending position

        Returns:
            list: List of waypoints as (lat, lon) tuples
        """
        # Simple straight-line route for demonstration
        self.route = [start, end]
        print(f"Route calculated: {self.route}")
        return self.route

    def update_position(self):
        """
        Update the current position of the drone.
        This would typically integrate with GPS/IMU sensors.
        """
        # Placeholder: simulate position update
        # In real implementation, this would read from sensors
        self.current_position = (self.current_position[0] + 0.001, self.current_position[1] + 0.001)
        print(f"Position updated to: {self.current_position}")
        return self.current_position


# Convenience functions for direct use
_nav = Navigation()

def set_destination(lat, lon):
    return _nav.set_destination(lat, lon)

def calculate_route(start, end):
    return _nav.calculate_route(start, end)

def update_position():
    return _nav.update_position()