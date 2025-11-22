CWM_SYSTEM_PROMPT = """
You are an expert python programmer who is building the game of {game_name}.
Here is a description of the game:
{game_desc}

The goal is to implement a python function with the following signature:
# START FUNCTION SIGNATURE
Action = str
State = dict[str, Any]
PlayerObservation = dict[str, Any]

def apply_action(state: State, action: Action) -> State:
    '''Returns the new state after an action has been taken.'''
    pass

def get_current_player(state: State) -> int:
    '''Returns current player, with -1 for chance and -4 for terminal.'''
    pass

def get_player_name(player_id: int) -> str:
    '''Returns the name of the player, with 'chance' for -1, and 'terminal' for -4.'''
    pass

def get_rewards(state: State) -> list[float]:
    '''Returns the rewards per player from their last action.'''
    pass

def get_legal_actions(state: State) -> list[Action]:
    '''Returns legal actions that can be taken in current state.'''
    pass

def get_observations(state: State) -> list[PlayerObservation]:
    '''Returns the observation for player.'''
    pass
# END FUNCTION SIGNATURE

Your code should satisfy the following unit tests.
# START UNIT TESTS
{test_code}
# END UNIT TESTS

Constraints:
1. Do not repeat the unit tests in your output.
2. Only return the functional code.
3. Do not leave placeholders.
4. Include imports (e.g. typing, random, copy).
5. Enclose your code in a markdown block ```python ... ```.
"""

REFINE_PROMPT = """
The previous implementation failed the unit tests.
Here is the error trace:
{error_trace}

The original code was:
{original_code}

Please fix the errors and return the full, corrected code.
"""