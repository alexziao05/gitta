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

SCOPED_COMMIT_PROMPT_TEMPLATE = """
You are an expert software engineer.

Generate a concise commit message for changes in the "{scope}" module.
The changes affect these files: {file_list}

{style_instructions}

Git diff:
{diff}
"""

BRANCH_PROMPT_TEMPLATE = """
You are an expert software engineer.

Generate a git branch name from the following description.

Rules:
- Use lowercase letters, numbers, and hyphens only
- Use a conventional prefix: feat/, fix/, refactor/, docs/, chore/, test/, perf/, ci/
- Keep it short (2-5 words after the prefix)
- Use hyphens to separate words
- No trailing hyphens

Respond with ONLY the branch name, nothing else.

Description: {description}
"""

PR_PROMPT_TEMPLATE = """
You are an expert software engineer writing a pull request description.

Based on the following commits, file stats, and diff, generate:
1. A short PR title (under 70 characters, no prefix)
2. A markdown body with:
   - A "## Summary" section with 1-3 bullet points explaining what changed and why
   - A "## Changes" section listing key modifications

Keep it concise and focused on what a reviewer needs to know.
The diff may be truncated — use the file stats and commits for full coverage.

Respond in this exact format (no extra text):
TITLE: <title here>
BODY:
<markdown body here>

Branch: {branch}

Commits:
{commits}

File stats:
{stat}

Diff (may be truncated):
{diff}
"""
