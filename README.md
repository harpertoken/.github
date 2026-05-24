<a href="https://github.com/harpertoken/.github" aria-label="git-gui"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#44403c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 2v2"/><path d="M14 2v2"/><path d="M16 8a1 1 0 0 1 1 1v8a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V9a1 1 0 0 1 1-1h14a4 4 0 1 1 0 8h-1"/><path d="M6 2v2"/></svg> <code>git-gui</code></a>

GUI for common Git operations.

This repository also contains organization defaults for `harpertoken`.

Requires a Python build with Tk support.

## Paths

- `profile/readme.md` - organization profile
- `.github/workflows/update-org-activity.yml` - profile activity updater
- `.github/ISSUE_TEMPLATE/` - issue templates
- `.github/PULL_REQUEST_TEMPLATE.md` - pull request template
- `docs/` - project notes

The activity updater rewrites only:

```md
<!-- ORG_ACTIVITY:START -->
<!-- ORG_ACTIVITY:END -->
```

## Commands

```sh
make install
make run
python run_tests.py
python check_all.py
```

Run directly:

```sh
python main.py
```

Run with Docker:

```sh
docker-compose up --build
```

## Development

```sh
ruff check .
ruff format .
pre-commit install
pre-commit run --all-files
```

Commit messages use conventional commit types. To install the local hook:

```sh
cp scripts/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

## Release

```sh
python bump_version.py <major|minor|patch>
```

Tag a version such as `v1.0.0` to trigger the release workflow.
