"""
Mission control module for Northwind drone library.
Manages mission lifecycle: start, pause, and return home.
"""

class MissionController:
    def __init__(self):
        self.mission_active = False
        self.mission_paused = False
        self.home_position = (0.0, 0.0)  # (lat, lon)

    def start_mission(self):
        """
        Start the drone mission.
        """
        if not self.mission_active:
            self.mission_active = True
            self.mission_paused = False
            print("Mission started")
        else:
            print("Mission already active")

    def pause_mission(self):
        """
        Pause the current mission.
        """
        if self.mission_active and not self.mission_paused:
            self.mission_paused = True
            print("Mission paused")
        else:
            print("Mission not active or already paused")

    def return_home(self):
        """
        Return drone to home position.
        """
        print("Returning to home position")
        # Placeholder: set destination to home and engage navigation
        # Would integrate with navigation.set_destination(self.home_position)


# Convenience functions
_controller = MissionController()

def start_mission():
    return _controller.start_mission()

def pause_mission():
    return _controller.pause_mission()

def return_home():
    return _controller.return_home()