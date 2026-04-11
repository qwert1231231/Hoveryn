#!/usr/bin/env python3
"""
Demo script for Northwind Drone Library
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import northwind

def main():
    print("Northwind Drone Library Demo")
    print("=" * 30)

    # Navigation demo
    print("\n1. Navigation:")
    northwind.set_destination(37.7749, -122.4194)  # San Francisco
    route = northwind.calculate_route((0.0, 0.0), (37.7749, -122.4194))
    position = northwind.update_position()

    # Obstacle handling demo
    print("\n2. Obstacle Handling:")
    obstacle_detected = northwind.detect_obstacle({'distance': 5.0})
    if obstacle_detected:
        northwind.avoid_obstacle('left')
        northwind.recalculate_path()

    # Stability demo
    print("\n3. Stability:")
    northwind.correct_drift((0.001, -0.002))
    northwind.adjust_altitude({'speed': 20, 'direction': 'N'})
    northwind.hold_position()

    # Mission control demo
    print("\n4. Mission Control:")
    northwind.start_mission()
    northwind.pause_mission()
    northwind.return_home()

    # Short mission API demo
    print("\n7. Short mission API:")
    drone = northwind.Drone()
    drone.fly([(0.0, 0.0), (37.7749, -122.4194)])
    drone.home()

    # AI decision demo
    print("\n5. AI Decision:")
    action = northwind.choose_action('obstacle_detected')
    next_move = northwind.predict_next_move()

    # Data logging demo
    print("\n6. Data Logging:")
    northwind.log_flight_data()
    northwind.export_data()
    northwind.send_to_cloud()

    print("\nDemo completed!")

if __name__ == "__main__":
    main()