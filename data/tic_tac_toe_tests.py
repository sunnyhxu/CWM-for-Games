import io
import unittest
from typing import Any

# NOTE: The synthesized code is injected before this runs.

class TestTransition(unittest.TestCase):
    def test_transition_basic(self):
        # Initial State
        state = {
            'board': [None, None, None, None, 'x', None, 'o', None, None], 
            'current_player_mark': 'x'
        }
        
        # 1. Check current player
        curr = get_current_player(state)
        self.assertEqual(curr, 0, f"Expected current player 0, got {curr}") 
        
        # 2. Check rewards (game not over)
        rewards = get_rewards(state)
        self.assertEqual(rewards, [0.0, 0.0], f"Expected rewards [0.0, 0.0], got {rewards}")
        
        # 3. Check observations
        obs = get_observations(state)
        self.assertEqual(len(obs), 2, f"get_observations returned {len(obs)} items, expected 2 (one for each player).")
        self.assertEqual(obs[0], state, "Observation 0 does not match state")
        
        # 4. Check legal actions
        legal_actions = set(get_legal_actions(state))
        expected_actions = set([
            'x(0,0)', 'x(0,1)', 'x(0,2)', 
            'x(1,0)', 'x(1,2)', 
            'x(2,1)', 'x(2,2)'
        ])
        self.assertSetEqual(legal_actions, expected_actions, f"Legal actions mismatch. Expected {expected_actions}, got {legal_actions}")
        
        # 5. Apply Action
        next_state = apply_action(state, 'x(1,0)')
        expected_next_board = [None, None, None, 'x', 'x', None, 'o', None, None]
        
        self.assertEqual(next_state['board'], expected_next_board, "Board state update incorrect after move x(1,0)")
        self.assertEqual(next_state['current_player_mark'], 'o', "Player turn did not switch to 'o'")

suite = unittest.TestLoader().loadTestsFromTestCase(TestTransition)
stream = io.StringIO()
runner = unittest.TextTestRunner(stream=stream, verbosity=2)
result = runner.run(suite)

if not result.wasSuccessful():
    error_message = stream.getvalue()
    raise Exception(f"Unit tests failed:\n{error_message}")