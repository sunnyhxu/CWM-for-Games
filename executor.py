import traceback
import random
from typing import Tuple, Any, Dict

class Executor:
    def run_tests(self, game_code: str, test_code: str) -> Tuple[bool, str]:
        """
        Executes the game code combined with the test code.
        Returns (True, "Passed") or (False, Traceback).
        """
        full_script = f"{game_code}\n\n{test_code}"
        
        execution_scope: Dict[str, Any] = {}
        
        try:
            exec(full_script, execution_scope)
            return True, "All tests passed."
        except Exception:
            return False, traceback.format_exc()
