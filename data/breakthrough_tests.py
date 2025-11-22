import io
import unittest
from typing import Any

# NOTE: The synthesized code is injected before this runs.

class TestTransition(unittest.TestCase):
    def test_initial_setup(self):
        # Initial State (Standard 5x5 setup)
        # P0 (White/w) at top (rows 0,1), P1 (Black/b) at bottom (rows 3,4)
        state = {
            'board': [
                'w', 'w', 'w', 'w', 'w',  # Row 0
                'w', 'w', 'w', 'w', 'w',  # Row 1
                '.', '.', '.', '.', '.',  # Row 2 (Empty)
                'b', 'b', 'b', 'b', 'b',  # Row 3
                'b', 'b', 'b', 'b', 'b'   # Row 4
            ],
            'current_player': 0
        }

        # Check current player
        curr = get_current_player(state)
        self.assertEqual(curr, 0, f"Initial state should be Player 0's turn, got {curr}")

        # Check legal actions for P0
        # P0 pieces at Row 1 can move to Row 2 (since Row 2 is empty).
        # P0 pieces at Row 0 cannot move (blocked by Row 1).
        # Moves: (1,0)->(2,0), (1,1)->(2,1), etc.
        legal = set(get_legal_actions(state))
        expected_sample = '1,0->2,0'
        self.assertIn(expected_sample, legal, f"Legal actions should include forward moves like {expected_sample}")
        self.assertEqual(len(legal), 5, f"Expected 5 legal moves (one for each piece in Row 1), got {len(legal)}")

    def test_observation_structure(self):
        """
        Specific test to ensure get_observations returns a list of views 
        for ALL players, even in perfect information games.
        """
        state = {
            'board': ['.'] * 25,
            'current_player': 0
        }
        obs = get_observations(state)
        
        # CRITICAL CHECK: Must return list of length 2 (Player 0 view, Player 1 view)
        self.assertEqual(len(obs), 2, f"get_observations must return a list of length 2. Got length {len(obs)}.")
        
        # For perfect info, both views are identical to the state
        self.assertEqual(obs[0], state, "Player 0 observation should match state")
        self.assertEqual(obs[1], state, "Player 1 observation should match state")

    def test_capture_logic(self):
        # Custom State: Setup a capture scenario
        # P0 piece at (2,2). P1 pieces at (3,1), (3,2), (3,3).
        # P0 moving straight to (3,2) is BLOCKED by P1.
        # P0 capturing diagonal to (3,1) or (3,3) is VALID.
        state = {
            'board': [
                '.', '.', '.', '.', '.',
                '.', '.', '.', '.', '.',
                '.', '.', 'w', '.', '.',  # Piece at 2,2
                '.', 'b', 'b', 'b', '.',  # Pieces at 3,1; 3,2; 3,3
                '.', '.', '.', '.', '.'
            ],
            'current_player': 0
        }

        legal = set(get_legal_actions(state))
        
        # Check Blocked
        blocked_move = '2,2->3,2'
        self.assertNotIn(blocked_move, legal, f"Move {blocked_move} should be illegal (cannot move straight into opponent)")

        # Check Captures
        capture_left = '2,2->3,1'
        capture_right = '2,2->3,3'
        self.assertIn(capture_left, legal, f"Move {capture_left} should be legal (diagonal capture)")
        self.assertIn(capture_right, legal, f"Move {capture_right} should be legal (diagonal capture)")

    def test_apply_move(self):
        # Simple move
        state = {
            'board': [
                '.', '.', '.', '.', '.',
                '.', '.', 'w', '.', '.', # 1,2
                '.', '.', '.', '.', '.',
                '.', '.', '.', '.', '.',
                '.', '.', '.', '.', '.'
            ],
            'current_player': 0
        }
        
        action = '1,2->2,2'
        new_state = apply_action(state, action)
        
        # Check Board Update
        self.assertEqual(new_state['board'][7], '.', "Source square (1,2) index 7 should be empty after move")
        self.assertEqual(new_state['board'][12], 'w', "Dest square (2,2) index 12 should contain 'w'")
        
        # Check Player Switch
        self.assertEqual(new_state['current_player'], 1, "Turn should switch to Player 1 after move")

    def test_win_condition(self):
        # P0 is about to win
        state = {
            'board': [
                '.', '.', '.', '.', '.',
                '.', '.', '.', '.', '.',
                '.', '.', '.', '.', '.',
                '.', '.', 'w', '.', '.', # P0 at Row 3
                '.', '.', '.', '.', '.'  # Row 4 (Goal)
            ],
            'current_player': 0
        }
        
        # This move reaches Row 4
        action = '3,2->4,2'
        
        next_state = apply_action(state, action)
        
        # Use get_rewards on the RESULTING state
        rewards = get_rewards(next_state)
        
        # P0 wins, so [1.0, -1.0]
        self.assertEqual(rewards, [1.0, -1.0], f"Move {action} reached back rank. Expected P0 win rewards [1.0, -1.0], got {rewards}")
        
        # Check terminal status
        term = get_current_player(next_state)
        self.assertEqual(term, -4, f"Game should be terminal (-4) after reaching back rank. Got {term}")

# Run the tests
suite = unittest.TestLoader().loadTestsFromTestCase(TestTransition)
stream = io.StringIO()
runner = unittest.TextTestRunner(stream=stream, verbosity=2)
result = runner.run(suite)

if not result.wasSuccessful():
    error_message = stream.getvalue()
    raise Exception(f"Unit tests failed:\n{error_message}")