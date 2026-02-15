# ai/prompts.py
# Purpose: Store prompt templates.

COMMIT_PROMPT_TEMPLATE = """
You are an expert software engineer.

Generate a concise conventional commit message based on the following git diff.

Follow this format:

type(scope): short summary

Optional body if necessary.

Git diff:
{diff}
"""
