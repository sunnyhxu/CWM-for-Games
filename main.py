import os
import logging
from datetime import datetime
from synthesizer import CWMSynthesizer
from executor import Executor

def load_file(filepath):
    with open(filepath, "r") as f:
        return f.read()

def save_file(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)

def setup_logging():
    """Sets up a timestamped log file for this specific run."""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/run_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    print(f"Logging enabled. Check file: {log_filename}")

def run_pipeline(game_name, info_type="perfect"):
    setup_logging()
    
    rules_path = f"data/{game_name}_rules.txt"
    tests_path = f"data/{game_name}_tests.py"
    output_path = f"results/generated_{game_name}.py"

    logging.info(f"Loading data for {game_name}...")
    rules = load_file(rules_path)
    tests = load_file(tests_path)

    synthesizer = CWMSynthesizer()
    executor = Executor()

    # 1. Run Synthesis Pipeline
    cwm_code = synthesizer.synthesize(
        game_name=game_name,
        rules=rules,
        tests=tests,
        info_type=info_type
    )

    if not cwm_code:
        logging.error("Pipeline failed to generate valid code.")
        return

    # 2. Save the valid code
    logging.info(f"Saving verified CWM to {output_path}...")
    save_file(output_path, cwm_code)

    logging.info("--- Pipeline Complete ---")

if __name__ == "__main__":
    game_to_run = "kuhn_poker"  # Options: "breakthrough", "isolation", "kuhn_poker", "tic_tac_toe"
    info_type = "imperfect"  # Set to "imperfect" for imperfect-information games
    run_pipeline(game_to_run, info_type)