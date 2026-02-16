# gitta

AI-powered Git commit messages from your terminal.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexziao05/gitta/main/demo.gif" alt="Gitta Demo" width="600">
</p>

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
| `gitta log` | Show recent commits in a table |
| `gitta log -n 20` | Show last 20 commits |
| `gitta config list` | Show all configuration values |
| `gitta config get <key>` | Get a single config value |
| `gitta config set <key> <value>` | Update a config value |
| `gitta doctor` | Check your setup for issues |

## Recommended Configuration

<p align="center">
  <img src="https://raw.githubusercontent.com/alexziao05/gitta/main/configuration.png" alt="Recommended Configuration" width="500">
</p>
