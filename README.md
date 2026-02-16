# gitta

AI-powered Git commit messages from your terminal.

By: Alex Huang 

## Installation

```bash
pip install gitta
```

## Quick Start

### 1. Set up your AI provider

```bash
gitta init
```

You'll be prompted for:
- **Provider name** (e.g. `openai`, `anthropic`)
- **API base URL** (e.g. `https://api.openai.com/v1`)
- **Model** (e.g. `gpt-4o`)
- **Commit style** (`conventional`, `simple`, or `detailed`)
- **API key**

### 2. Stage files and commit

```bash
gitta add .
```

Stages your files, generates a commit message, and lets you confirm, edit, or cancel.

### 3. Or commit with already-staged files

```bash
git add .
gitta commit
```

### 4. Stage, commit, and push in one step

```bash
gitta ship
```

## Commands

| Command | Description |
|---|---|
| `gitta init` | Configure your AI provider and API key |
| `gitta add <files>` | Stage files and generate a commit message |
| `gitta commit` | Generate a commit message for staged changes |
| `gitta commit --dry-run` | Preview the message without committing |
| `gitta ship` | Stage all, commit, and push |
| `gitta doctor` | Check your setup for issues |