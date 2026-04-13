#!/usr/bin/env python3
"""
Demo script for Hoveryn Drone Library
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import Hoveryn

def main():
    print("Hoveryn Drone Library Demo")
    print("=" * 30)

    # Navigation demo
    print("\n1. Navigation:")
    Hoveryn.set_target_coordinate(37.7749, -122.4194)  # San Francisco
    route = Hoveryn.plan_flight_path((0.0, 0.0), (37.7749, -122.4194))
    position = Hoveryn.refresh_position()

    # Obstacle handling demo
    print("\n2. Obstacle Handling:")
    obstacle_detected = Hoveryn.scan_for_obstacle({'distance': 5.0})
    if obstacle_detected:
        Hoveryn.execute_avoidance('left')
        Hoveryn.reroute_path()

    # Stability demo
    print("\n3. Stability:")
    Hoveryn.correct_gps_drift((0.001, -0.002))
    Hoveryn.adjust_altitude({'speed': 20, 'direction': 'N'})
    Hoveryn.engage_hover_hold()

    # Mission control demo
    print("\n4. Mission Control:")
    Hoveryn.start_mission()
    Hoveryn.pause_mission()
    Hoveryn.return_home()

    # Short mission API demo
    print("\n7. Short mission API:")
    drone = Hoveryn.Drone()
    drone.fly([(0.0, 0.0), (37.7749, -122.4194)])
    drone.home()

    # Decision logic demo
    print("\n5. Decision Logic:")
    action = Hoveryn.choose_action('obstacle_detected')
    next_move = Hoveryn.predict_next_move()

    # Data logging demo
    print("\n6. Data Logging:")
    Hoveryn.log_flight_data()
    Hoveryn.export_data()
    Hoveryn.send_to_cloud()

    print("\nDemo completed!")

if __name__ == "__main__":
    main()