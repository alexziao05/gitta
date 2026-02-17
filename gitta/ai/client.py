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

from gitta.ai.prompts import BRANCH_PROMPT_TEMPLATE, COMMIT_PROMPT_TEMPLATE, PR_PROMPT_TEMPLATE, SCOPED_COMMIT_PROMPT_TEMPLATE, STYLE_INSTRUCTIONS
from gitta.config.settings import Settings
from gitta.constants import KEYRING_SERVICE


class AIClient:
    def __init__ (self): 
        settings = Settings()

        self.api_key = keyring.get_password(KEYRING_SERVICE, settings.provider)

        if not self.api_key:
            raise ValueError(f"API key not found. Run 'gitta init' to configure your API key.")
        
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

    def generate_pr_description(self, branch: str, commits: str, stat: str, diff: str) -> tuple[str, str]:
        """
        Generate a PR title and body from branch commits and diff.

        Args:
            branch: The current branch name.
            commits: The commit log (oneline format).
            stat: The diffstat summary (git diff --stat).
            diff: The full diff vs base branch.

        Returns:
            tuple: (title, body) strings.
        """
        prompt = PR_PROMPT_TEMPLATE.format(
            branch=branch,
            commits=commits,
            stat=stat,
            diff=diff,
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        text = response.choices[0].message.content.strip()

        # Parse TITLE: and BODY: from response
        title = ""
        body = ""
        if "TITLE:" in text and "BODY:" in text:
            title_part, body_part = text.split("BODY:", 1)
            title = title_part.replace("TITLE:", "").strip()
            body = body_part.strip()
        else:
            # Fallback: use first line as title, rest as body
            lines = text.split("\n", 1)
            title = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else ""

        return title, body

    def generate_branch_name(self, description: str) -> str:
        """
        Generate a git branch name from a natural language description.

        Args:
            description: A natural language description of the work.

        Returns:
            str: The generated branch name (e.g., "feat/add-login-page").
        """
        prompt = BRANCH_PROMPT_TEMPLATE.format(description=description)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        return response.choices[0].message.content.strip()

    def generate_scoped_commit_message(self, scope: str, files: list[str], diff: str) -> str:
        """
        Generate a commit message scoped to a specific module/group.

        Args:
            scope: The module or directory name (e.g., "cli", "ai").
            files: List of file paths in this group.
            diff: The combined diff text for this group.

        Returns:
            str: The generated scoped commit message.
        """
        style_instructions = STYLE_INSTRUCTIONS.get(self.style, STYLE_INSTRUCTIONS["conventional"])
        prompt = SCOPED_COMMIT_PROMPT_TEMPLATE.format(
            scope=scope,
            file_list=", ".join(files),
            diff=diff,
            style_instructions=style_instructions,
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        return response.choices[0].message.content.strip()