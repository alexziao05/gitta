# ai/prompts.py
# Purpose: Store prompt templates.

STYLE_INSTRUCTIONS = {
    "conventional": """Follow conventional commit format:

type(scope): short summary

Optional body if necessary.

Types: feat, fix, refactor, docs, style, test, chore, perf, ci, build.""",

    "simple": """Write a short, single-line commit message summarizing the change. No prefix, no body.""",

    "detailed": """Write a detailed commit message with:

- A short summary line (max 72 chars)
- A blank line
- A detailed body explaining what changed and why.""",
}

COMMIT_PROMPT_TEMPLATE = """
You are an expert software engineer.

Generate a concise commit message based on the following git diff.

{style_instructions}

Git diff:
{diff}
"""
