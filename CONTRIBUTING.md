# Contributing

First off, thank you for considering contributing to this project! It's people like you that make this project great.

## Getting Started

Before you begin:
- Try running the app to get familiar with the project
- Familiarize yourself with the project structure and architecture

## Installation and Build Guide

### macOS / Linux

1. **Install dependencies**:
   ```bash
   pip install -e .
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Docker

Build and run with Docker Compose:

```bash
docker-compose up --build
```

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for this project. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

- Use a clear and descriptive title for the issue to identify the problem
- Describe the exact steps which reproduce the problem in as many details as possible
- Provide specific examples to demonstrate the steps

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for this project, including completely new features and minor improvements to existing functionality.

- Use a clear and descriptive title for the issue to identify the suggestion
- Provide a step-by-step description of the suggested enhancement in as many details as possible
- Explain why this enhancement would be useful to most users

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Include screenshots and animated gifs in your pull request whenever possible
- Follow the Python styleguides
- End all files with a newline

## Styleguides

### Git Commit Messages

- Use the present tense ("add feature" not "added feature")
- Use the imperative mood ("move cursor to..." not "moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- We use conventional commits: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `perf:`, `ci:`, `build:`, `revert:`

### Python Styleguide

We use Ruff for linting and formatting. Run these commands before committing:

```bash
ruff check .
ruff format .
```

## Building

```bash
pip install -e .
```

## Running Tests

Before submitting a pull request, run all the tests to ensure nothing has broken:

```bash
python run_tests.py
```

Or manually:

```bash
pytest --cov=main --cov-report=html tests/
```

## Code Architecture

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

### Understanding the Code

- App initializes DB connection (optional)
- UI built with Textual widgets (Header, Buttons, Input, Static)
- Events handled via `on_button_pressed` and `on_key`
- Git commands executed synchronously with error checking
- Tests use pytest and Textual's Pilot for e2e

## Additional Notes

### Principles

- **Simplicity**: Write code that is easy for humans to read, fast for machines to execute. Less is more.
- **Focus**: Avoid feature creep. Focus on the core functionality and build upon it.
- **User-centric**: Focus on building what people want and bring maximum value.

### Issue and Pull Request Labels

- `bug` - Issues that are bugs
- `enhancement` - Issues that are feature requests
- `documentation` - Issues or pull requests related to documentation
- `good first issue` - Good for newcomers

## Troubleshooting

If files or folders are not visible (especially hidden files starting with .), on macOS:

- In Finder: Press `Cmd` + `Shift` + `.` to temporarily toggle hidden files.
- Via Terminal (persistent): `defaults write com.apple.finder AppleShowAllFiles YES && killall Finder`. To hide again, replace `YES` with `NO`.

## Pre-commit Checks

Run all checks before commit/push:

```bash
python check_all.py
```

This runs:
- Linting with Ruff
- Formatting check with Ruff
- Tests with coverage
- Security scanning with Bandit

## Release

Bump version:

```bash
python bump_version.py <major|minor|patch>
```

Then tag a version (e.g., v1.0.0) to trigger automated release with built package.

## Security

Code scanned with Bandit and CodeQL. Dependabot enabled for dependency updates.

## Join the Community

Feel free to open issues for bugs, feature requests, or general questions. We welcome contributions!

Thank you for contributing to this project!
