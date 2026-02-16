# gitta

AI-powered Git commit messages and PR descriptions from your terminal.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexziao05/gitta/main/demo.gif" alt="Gitta Demo" width="600">
</p>

## Installation

```bash
pip install gitta
```

## Quick Start

```bash
gitta init          # Set up your AI provider
gitta add .         # Stage files + generate commit message
gitta ship          # Stage, commit, and push in one step
gitta pr --create   # Generate and create a PR on GitHub
```

## Usage

### Setup

Run the interactive setup wizard to configure your AI provider:

```bash
gitta init
```

You'll be prompted for your provider name, API base URL, model, commit style, and API key. Your API key is stored securely in the system keyring.

<p align="center">
  <img src="https://raw.githubusercontent.com/alexziao05/gitta/main/configuration.png" alt="Recommended Configuration" width="500">
</p>

### Committing

Generate an AI-powered commit message from your staged changes:

```bash
gitta add .              # Stage files + generate message
gitta commit             # Generate message for already-staged files
gitta commit --dry-run   # Preview without committing
```

You'll see the generated message and can **confirm** (y), **edit** (e), or **cancel** (n).

### Split Commits

When changes span multiple modules, use `--split` to create scoped commits:

```bash
gitta commit --split
gitta add . --split
gitta ship --split
```

Gitta groups changes by module (e.g. `cli`, `ai`, `core`) and generates a message for each. You can then commit **all** separately, **merge** into one, or **cancel**.

To enable by default:

```bash
gitta config set multi_file true
```

### Ship

Stage everything, generate a commit message, and push — all in one step:

```bash
gitta ship
```

### Pull Requests

Generate a PR title and description from all commits on your branch:

```bash
gitta pr                    # Preview the generated title + body
gitta pr --create           # Push branch and create PR on GitHub
gitta pr --create --draft   # Create as draft
gitta pr --base develop     # Compare against a specific base branch
```

When creating, you can **confirm** (y), **edit** (e), or **cancel** (n) before the PR is submitted. Requires the [GitHub CLI](https://cli.github.com/) (`gh`).

### Utilities

```bash
gitta log                       # Show recent commits in a table
gitta log -n 20                 # Show last 20 commits
gitta config list               # Show all config values
gitta config get <key>          # Get a config value
gitta config set <key> <value>  # Update a config value
gitta doctor                    # Diagnose setup issues
```

## Configuration

Config is stored in `~/.gitta/config.toml`. Available settings:

| Key | Description | Default |
|---|---|---|
| `provider` | AI provider name (e.g. `openai`) | — |
| `base_url` | API endpoint | — |
| `model` | Model identifier (e.g. `gpt-4o`) | — |
| `style` | Commit format: `conventional`, `simple`, `detailed` | — |
| `max_diff_chars` | Max diff size sent to AI | `32000` |
| `multi_file` | Enable split commits by default | `false` |
