# Northwind Drone Navigation Library

**Version 1.2.2**

A lightweight set of helper modules and experiments for drone-style navigation, obstacle handling, and stability logic. This is not a full autopilot system — it is more of a code sketch for testing ideas and learning.

## Features

### 1. Navigation (Location and route math)
- `set_target_coordinate(lat, lon)` - Save a GPS destination coordinate
- `plan_flight_path(start, end)` - Build a waypoint route from start to end
- `refresh_position()` - Simulate a GPS/IMU position update

### 2. Obstacle Handling (Critical)
- `scan_for_obstacle(sensor_data)` - Check sensor inputs for nearby obstacles
- `execute_avoidance(direction)` - Perform a basic obstacle avoidance maneuver
- `reroute_path()` - Rebuild the route after avoiding an obstacle

### 3. Stability / Correction (Real Drone Behavior)
- `correct_gps_drift(gps_error)` - Correct a GPS drift estimate
- `adjust_altitude(wind_data)` - Adjust altitude based on wind conditions
- `engage_hover_hold()` - Hold position using stabilization control

### 4. Mission Control
- `start_mission()` - Begin a mission sequence
- `pause_mission()` - Pause the current mission
- `return_home()` - Return to home position safely

### 5. Decision Helpers
- `choose_action(state)` - Choose the next action based on current state
- `predict_next_move()` - Predict the next move using simple logic

### 6. Data Logging (For Learning)
- `log_flight_data()` - Log flight telemetry and sensor data
- `export_data()` - Export logged data to JSON files
- `send_to_cloud()` - Upload data to cloud storage for analysis

## Installation

Install the latest release from PyPI:

```bash
pip install --upgrade northwind
```

Install the current repository version from GitHub:

```bash
pip install --upgrade git+https://github.com/qwert1231231/northwind.git
```

Or clone and install locally:

```bash
git clone https://github.com/qwert1231231/northwind.git
cd northwind
pip install -e .
```

## Quick Start

```python
import northwind

# Set destination coordinates
northwind.set_target_coordinate(37.7749, -122.4194)  # San Francisco

# Start autonomous mission
northwind.start_mission()

# Hardware motor control
northwind.configure_motor_profile('esp32')
northwind.set_motor_speed_percent(75)  # percent of full PWM range
northwind.ramp_motor_speed(90, step=10, delay=0.1)
status = northwind.read_motor_status()
print(status)

# Decision helpers
action = northwind.choose_action('normal')
next_move = northwind.predict_next_move()

# Log flight data
northwind.log_flight_data()
northwind.export_data()
```

## Motor Speed Control

Northwind 1.1.2 introduces PWM-based motor speed control for embedded hardware platforms.
Supported device profiles:

- `esp32` — ESP32 PWM driver profile
- `arduino` — Arduino PWM driver profile
- `drone` — Generic drone ESC PWM profile

Use `configure_motor_profile(...)` to choose the device type, then control speed with `set_motor_speed_percent(...)` or `set_motor_pwm(...)`.

## Requirements

- Python 3.8+
- GPS/IMU sensors (for real drone integration)
- Cloud storage account (optional, for data upload)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Repository

- GitHub: [https://github.com/qwert1231231/northwind](https://github.com/qwert1231231/northwind)
- PyPI: [https://pypi.org/project/northwind/](https://pypi.org/project/northwind/)