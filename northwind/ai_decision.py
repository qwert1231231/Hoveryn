"""
AI Decision Layer module for Northwind drone library.
Implements simple AI for decision making and move prediction.
"""

import random

class AIDecision:
    def __init__(self):
        self.states = ['normal', 'obstacle_detected', 'low_battery', 'high_wind']
        self.actions = ['continue', 'avoid', 'return_home', 'hover', 'land']

    def choose_action(self, state):
        """
        Choose an action based on current state.

        Args:
            state (str): Current drone state

        Returns:
            str: Chosen action
        """
        if state == 'obstacle_detected':
            action = 'avoid'
        elif state == 'low_battery':
            action = 'return_home'
        elif state == 'high_wind':
            action = 'hover'
        else:
            action = 'continue'

        print(f"AI chose action '{action}' for state '{state}'")
        return action

    def predict_next_move(self):
        """
        Predict the next optimal move based on current conditions.

        Returns:
            str: Predicted move/action
        """
        # Simple prediction based on random selection for demonstration
        move = random.choice(self.actions)
        print(f"Predicted next move: {move}")
        return move


# Convenience functions
_ai = AIDecision()

def choose_action(state):
    return _ai.choose_action(state)

def predict_next_move():
    return _ai.predict_next_move()