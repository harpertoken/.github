# Git TUI

A simple Terminal User Interface for Git operations.

## Documentation

See [docs/](docs/) for detailed project state and coverage info.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Conventional Commits

This project follows conventional commit standards.

### Setup

To enable commit message validation:

1. Copy the commit hook: `cp scripts/commit-msg .git/hooks/commit-msg`
2. Make it executable: `chmod +x .git/hooks/commit-msg`

### Usage

Commit messages must:
- Start with a type: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `perf:`, `ci:`, `build:`, `revert:`
- Be lowercase
- First line ≤60 characters

### History Cleanup

To rewrite existing commit messages in the history:

Run `scripts/rewrite_msg.sh`

This will lowercase and truncate first lines, then force-push the changes.

## Installation

pip install .

## Usage

python main.py

## Troubleshooting

If files or folders are not visible (especially hidden files starting with .), on macOS:

- In Finder: Press `Cmd` + `Shift` + `.` to temporarily toggle hidden files.
- Via Terminal (persistent): `defaults write com.apple.finder AppleShowAllFiles YES && killall Finder`. To hide again, replace `YES` with `NO`.

## Docker

Build and run with Docker Compose:

docker-compose up --build

## Testing

Run tests with coverage and security scan: python run_tests.py

Or manually: pytest --cov=main --cov-report=html tests/

Run all checks before commit/push: python check_all.py

## Security

Code scanned with Bandit and CodeQL. Dependabot enabled for dependency updates.

## Development

Code linted and formatted with Ruff. Run `ruff check .` for linting and `ruff format .` for formatting. CI runs on push/PR.

## Release

Bump version: python bump_version.py <major|minor|patch>

Then tag a version (e.g., v1.0.0) to trigger automated release with built package.

## Code Architecture

### Overview
The app is built with Textual for the TUI framework. Main components:
- `GitTUI` class: Core app logic, UI composition, event handling
- Git command execution: Uses `subprocess` to run shell commands
- Database: Optional PostgreSQL for command history (falls back gracefully)
- UI: Buttons for actions, input for commit messages, output display

### Project Structure
```
.
├── .github/
│   ├── ISSUE_TEMPLATE/          # Issue templates
│   ├── workflows/               # GitHub Actions
│   └── PULL_REQUEST_TEMPLATE.md # PR template
├── docs/                        # Documentation
├── tests/                       # Test files
├── CONTRIBUTING.md              # Contributing guide
├── Dockerfile                   # Docker image
├── README.md                    # This file
├── bump_version.py              # Version bumping script
├── check_all.py                 # Pre-commit checks
├── docker-compose.yml           # Docker Compose
├── main.py                      # Main app code
├── pyproject.toml               # Packaging config
└── run_tests.py                 # Test runner
```

### Key Files
- `main.py`: Entry point, app definition
- `tests/`: Unit and e2e tests
- `pyproject.toml`: Packaging and dependencies
- Workflows: CI/CD automation

### How to Operate
1. **Run the App**: `python main.py` launches the TUI
2. **Git Operations**: Click buttons or use keyboard shortcuts (s=status, a=add, etc.)
3. **Commit**: Type message in input field, press Enter or click Commit
4. **History**: View past commands if DB is connected
5. **Development**: Run `python check_all.py` before committing

### Understanding the Code
- App initializes DB connection (optional)
- UI built with Textual widgets (Header, Buttons, Input, Static)
- Events handled via `on_button_pressed` and `on_key`
- Git commands executed synchronously with error checking
- Tests use pytest and Textual's Pilot for e2e

## Features

- Git status, add, diff, log, commit, push, pull
- Command history (with PostgreSQL)
- Keyboard shortcuts