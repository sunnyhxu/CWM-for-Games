import io
import unittest
from typing import Any

# NOTE: The synthesized code is injected before this runs.

class TestKuhnTransitions(unittest.TestCase):
    def test_initial_deal(self):
        state = {
            'deck': ['Q'],
            'hands': ['J', 'K'],
            'pot': [1.0, 1.0],
            'history': [],
            'current_player': 0,
            'is_terminal': False
        }
        
        self.assertEqual(get_current_player(state), 0)
        legal = set(get_legal_actions(state))
        expected = {'check', 'bet'}
        self.assertSetEqual(legal, expected)

    def test_observation_hiding(self):
        """
        CRITICAL: Ensures players cannot see each other's cards.
        """
        state = {
            'deck': ['Q'],
            'hands': ['J', 'K'],
            'pot': [1.0, 1.0],
            'history': ['check'],
            'current_player': 1,
            'is_terminal': False
        }
        
        obs_list = get_observations(state)
        self.assertEqual(len(obs_list), 2, "Must return observations for both players")
        
        obs_p0 = obs_list[0]
        self.assertEqual(obs_p0['private_card'], 'J', "P0 should see their own card J")
        self.assertNotIn('K', str(obs_p0), "P0 observation should NOT contain opponent card K")
        self.assertEqual(obs_p0['history'], ['check'])

        obs_p1 = obs_list[1]
        self.assertEqual(obs_p1['private_card'], 'K', "P1 should see their own card K")
        self.assertNotIn('J', str(obs_p1), "P1 observation should NOT contain opponent card J")
        self.assertEqual(obs_p1['history'], ['check'])

    def test_showdown_p1_wins(self):
        state = {
            'deck': ['Q'],
            'hands': ['J', 'K'],
            'pot': [1.0, 1.0],
            'history': ['check'],
            'current_player': 1,
            'is_terminal': False
        }
        
        next_state = apply_action(state, 'check')
        self.assertEqual(get_current_player(next_state), -4)
        rewards = get_rewards(next_state)
        self.assertEqual(rewards, [-1.0, 1.0], f"P1(K) vs P0(J) check-check should result in [-1, 1], got {rewards}")

    def test_fold_logic(self):
        state = {
            'deck': ['K'],
            'hands': ['Q', 'J'],
            'pot': [2.0, 1.0],
            'history': ['bet'],
            'current_player': 1,
            'is_terminal': False
        }
        
        next_state = apply_action(state, 'fold')
        
        self.assertEqual(get_current_player(next_state), -4)
        
        self.assertEqual(get_rewards(next_state), [1.0, -1.0])

    def test_resample_history_consistency(self):
        """
        Verifies that resampled histories are consistent with observations.
        This implements the "Round-Trip" consistency check described in the paper.
        """
        p0_obs = {
            'private_card': 'J',
            'history': ['check'],
            'current_player': 1
        }
        
        resampled_actions = resample_history([p0_obs], 0)
        
        sim_state = {
            'deck': ['J', 'Q', 'K'], 
            'hands': [None, None], 
            'pot': [1.0, 1.0],
            'history': [],
            'current_player': -1,
            'is_terminal': False
        }
        
        try:
            for action in resampled_actions:
                sim_state = apply_action(sim_state, action)
        except Exception as e:
            self.fail(f"Resampled history was invalid and crashed execution: {e}")

        sim_public_history = [a for a in sim_state['history'] if not a.startswith('deal')]
        
        self.assertEqual(sim_public_history, p0_obs['history'], 
                         f"Public history mismatch. Sim: {sim_public_history}, Obs: {p0_obs['history']}")
        
        p0_card_in_sim = sim_state['hands'][0]
        self.assertEqual(p0_card_in_sim, 'J', 
                         f"Consistency violation: Observation said 'J', but sampled history dealt '{p0_card_in_sim}'.")
        
        p1_card_in_sim = sim_state['hands'][1]
        self.assertIn(p1_card_in_sim, ['Q', 'K'], 
                      "Sampled history assigned an invalid card to the opponent.")
        self.assertNotEqual(p1_card_in_sim, 'J', 
                            "Impossible state: Sampled history dealt 'J' to both players.")

suite = unittest.TestLoader().loadTestsFromTestCase(TestKuhnTransitions)
stream = io.StringIO()
runner = unittest.TextTestRunner(stream=stream, verbosity=2)
result = runner.run(suite)

if not result.wasSuccessful():
    error_message = stream.getvalue()
    raise Exception(f"Unit tests failed:\n{error_message}")