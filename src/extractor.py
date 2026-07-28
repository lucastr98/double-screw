from importlib.resources import path

from .llm_client import LLMClient
from pathlib import Path

SYSTEM_PROMPT_PATH = "prompts/system-prompt.txt"

class DataExtractor:
    def __init__(self, client: LLMClient, debug: bool = False):
        self.client = client
        self.debug = debug
    

    def extract(self, data: dict) -> dict:
        """
        Extracts connections between different datasets.
        """
        # 1. Define prompts
        system_prompt = Path(SYSTEM_PROMPT_PATH).read_text(encoding="utf-8").strip()
        
        query = "Analyze the following datasets for duplicates:\n"
        query += f"\n{data}\n"

        # 2. Query LLM
        response = self.client.query(query, system_prompt=system_prompt)

        if self.debug:
            print("[DEBUG] Query:\n", query)
            print("[DEBUG] LLM response:\n", response)
        
        # 3. Process answer
        csv_content = response.strip()
        
        return csv_content
