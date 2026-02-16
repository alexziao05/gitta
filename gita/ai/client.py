# ai/client.py
# Purpose: Wrapper around LLM provider.
#
# Responsibilities:
#   - Load config
#   - Retrieve API key from keyring
#   - Instantiate client
#   - Send prompt
#   - Return text output

import keyring
from openai import OpenAI

from gita.ai.prompts import COMMIT_PROMPT_TEMPLATE, STYLE_INSTRUCTIONS
from gita.config.settings import Settings
from gita.constants import KEYRING_SERVICE


class AIClient:
    def __init__ (self): 
        settings = Settings()

        self.api_key = keyring.get_password(KEYRING_SERVICE, settings.provider)

        if not self.api_key:
            raise ValueError(f"API key not found. Run 'gita init' to configure your API key.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=settings.base_url
        )

        self.model = settings.model
        self.style = settings.style

    def generate_commit_message(self, diff: str) -> str:
        """
        Generate a commit message from a git diff using the AI client.

        Args:
            diff (str): The git diff representing the staged changes.

        Returns:
            str: The generated commit message.
        """
        style_instructions = STYLE_INSTRUCTIONS.get(self.style, STYLE_INSTRUCTIONS["conventional"])
        prompt = COMMIT_PROMPT_TEMPLATE.format(diff=diff, style_instructions=style_instructions)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        return response.choices[0].message.content.strip()