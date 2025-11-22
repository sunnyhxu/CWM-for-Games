import os
import re
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, model="gpt-4o"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str = "Generate the code.") -> str:
        """Sends request to OpenAI, logs the interaction, and extracts code."""
        
        logging.info(f"\n{'='*40}\n SENDING PROMPT TO LLM\n{'='*40}")
        logging.info(f"--- System Prompt ---\n{system_prompt}") 
        logging.info(f"--- User Prompt ---\n{user_prompt}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            content = response.choices[0].message.content
            
            logging.info(f"\n{'='*40}\n RECEIVED RESPONSE FROM LLM\n{'='*40}")
            logging.info(content)
            
            return self._extract_code(content)

        except Exception as e:
            logging.error(f"LLM API Error: {e}")
            return ""

    def _extract_code(self, text: str) -> str:
        """Extracts python code from markdown fences."""
        pattern = r"```python(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()