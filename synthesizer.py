import logging
from llm_client import LLMClient
from executor import Executor
from prompts import CWM_SYSTEM_PROMPT, REFINE_PROMPT

class CWMSynthesizer:
    def __init__(self):
        self.llm = LLMClient()
        self.executor = Executor()

    def synthesize(self, game_name: str, rules: str, tests: str, max_retries=2) -> str:
        logging.info(f"--- Starting Synthesis for {game_name} ---")

        # 1. Initial Zero-Shot Generation
        system_prompt = CWM_SYSTEM_PROMPT.format(
            game_name=game_name,
            game_desc=rules,
            test_code=tests
        )
        
        current_code = self.llm.generate(system_prompt)
        
        # 2. Refinement Loop
        for attempt in range(max_retries + 1):
            logging.info(f"Validating Attempt {attempt + 1}...")
            
            success, result = self.executor.run_tests(current_code, tests)
            
            if success:
                logging.info(f"Success! Code passed all tests.")
                return current_code
            
            logging.warning(f"Attempt {attempt + 1} Failed. Error trace captured.")
            logging.debug(f"Error Trace: {result}") # Log full trace to file

            if attempt < max_retries:
                refinement_prompt = REFINE_PROMPT.format(
                    error_trace=result,
                    original_code=current_code
                )
                logging.info("Refining code with LLM...")
                current_code = self.llm.generate(refinement_prompt)
            else:
                logging.error("Max retries reached. Synthesis failed.")
        
        return ""