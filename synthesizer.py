import logging
from llm_client import LLMClient
from executor import Executor
from prompts import (
    CWM_SYSTEM_PROMPT_PERFECT,
    CWM_SYSTEM_PROMPT_IMPERFECT,
    REFINE_PROMPT,
)

class CWMSynthesizer:
    def __init__(self):
        self.llm = LLMClient()
        self.executor = Executor()

    PROMPT_MAP = {
        "perfect": CWM_SYSTEM_PROMPT_PERFECT,
        "imperfect": CWM_SYSTEM_PROMPT_IMPERFECT,
    }

    def synthesize(
        self,
        game_name: str,
        rules: str,
        tests: str,
        info_type: str = "perfect",
        max_retries = 2,
    ) -> str:
        logging.info(f"--- Starting Synthesis for {game_name} ---")
        info_key = info_type.strip().lower()
        if info_key not in self.PROMPT_MAP:
            raise ValueError(
                f"Unsupported info_type '{info_type}'. Expected one of {list(self.PROMPT_MAP.keys())}."
            )
        logging.info(f"Using {info_key} information prompt template.")

        # 1. Initial Zero-Shot Generation
        system_prompt_template = self.PROMPT_MAP[info_key]
        system_prompt = system_prompt_template.format(
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
            logging.debug(f"Error Trace: {result}")

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