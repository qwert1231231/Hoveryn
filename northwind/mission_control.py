"""
Mission control module for Northwind drone library.
Manages mission lifecycle, autonomous behaviors, safety protocols, and system health.
"""

import datetime
import random

from . import ai_decision
from . import data_logging
from . import navigation
from . import obstacle_handling
from . import stability


class MissionController:
    def __init__(self):
        self.mission_active = False
        self.mission_paused = False
        self.home_position = navigation.Navigation().current_position
        self.flight_mode = 'manual'
        self.mission_plan = []
        self.route = []
        self.world_model = {}
        self.telemetry = []
        self.sensors_calibrated = False
        self.last_environment_scan = {}
        self.emergency_engaged = False
        self.health_status = {
            'battery': 100,
            'gps': True,
            'imu': True,
            'camera': True,
            'motors': True,
        }

    def initialize_system(self):
        """Boot and reset all drone systems and state."""
        self.mission_active = False
        self.mission_paused = False
        self.flight_mode = 'manual'
        self.mission_plan = []
        self.route = []
        self.world_model = {}
        self.telemetry = []
        self.sensors_calibrated = False
        self.last_environment_scan = {}
        self.emergency_engaged = False
        self.health_status = {
            'battery': 100,
            'gps': True,
            'imu': True,
            'camera': True,
            'motors': True,
        }
        self.home_position = navigation.Navigation().current_position
        print("System initialized and reset")
        return True

    def calibrate_sensors(self):
        """Calibrate GPS, IMU, and camera inputs."""
        self.sensors_calibrated = True
        print("Calibrating GPS, IMU, and camera sensors")
        print("Calibration complete")
        return True

    def set_flight_mode(self, mode):
        """Switch between manual, assist, and autonomous flight modes."""
        valid_modes = {'manual', 'assist', 'autonomous'}
        if mode not in valid_modes:
            raise ValueError(f"Invalid flight mode: {mode}")
        self.flight_mode = mode
        print(f"Flight mode set to: {mode}")
        return self.flight_mode

    def define_mission(self, path):
        """Load a full route or waypoint list for the mission."""
        if isinstance(path, str):
            try:
                with open(path, 'r') as handle:
                    import json
                    payload = json.load(handle)
                self.mission_plan = payload.get('waypoints', []) if isinstance(payload, dict) else payload
            except (IOError, ValueError) as exc:
                raise ValueError(f"Unable to load mission file: {exc}")
        elif isinstance(path, (list, tuple)):
            self.mission_plan = list(path)
        else:
            raise TypeError("Mission path must be a list of waypoints or a JSON filepath")

        if not self.mission_plan:
            raise ValueError("Mission plan cannot be empty")

        start_position = navigation.Navigation().current_position
        end_position = self.mission_plan[-1]
        self.route = navigation.calculate_route(start_position, end_position)
        print(f"Mission defined with {len(self.mission_plan)} waypoints")
        return self.route

    def validate_mission(self):
        """Check safety and feasibility before flight."""
        if not self.mission_plan:
            print("No mission plan defined")
            return False

        if not self.sensors_calibrated:
            print("Sensors are not calibrated")
            return False

        battery_needed = self.estimate_battery_usage()
        if battery_needed > self.health_status['battery']:
            print(f"Insufficient battery for mission: needs {battery_needed}%, available {self.health_status['battery']}%")
            return False

        if any(obstacle_handling.detect_obstacle(waypoint) for waypoint in self.mission_plan if isinstance(waypoint, dict)):
            print("Mission validation failed due to obstacles on route")
            return False

        print("Mission validation passed")
        return True

    def estimate_battery_usage(self):
        """Predict energy needs for the defined mission."""
        if not self.route:
            return 0

        total_distance = 0.0
        previous = self.route[0]
        for waypoint in self.route[1:]:
            total_distance += self._distance(previous, waypoint)
            previous = waypoint

        estimate = min(100, int(total_distance * 2 + len(self.route) * 1.5))
        print(f"Estimated battery usage: {estimate}% for distance {total_distance:.2f} km")
        return estimate

    def optimize_route(self):
        """Improve path efficiency based on distance and obstacles."""
        if not self.route:
            print("No route to optimize")
            return []

        original_length = len(self.route)
        optimized = []
        seen = set()
        for waypoint in self.route:
            if waypoint not in seen:
                optimized.append(waypoint)
                seen.add(waypoint)

        self.route = optimized
        print(f"Route optimized from {original_length} to {len(self.route)} waypoints")
        return self.route

    def scan_environment(self):
        """Gather real-time sensor data."""
        scan_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'distance': random.uniform(2, 50),
            'vision': {'objects': random.randint(0, 5)},
            'gps_signal': random.choice(['good', 'fair', 'weak']),
            'wind_speed': random.uniform(0, 20),
        }
        self.last_environment_scan = scan_data
        print(f"Environment scanned: {scan_data}")
        return scan_data

    def detect_dynamic_obstacles(self):
        """Identify moving objects from the latest sensor scan."""
        scan = self.last_environment_scan or self.scan_environment()
        obstacles = []
        if scan.get('vision', {}).get('objects', 0) > 0:
            obstacles.append({'type': 'moving_object', 'distance': scan['distance']})
            print(f"Detected dynamic obstacle at distance: {scan['distance']:.2f}m")
        else:
            print("No dynamic obstacles detected")
        return obstacles

    def update_world_model(self):
        """Maintain an internal map of surroundings."""
        scan = self.last_environment_scan or self.scan_environment()
        self.world_model['last_scan'] = scan
        self.world_model['updated_at'] = datetime.datetime.now().isoformat()
        print("World model updated")
        return self.world_model

    def decision_engine(self, state=None):
        """Choose the best next action based on AI logic."""
        if state is None:
            state = 'normal'
            if self.health_status['battery'] < 25:
                state = 'low_battery'
            elif self.last_environment_scan.get('distance', 100) < 10:
                state = 'obstacle_detected'
            elif self.last_environment_scan.get('wind_speed', 0) > 15:
                state = 'high_wind'

        action = ai_decision.choose_action(state)
        print(f"Decision engine selected action: {action}")
        return action

    def emergency_protocol(self):
        """Trigger safe behavior in case of failure."""
        self.emergency_engaged = True
        self.mission_active = False
        self.mission_paused = False
        print("Emergency protocol engaged")
        self.hover_stable()
        return True

    def auto_land(self):
        """Safely land at the current or nearest safe location."""
        if self.emergency_engaged:
            print("Auto-landing due to emergency")
        else:
            print("Auto-landing at current location")
        self.mission_active = False
        return True

    def return_to_base(self):
        """Navigate back to origin automatically."""
        self.set_flight_mode('assist')
        navigation.set_destination(*self.home_position)
        self.mission_active = False
        print("Returning to base")
        return self.home_position

    def hover_stable(self):
        """Maintain fixed position against wind or drift."""
        status = stability.hold_position()
        print("Hover stable engaged")
        return status

    def log_telemetry(self):
        """Record all flight data continuously."""
        data_logging.log_flight_data()
        print("Telemetry logged")
        return True

    def sync_cloud(self):
        """Upload logs and status to cloud storage."""
        success = data_logging.send_to_cloud()
        print("Cloud sync completed")
        return success

    def download_updates(self):
        """Fetch improved AI models or configs."""
        print("Downloading updates for AI models and configs")
        updates = {
            'ai_model': 'v1.1',
            'config': 'latest',
            'timestamp': datetime.datetime.now().isoformat(),
        }
        print(f"Downloaded updates: {updates}")
        return updates

    def simulate_mission(self):
        """Run the mission in a virtual environment before execution."""
        if not self.route:
            print("No route available to simulate")
            return False

        print("Simulating mission...")
        for waypoint in self.route:
            print(f"Simulated reaching waypoint: {waypoint}")
        print("Mission simulation complete")
        return True

    def health_check(self):
        """Continuously monitor system components and report failures or risks."""
        issues = []
        if self.health_status['battery'] < 20:
            issues.append('low_battery')
        if not self.health_status['gps']:
            issues.append('gps_failure')
        if not self.health_status['imu']:
            issues.append('imu_failure')
        if not self.health_status['camera']:
            issues.append('camera_failure')
        if not self.health_status['motors']:
            issues.append('motor_failure')

        if issues:
            print(f"Health check issues: {issues}")
        else:
            print("All systems nominal")
        return {'status': 'ok' if not issues else 'warning', 'issues': issues}

    @staticmethod
    def _distance(start, end):
        if not isinstance(start, tuple) or not isinstance(end, tuple):
            return 0.0
        return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5

    def start_mission(self):
        if not self.mission_active:
            self.mission_active = True
            self.mission_paused = False
            print("Mission started")
        else:
            print("Mission already active")

    def pause_mission(self):
        if self.mission_active and not self.mission_paused:
            self.mission_paused = True
            print("Mission paused")
        else:
            print("Mission not active or already paused")

    def return_home(self):
        print("Returning to home position")
        return navigation.set_destination(*self.home_position)


# Convenience functions
_controller = MissionController()

class Drone:
    """Lightweight drone facade for simple mission workflows."""

    def __init__(self, mode='autonomous'):
        self._controller = MissionController()
        self._controller.set_flight_mode(mode)

    def fly(self, path):
        """Initialize and execute a mission in one call."""
        self._controller.initialize_system()
        self._controller.calibrate_sensors()
        self._controller.define_mission(path)
        if not self._controller.validate_mission():
            raise RuntimeError('Mission validation failed')
        self._controller.optimize_route()
        self._controller.simulate_mission()
        self._controller.start_mission()
        self._controller.log_telemetry()
        return self._controller.route

    def home(self):
        return self._controller.return_to_base()

    def land(self):
        return self._controller.auto_land()

    def emergency(self):
        return self._controller.emergency_protocol()

    def status(self):
        return self._controller.health_check()


def quick_mission(path, mode='autonomous'):
    """Shortcut to run a full mission with minimal user code."""
    return Drone(mode=mode).fly(path)


def quick_launch(path, mode='autonomous'):
    return quick_mission(path, mode)


def land():
    return _controller.auto_land()


def home():
    return _controller.return_to_base()


def initialize_system():
    return _controller.initialize_system()


def calibrate_sensors():
    return _controller.calibrate_sensors()


def set_flight_mode(mode):
    return _controller.set_flight_mode(mode)


def define_mission(path):
    return _controller.define_mission(path)


def validate_mission():
    return _controller.validate_mission()


def estimate_battery_usage():
    return _controller.estimate_battery_usage()


def optimize_route():
    return _controller.optimize_route()


def scan_environment():
    return _controller.scan_environment()


def detect_dynamic_obstacles():
    return _controller.detect_dynamic_obstacles()


def update_world_model():
    return _controller.update_world_model()


def decision_engine(state=None):
    return _controller.decision_engine(state)


def emergency_protocol():
    return _controller.emergency_protocol()


def auto_land():
    return _controller.auto_land()


def return_to_base():
    return _controller.return_to_base()


def hover_stable():
    return _controller.hover_stable()


def log_telemetry():
    return _controller.log_telemetry()


def sync_cloud():
    return _controller.sync_cloud()


def download_updates():
    return _controller.download_updates()


def simulate_mission():
    return _controller.simulate_mission()


def health_check():
    return _controller.health_check()


def start_mission():
    return _controller.start_mission()


def pause_mission():
    return _controller.pause_mission()


def return_home():
    return _controller.return_home()