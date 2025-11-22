import io
import unittest
from typing import Any

# NOTE: The synthesized code is injected before this runs.

class TestTransition(unittest.TestCase):
    def test_initial_state(self):
        state = {
            'board': [None] * 13,
            'current_player': 0
        }
        
        curr = get_current_player(state)
        self.assertEqual(curr, 0, f"Initial player should be 0, got {curr}")
        
        legal = set(get_legal_actions(state))
        self.assertEqual(len(legal), 13, f"Expected 13 legal moves initially, got {len(legal)}")
        self.assertIn('0', legal)
        self.assertIn('12', legal)

    def test_adjacency_constraint(self):
        state = {
            'board': [None] * 13,
            'current_player': 1
        }
        state['board'][5] = 0
        
        legal = set(get_legal_actions(state))
        
        self.assertNotIn('5', legal, "Square 5 is occupied, should be illegal")
        self.assertNotIn('4', legal, "Square 4 is adjacent to 5, should be illegal")
        self.assertNotIn('6', legal, "Square 6 is adjacent to 5, should be illegal")
        
        self.assertIn('3', legal, "Square 3 is not adjacent to 5, should be legal")
        self.assertIn('7', legal, "Square 7 is not adjacent to 5, should be legal")

    def test_boundary_constraint(self):
        state = {
            'board': [None] * 13,
            'current_player': 1
        }
        state['board'][0] = 0
        
        legal = set(get_legal_actions(state))
        self.assertNotIn('0', legal)
        self.assertNotIn('1', legal)
        self.assertIn('2', legal)

    def test_apply_move(self):
        state = {
            'board': [None] * 13,
            'current_player': 0
        }
        
        new_state = apply_action(state, '6')
        
        self.assertEqual(new_state['board'][6], 0, "Square 6 should be claimed by Player 0")
        self.assertEqual(new_state['current_player'], 1, "Turn should switch to Player 1")
        
        legal = set(get_legal_actions(new_state))
        self.assertNotIn('5', legal)
        self.assertNotIn('6', legal)
        self.assertNotIn('7', legal)

    def test_win_condition(self):
        board = [None] * 13
        for i in [0, 3, 6, 9, 12]:
            board[i] = 0
            
        state = {
            'board': board,
            'current_player': 1
        }
        
        legal = get_legal_actions(state)
        self.assertEqual(len(legal), 0, f"Expected 0 legal moves in terminal state, got {legal}")
        
        term_check = get_current_player(state)